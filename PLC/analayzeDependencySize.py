import json
from sys import argv

from numpy import average
if(len(argv) < 2):
    print("Provide dependencies json")
    exit()
jsonFile = argv[1]
with open(jsonFile, "r") as fp:
    globalDependencies = json.load(fp)

print("json loaded")

lastLayer = False
for layer in range(20):
    sizeLayer = []
    for tag in globalDependencies:
        if(layer > len(globalDependencies[tag]["indirect"]) - 1):
            lastLayer = True
            break
        sizeLayer.append(len(globalDependencies[tag]["indirect"][layer]))
    if(lastLayer):
        break
    sizeLayer.sort()
    averageLen = average(sizeLayer)
    range = str(sizeLayer[0]) + "-" + str(sizeLayer[-1])
    print("Layer", layer, "stats")
    print("Number of tags with dependencies:", len(globalDependencies))
    print("Average number of elements at this layer:", averageLen)
    print("Range of lengths across dependencies:", range)
    
        

