from sys import argv
import binascii

chunkSize = 1 #bytes to compare at once

if(len(argv) < 3):
    print("Please provide two files")
    exit()
firstFile = argv[1]
secondFile = argv[2]
byteIndex = 0
with open(firstFile, "rb") as firstFP:
    with open(secondFile, "rb") as secondFP:
        while(True):
            leftByte = firstFP.read(chunkSize)
            rightByte = secondFP.read(chunkSize)
            if(len(leftByte) == 0 or len(rightByte) == 0):
                break
            if(leftByte != rightByte):
                print("", binascii.b2a_hex(leftByte), "\n", binascii.b2a_hex(rightByte), ":", byteIndex)
            byteIndex += chunkSize
