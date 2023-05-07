import re

functions = {}
f = open("Parsed-MPI_V2.txt")
for line in f.readlines():
    #finds called function name
    functionName = re.search(": \S+!\S+", line).group()[2:]
    if(functionName in functions):
        functions[functionName] += 1
    else:
        functions[functionName] = 1
    #finding caller functions
    functionName = re.search("<- \S+", line).group()[3:]
    if(functionName in functions):
        functions[functionName] += 1
    else:
        functions[functionName] = 1

f.close()
f = open("output.txt", "w")
for key in sorted(functions, key= lambda x:functions[x]):
    print(key + ": " + str(functions[key]))
    f.write(key + ": " + str(functions[key]) + "\n")

f.close()



#pairwise list of functions
#one after other
#count

#sequence burst rates A->A = 2

#use whitelist of functions

    