import re


filename = "Parsed-WS7_S7AG.txt"
firstFunction = ""
secondFunction = ""
old = ""
pairwiseList = []
burstCount = 1

#this script goes through the Parsed-* file's contents and tracks a set of whitelisted functions.
#It looks at pairs of functions that occur after each other and records each one. (ie, funciton A is called, then B; recorded as A|B:1)
#the number appended is the Burst Count. This accounts for times when a function is repeatedly called after itself.
# (ie Funtction A, then Function A, then Function A; recorded as A|A:3)



#AGBEF whitelist
# whitelist = {
#     "WS7_AGBEF!AGBEF_iGetZielHardware$qqsv",
#     "WS7_AGBEF!AGBEF_bGetStatusThreadEnable$qqsv",
#     "WS7_AGBEF!AGBEF_GetAgBefVerbindungsStatus$qqsv",
#     "WS7_AGBEF!AGBEF_GetMPIKlassenHandle$qqsv",
#     "WS7_AGBEF!AGBEF_bVerbindungOnline$qqsv",
#     "ws7v6!Pae_paa_konfigformFinalize+0xb74",
#     "ws7v6!Pae_paa_konfigformFinalize+0x48d"
# }
#WS7_V2_MPI whitelist
# whitelist = {
#     "ws7v6!EditorformFinalize+0x125",
#     "WS7_V2_MPI!MPI_V2_MPI_WriteHintInTraceDatei$qipc",
#     "WS7_V2_MPI!MPI_V2_GetKommunikationAlive$qi"
# }

#WS7_S7AG Whitelist
whitelist = {
    "WS7_S7AG!S7AG_Step7Zyklus$qqsv",
    "WS7_S7AG!S7AG_Step7ZyklusReady$qqsv",
    "WS7_S7AG!S7AG_BSRoutineReady$qqsv",
    "WS7_S7AG!S7AG_BSRoutine$qqsv"
}
f = open(filename)
f_out = open(filename[:-4] + "_BurstCount" + ".txt", "w")
for line in f.readlines():
    #finds called function name
    functionName = re.search(": \S+!\S+", line).group()[2:]
    if(functionName not in whitelist):
        continue
    if(secondFunction != "" and firstFunction != ""):
        old = firstFunction
        firstFunction = secondFunction
        secondFunction = functionName
        if(firstFunction == secondFunction):
            burstCount += 1
        else:
            f_out.write(old + "|" + firstFunction + ":" + str(burstCount)+"\n")
            #print(old + "|" + firstFunction + ":" + str(burstCount))
            burstCount = 1
    else: #handle initial conditions
        old = firstFunction
        firstFunction = secondFunction
        secondFunction = functionName


f.close()



#pairwise list of functions
#one after other
#count

#sequence burst rates A->A = 2

#use whitelist of functions