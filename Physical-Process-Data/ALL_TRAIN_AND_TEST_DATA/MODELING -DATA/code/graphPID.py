#This script reads in multiple log files output from FactoryIO and compares a tag among them. The variable "compareAttribute" defines the tag name to compare
#The variable "dataDir" defines where the log files are to be found
#"logFileMarker" is the string marker used to decide which logs to consider
#currently the script labels the graphed data based on the "P" value used in a PID simmulation, but it ultimately gets the name by the filename


from tkinter import Label
import matplotlib.pyplot as plt
import numpy as np
import json
from os import listdir
from os.path import isfile, join


#from tkinter import Tk
from tkinter.filedialog import *
print("Loading...")
graphData = dict()
compareAttribute = "Level meter"
dataDir = "Data/ProcessVariableTester";
logFileMarker = "Test_60_P"
pValues = []

for filename in [f for f in listdir(dataDir) if(isfile(join(dataDir, f)) and logFileMarker in f)]:
    print("Extracting from filename: " + filename)
    pValueStart = filename.find("Value_")
    pValueString = filename[pValueStart+6:-4]
    pValueString = pValueString.replace("-", ".")
    #add break here to exclude/include specific pValues

    pValues.append(pValueString)
    data = dict()
    attributesOrdered = []
    dataStart = False
    #read through and get all the field names
    file = open(join(dataDir, filename), "r")
    for line in file.readlines():
        if(dataStart):
            if(line != ""):
                vals = line.split(",")
                #print(vals)
                index = 0
                for name in attributesOrdered:
                    data[name].append(float(vals[index]))
                    index += 1
        elif(line.startswith("@ATTRIBUTE")):
            start = line.find("\"")
            end = line.find("\"", start+1)
            attributeName = line[start+1:end]
            data[attributeName] = []
            attributesOrdered.append(attributeName)
            print("Attribute Name: " + attributeName)
        elif(line.startswith("@DATA")):
            dataStart = True
        
    graphData[pValueString + "_millis"] = data["millis"]
    print(data[compareAttribute])
    graphData[pValueString] = data[compareAttribute]
    file.close()




yLabels = pValues
i = 0
print("Plotting values: " + str(yLabels))       
print("Plotting...")


for yLabel in yLabels:
    print("Capturing values for label: " + yLabel)
    x = graphData[yLabel+"_millis"]
    y = graphData[yLabel]
    #print(y)
    plt.plot(x,y, label="P = " + yLabel)
    print()
    print()
print("Plotted, showing")
plt.legend()
plt.axhline(2, color = "black")
plt.xlabel("Milliseconds")
plt.ylabel("Holding Tank Level")
plt.show()

