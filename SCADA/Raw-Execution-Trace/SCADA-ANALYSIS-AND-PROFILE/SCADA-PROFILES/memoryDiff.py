
firstFile = open("./WinSPS/WinSPS_Zeroes_Full.dmp", "rb")
secondFile = open("./WinSPS/WinSPS_Ones_Full.dmp", "rb")

BUFFER_SIZE = 512
firstBuffer = firstFile.read(BUFFER_SIZE)
secondBuffer = secondFile.read(BUFFER_SIZE)
diffBytes = 0
bytesRead = 512
while(len(firstBuffer) != 0 and len(secondBuffer) != 0):
    if(firstBuffer != secondBuffer):
        diffBytes += BUFFER_SIZE
        # print("Diff found")
        # print(str(bytesRead))
        # print()
    firstBuffer = firstFile.read(BUFFER_SIZE)
    secondBuffer = secondFile.read(BUFFER_SIZE)

print("Total diff: " + str(diffBytes))
