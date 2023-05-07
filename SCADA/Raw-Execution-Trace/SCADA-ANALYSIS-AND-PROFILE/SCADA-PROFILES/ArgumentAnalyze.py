#copied from ../../Communication Investigation/ArgumentInvestigation/

#Running the command: bm <module>!<functionName> "kv 2; r; g"
#inputFile should be the name of that output log file. For the most consistent results, remove all lines up until execution is passed back to the program
#produces a json file with each object being a unique function, member elements being lists for each register and the stack. the list contains all unique values these
#   elements contained when the function was called. (ie if 'eax' only has one element in its array, that means every time the function was called eax always had that value)
import json
import re
import sys

inputFile = sys.argv[1]
f = open(inputFile)
out = open("ArgumentProfile_" + inputFile[0:-3] + "json", "w")

linesread = 0
printline = ""
functionName = ""
uniqueArgs = {}

for line in f.readlines():
    linesread += 1
    if(line.find("00") == 0): #the current functionName
        m = re.search("\S*!\S*", line) #grab functionName that had the breakpoint
        #out.write(printline)
        
        if(m != None):
            printline = printline + m.group()
            functionName = m.group()
            if(functionName not in uniqueArgs):
                uniqueArgs[functionName] = {}
                uniqueArgs[functionName]["eax"] = set()
                uniqueArgs[functionName]["ebx"] = set()
                uniqueArgs[functionName]["ecx"] = set()
                uniqueArgs[functionName]["edx"] = set()
                uniqueArgs[functionName]["esi"] = set()
                uniqueArgs[functionName]["edi"] = set()
                uniqueArgs[functionName]["stack"] = set()
        
        m = re.search("(\S+) (\S+) (\S+)", line) #grab stack args
        if(m != None):
            uniqueArgs[functionName]["stack"].add(m.groups()[0])
            uniqueArgs[functionName]["stack"].add(m.groups()[1])
            uniqueArgs[functionName]["stack"].add(m.groups()[2])
    if(line.find('01') == 0): #the format of the kv functionName places the caller of 00 at 01
        m = re.search("\S*!\S*", line) #grab calling functionName
        if(m != None):
            printline = printline + " <- " + m.group()
        else:
            m = re.search("\S*$\S?", line) #to catch lack of functionName on the line
            printline = printline + " <- " + m.group() + "\n"
            #out.write(printline)
    if(line.find("eax=") == 0):
        printline += line
        m = re.search("eax=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["eax"].add(m.groups()[0])
        m = re.search("ebx=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["ebx"].add(m.groups()[0])
        
        m = re.search("ecx=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["ecx"].add(m.groups()[0])
        
        m = re.search("edx=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["edx"].add(m.groups()[0])
        
        m = re.search("esi=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["esi"].add(m.groups()[0])

        m = re.search("edi=(\S+)", line) #match the time stamp
        if(m != None):
            uniqueArgs[functionName]["edi"].add(m.groups()[0])


for key in uniqueArgs:
    for type in uniqueArgs[key]:
        uniqueArgs[key][type] = list(uniqueArgs[key][type])
out.write(json.dumps(uniqueArgs))