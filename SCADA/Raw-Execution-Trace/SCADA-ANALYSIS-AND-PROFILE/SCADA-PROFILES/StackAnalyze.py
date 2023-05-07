#copied from ../../Communication Investigation/ArgumentInvestigation/
# Author: Keaton Sadoski
# Email: dksados@sandia.gov
#Running the command: bm <module>!<functionName> "kv 2; r; g"
#inputFile should be the name of that output log file. For the most consistent results, remove all lines up until execution is passed back to the program
#produces a json file with each object being a unique function, member elements being lists for each register and the stack. the list contains all unique values these
#   elements contained when the function was called. (ie if 'eax' only has one element in its array, that means every time the function was called eax always had that value)
from inspect import stack
import json
import re
import sys

inputFile = sys.argv[1] # first argument is name of log file with above code run
f = open(inputFile)
out = open("StackProfile_" + inputFile[0:-3] + "json", "w")

linesread = 0
printline = ""
functionName = ""
stackProfile = {}

for line in f.readlines():
    linesread += 1
    if(line.find("00") == 0): #the current functionName
        m = re.search("\S*!\S*", line) #grab functionName that had the breakpoint
        #out.write(printline)
        
        if(m != None):
            baseFunc = m.group()
            if(baseFunc not in stackProfile):
                stackProfile[baseFunc] = {}

                
        
    if(line.find('01') == 0): #the format of the kv functionName places the caller of 00 at 01
        m = re.search("\S*!\S*", line) #grab calling functionName
        secondFunc = ""
        if(m != None):
            secondFunc = m.group()
        else:
            m = re.search("\S*$\S?", line) #to catch lack of functionName on the line
            if(m != None):
                secondFunc = m.group()
        if(secondFunc not in stackProfile[baseFunc]):
            stackProfile[baseFunc][secondFunc] = {}
    
    if(line.find('02') == 0): #the format of the kv functionName places the caller of 00 at 01
        m = re.search("\S*!\S*", line) #grab calling functionName
        thirdFunc = ""
        if(m != None):
            thirdFunc = m.group()
        else:
            m = re.search("\S*$\S?", line) #to catch lack of functionName on the line
            if(m != None):
                thirdFunc = m.group()
        if(thirdFunc not in stackProfile[baseFunc][secondFunc]):
            stackProfile[baseFunc][secondFunc][thirdFunc] = 1
        else:
            stackProfile[baseFunc][secondFunc][thirdFunc] += 1
    
        

# for key in stackProfile:
#     for type in stackProfile[key]:
#         stackProfile[key][type] = list(stackProfile[key][type])
out.write(json.dumps(stackProfile))