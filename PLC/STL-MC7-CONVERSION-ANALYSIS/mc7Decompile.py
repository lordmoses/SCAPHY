
from array import typecodes
from operator import ne
from sys import argv
import opcodeDefinitions as mc7

if(len(argv) < 2):
    print("Provide an MMC file")
    exit()

mmcFile = argv[1]
outputFile = open(mmcFile[:-4]+"STL.txt", "w")
byteFile = open(mmcFile, "rb")

class Block:
    def __init__(self):
        self.type = ""
        self.statementList = []
        self.number = -1
        self.length = -1
    def importHeader(self, header:str):
        print("Header:", header, file=outputFile)
        typeCode = header[5*2:5*2+2]
        print("Typecode", typeCode, file=outputFile)
        if(typeCode == "0E"):
            self.type = "FB"
        elif(typeCode == "08"):
            self.type = "OB"
        print("Type", self.type, file=outputFile)
        self.number = int(header[6*2:6*2+4], 16)
        self.length = int(header[8*2:8*2+8].strip("0"), 16)
    def importOpcode(self, opcode:str):
        self.statementList.append(opcode)
        print("Imported:", opcode, ": into block", self.number, file=outputFile)
        return
    def importWithArg(self, opcode:str, arg:str):
        print("Skeleton opcode", opcode, file=outputFile)
        numberToReplace = len(arg)
        placeHolder = "X"*numberToReplace
        opcode = opcode.replace(placeHolder, arg)
        print("Filled:", opcode, file=outputFile)
        self.statementList.append(opcode)
        return
    def print(self, file=outputFile):
        print("<METADATA>", file=outputFile)
        print(self.type, "Block", self.number, "with", len(self.statementList), "statements", file=outputFile)
        print("</METADATA>", file=outputFile)
        print("<STATEMENT LIST>", file=outputFile)
        for stl in self.statementList:
            print(stl, file=outputFile)
        print("</STATEMENT LIST>", file=outputFile)
        print( file=outputFile)



blocks = []
inBlock = False
currentBlock = None
argNext = False
argOpcode = ""
while True:
    nextBytes = byteFile.read(1).hex().upper()
    #print("Cursor:", nextBytes, type(nextBytes), file=outputFile, file=outputFile)
    if(nextBytes == ''):
        print("End of File reached", file=outputFile)
        blocks.append(currentBlock)
        break
    elif(nextBytes == "70" and not inBlock):
        nextBytes += byteFile.read(1).hex().upper()
        if(nextBytes != "7070"):
            print("Malformed bytecode. Detected part of start of block signature outside of block.", file=outputFile)
            exit()
        else:
            print("Start of block detected", file=outputFile)
        inBlock = True
        if(currentBlock):
            print("Appending finished block", file=outputFile)
            blocks.append(currentBlock)
            currentBlock = Block()
        else:
            currentBlock = Block()
        header = nextBytes + byteFile.read(34).hex().upper()
        currentBlock.importHeader(header)
        continue

    elif(inBlock):
        if(nextBytes in mc7.singleByteOpcodeSingleByteArg):
            print("Detected single byte opcode", file=outputFile)
            stl = mc7.singleByteOpcodeSingleByteArg[nextBytes]
            arg = byteFile.read(1).hex().upper()
            currentBlock.importWithArg(stl, arg)
        else:
            nextBytes += byteFile.read(1).hex().upper()
            print("Detected double byte opcode", file=outputFile)
            if(nextBytes in mc7.doubleByteOpcodeNoArg):
                print("No arg", file=outputFile)
                stl = mc7.doubleByteOpcodeNoArg[nextBytes]
                currentBlock.importOpcode(stl)
            elif(nextBytes in mc7.doubleByteOpcodeDoubleByteArg):
                print("Double Byte arg", file=outputFile)
                stl = mc7.doubleByteOpcodeDoubleByteArg[nextBytes]
                arg = byteFile.read(2).hex().upper()
                currentBlock.importWithArg(stl, arg)
            elif(nextBytes in mc7.doubleByteOpcodeQuadByteArg):
                print("Quad byte arg", file=outputFile)
                stl = mc7.doubleByteOpcodeQuadByteArg[nextBytes]
                arg = byteFile.read(4).hex().upper()
                currentBlock.importWithArg(stl, arg)

    if(nextBytes == "6500"): #BE
        inBlock = False           
block: Block
for block in blocks:
    block.print(file=outputFile)

