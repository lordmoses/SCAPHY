from tkinter import Label
import matplotlib.pyplot as plt
import numpy as np
import json
#from tkinter import Tk
from tkinter.filedialog import *
file = askopenfile(mode="r")  
dataDir = "/factoryIO/";
print("Loading...")

data = dict()
lineNum = 0
attributesOrdered = []
readingData = False
size = 0
dataIndex = 0
title = ""
#read through and get all the field names
for line in file.readlines():
    if(line.startswith("@ATTRIBUTE")):
        start = line.find("\"")
        end = line.find("\"", start+1)
        attributeName = line[start+1:end]
        while(attributeName in data): #avoids collisions where the same name is used mutliple times
            attributeName = attributeName + "Alt"
        data[attributeName] = np.empty(size)
        attributesOrdered.append(attributeName)
        print(attributeName)
    if(line.startswith("% 4")):
        index = line.find(": ")
        sizeString = line[index+2:-1]
        size = int(sizeString)
    if(line.startswith("% 2")):
        index = line.find(": ")
        title = line[index+2:-1]
    if(line != "" and readingData):
        vals = line.split(",")
        index = 0
        for name in attributesOrdered:
            data[name][dataIndex] = vals[index]
            
            index += 1
        dataIndex += 1
    if(line.startswith("@DATA")):
        readingData = True


xLabel = "millis"
#choose y axis for plotting
yAxisSelect = ""
yLabels = []
i = 0
print("Choose y axis ")
keys = []
for key in data.keys():
    print(str(i) + ": " + key)
    keys.append(key)
    i += 1
while(yAxisSelect == ""):
    yAxisSelect = input("Number of selection (comma separated): ")
    yLabels = []
    yLabelsIndex = yAxisSelect.split(",")
    for k in range(len(yLabelsIndex)):
        index = int(yLabelsIndex[k])
        print("Index detected: " + str(index))
        if(index >= len(keys) or index < 0):
            print(yLabelsIndex[k] + " is an invalid index. Try again")
            yAxisSelect = ""
            break
        print("Added " + keys[index])
        yLabels.append(keys[index])
print("Plotting values: " + str(yLabels))       



print("Plotting...")
x = data[xLabel]
print(len(yLabels))
fig, axs = plt.subplots(len(yLabels), sharex=True)
fig.tight_layout(h_pad=2) # ensure they don't overlap
exploit = input("Describe subtitle")
fig.suptitle("Factory I/O Scene: " + title + "\n" + exploit)
plt.subplots_adjust(top=0.80, bottom=0.1) #ensure there is room for the super title
index = 0
for yLabel in yLabels:
    print("Capturing values for label: " + yLabel)
    
        
    axs[index].plot(x/1000,data[yLabel], label=yLabel)
    axs[index].set_title(yLabel)
    print("Plotted " + str(len(data[yLabel])) + " Values")
    print()
    index += 1
for ax in axs.flat:
    ax.set(xlabel='Seconds')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
print("Plotted, showing")
#fig.savefig()
plt.show()

# plt.plot(each["millis"], each["Sensor_Level meter"], "blue")
#     plt.plot(each["millis"], each["Sensor_Setpoint"], "green")
#     plt.plot(each["millis"], each["Sensor_Flow meter"], "purple")

#     plt.plot(each["millis"], each["Actuator_Discharge valve"], "brown")
#     plt.plot(each["millis"], each["Actuator_Fill valve"], "olive")
