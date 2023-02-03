import enum
import re
import string
from sys import argv
import json
import PLC

dependencyLayers = 5

#state machine to keep track of where we are in the stl file
class State(enum.Enum):
    searchNetwork = 0 #looking for the start of a network
    network = 1 #found the start of a network, looking for stl code
    stl = 2 #reading stl code
    definitions = 3 #at the end of the file, reading memory names
    outsideOB = 4
state = State.outsideOB



def parse(statementList:list, plc:PLC):
    for op,arg in statementList:  
        plc.mapping[op](plc, arg) 
        ##print("RLO:",plc.statusWord["RLO"])
    plc.resetState()
    return 0


opcodeExtract = re.compile("^([\w=()]+)")
argExtract = re.compile("\S+\s+(\S+)\s+(\S+);")
dependExtract = re.compile("\w+:[\w.]+")
if(len(argv) < 2):
    #print("Provide an STL file")
    exit()

inFile = argv[1]
#print("Reading from ", inFile)

plc = PLC.PLC()



with open(inFile, "r") as inFp:
    inLines = inFp.readlines()
    networks = []
    statements = []
    organizationBlock = ""
    stlLineEnds = [";", "(", ")"]
    symbols = {}
    decompilation = []
    for line in inLines:
        line = line.strip() ##format lines to a regular form
        if(line.startswith("//") or len(line) == 0): ##ignore comments
            continue
        if(line.find(":") != -1):
            line = line[line.find(":")+1:].strip()
        
        
        if(state == State.stl and line[-1] not in stlLineEnds): #end of network since no more statements
            state = State.searchNetwork
            #print("Title:",networks[-1]["title"])
            networks[-1]["text"] = parse(statements, plc)
            #print(networks[-1]["text"])
            statements = []
        if(state == State.searchNetwork and line.startswith("NETWORK")):
            state = State.network
            continue
        if(state == State.network and line.startswith("TITLE")):
            networks.append({"title": line[line.find("=")+1:].strip()})
            continue
        if(state == State.network and line[-1] in stlLineEnds):
            state = State.stl
        if(state == State.stl and line[-1] in stlLineEnds):
            ##print(line)
            opcode = opcodeExtract.search(line).groups()[0]
            arg = argExtract.search(line)
            if(arg != None):
                arg = arg.groups()[0] + ":" + arg.groups()[1]
                ##print(arg)
            else:
                arg = ""
                ##print("None")
            ##print(opcode)
            statements.append([opcode, arg])
        if(state != State.outsideOB and line == "END_ORGANIZATION_BLOCK"):
            state = State.outsideOB
            continue
        if(state == State.outsideOB and "ORGANIZATION_BLOCK" in line):
            state = State.searchNetwork
            organizationBlock = line.split()[1]
            continue
        if(state == State.outsideOB and line != ""):
            symbolDefinition = line.split()
            ##print(symbolDefinition)
            symbol = symbolDefinition[0]
            memLocation = symbolDefinition[1] + ":" + symbolDefinition[2]
            symbols[memLocation] = symbol
            ##print("added symbol <", symbol, "> at", memLocation)

#print(plc.decompliations)      
#print(symbols)
#symbol replacements
humanReadable = []
dependencies = {}

def convertTagToSymbol(tagText:string):
    for memLoc in symbols.keys():
        if(memLoc in tagText):
            ##print(memLoc)
            tagText = tagText.replace(memLoc, symbols[memLoc])
    return tagText

for decomp in plc.decompliations:
    decomp = decomp.strip()
    decomp:str
    #print("Original:", decomp)
    dependent = re.search("\S+$", decomp)
    if(dependent == None):
        #print("No dependent found:", decomp)
        continue
    dependent = dependent.group()
    if(dependent not in dependencies):
        dependencies[dependent] = {
            "direct": set(),
            "indirect": [set()] * dependencyLayers
        }
    for match in dependExtract.findall(decomp)[:-1]: #ignore the last result as that is the dependent
        dependencies[dependent]["direct"].add(match)
    symbolText = convertTagToSymbol(decomp)
    #print("Human Readable:", symbolText)
    #print()
    humanReadable.append(symbolText + "\n")
with open(inFile + ".parsed", "w") as outFP:
    outFP.writelines(humanReadable)


for currentDepLayer in range(0,dependencyLayers):
    for tag in dependencies:
        print("Tag:", tag)
        dependencies[tag]["indirect"][currentDepLayer] = set()
        if(currentDepLayer == 0):
            dependencyList = dependencies[tag]["direct"]
        else:
            dependencyList = dependencies[tag]["indirect"][currentDepLayer-1]

        for dependency in dependencyList:
            dependencies[tag]["indirect"][currentDepLayer].add(dependency)
            if(dependency not in dependencies):
                continue
            print("Layer " + str(currentDepLayer) + " Dependency:", dependency)
            for nextLayerDepend in dependencies[dependency]["direct"]:
                print("\t\t" + "Nextlayer:", nextLayerDepend)
                dependencies[tag]["indirect"][currentDepLayer].add(nextLayerDepend)
        dependencies[tag]["indirect"][currentDepLayer]:set
        # dependencies[tag]["indirect"][currentDepLayer] = dependencies[tag]["indirect"] - dependencies[tag]["direct"]
        #print(dependencies[tag])

#needed to JSON encode the sets "Direct" and "Indirect"
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return json.JSONEncoder.default(self, obj)
with open(inFile + "_Dependencies.json", "w") as outFP:
    json_obj = json.dumps(dependencies, indent=4, cls=SetEncoder)
    outFP.write(json_obj)