# STL Command quick reference
# A AND
# FP Edge Positive
# R Reset
# = Assign
# JC Jump if RLO = 1
# AN AND NOT
# S Set
# BLD Program Display Instruction (Null)
# O OR
# CU Counter Up
# CD Counter Down
# L Load
# NOP Null Instruction
# BTI BCD to integer
# ON OR NOT
#source:
#https://cache.industry.siemens.com/dl/files/814/109751814/att_933093/v1/STEP_7_-_Statement_List_for_S7-300_and_S7-400.pdf

import string
class PLC:
    def __init__(self):
        self.nestStack = []
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
        self.ACCU1 = ""
        self.ACCU2 = ""
        self.decompliations = []
        self.dependGraphs = {}
        self.edges = set()

    def resetState(self):
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
        self.ACCU1 = ""
        self.ACCU2 = ""

    def A(self, arg : string):
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " AND " + arg
        else:
            self.statusWord["RLO"] += arg
        self.statusWord["/FC"] = 1
    def A_NOT(self, arg : string):
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " AND NOT " + arg
        else:
            self.statusWord["RLO"] += " NOT " + arg
        self.statusWord["/FC"] = 1
    def O(self, arg : string):
        if(arg == ""):
            O_NEST(arg)
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " OR " + arg
        else:
            self.statusWord["RLO"] += arg
        self.statusWord["/FC"] = 1
        self.statusWord["OR"] = 0
    def O_NOT(self, arg : string):
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " OR NOT " + arg
        else:
            self.statusWord["RLO"] += "NOT " + arg
        self.statusWord["/FC"] = 1
        self.statusWord["OR"] = 0
    def X(self, arg : string):
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " XOR " + arg
        else:
            self.statusWord["RLO"] += arg
        self.statusWord["/FC"] = 1
        self.statusWord["OR"] = 0
    def X_NOT(self, arg : string):
        if(self.statusWord["/FC"]):
            self.statusWord["RLO"] += " XOR NOT " + arg
        else:
            self.statusWord["RLO"] += "NOT" + arg
        self.statusWord["/FC"] = 1
        self.statusWord["OR"] = 0
    def O_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "OR"))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def A_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "AND"))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def A_NOT_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "AND NOT"))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def O_NOT_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "OR NOT"))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def X_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "XOR "))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def X_NOT_NEST(self, arg : string):
        self.nestStack.append((self.statusWord, "XOR NOT"))
        self.statusWord = {
            "OR": 0,
            "STA": 0,
            "RLO": "",
            "/FC": 0
        }
    def CLOSE_NEST(self, arg):
        oldWord, func = self.nestStack.pop()
        if(oldWord["/FC"]):
            self.statusWord["RLO"] = "(" + oldWord["RLO"] + ") " + func + " (" + self.statusWord["RLO"] + ")"
        else:
            self.statusWord["RLO"] =  self.statusWord["RLO"]
    def assign(self, arg: string): #stores RLO into arg location of memory
        print(self.statusWord["RLO"], "=>", arg)
        self.decompliations.append(self.statusWord["RLO"] + " => " + arg)
        self.statusWord["RLO"] = ""
        self.statusWord["/FC"] = 0
    def R(self, arg: string): #resets arg to 0 if RLO is 1, no change to arg otherwise
        print(self.statusWord["RLO"], "RESETS", arg)
        self.decompliations.append(self.statusWord["RLO"] + " RESETS " + arg)
    def S(self, arg: string): #sets the arg to 1 if RLO 1, no change to arg otherwise
        print(self.statusWord["RLO"], "SETS", arg)
        self.decompliations.append(self.statusWord["RLO"] + " SETS " + arg)

    def FP(self, arg: string): #See FN, this is positive edge
        print(self.statusWord["RLO"], "=>", arg)
        self.decompliations.append(self.statusWord["RLO"] + " => " + arg)
        self.statusWord["/FC"] = 1
        self.statusWord["RLO"] = "PosEdge[" + self.statusWord["RLO"] + "]"
    def FN(self, arg: string): #negative edge detection. State of RLO is stored in arg, current RLO is compared against state stored to determine next RLO
        print(self.statusWord["RLO"], "=>", arg)
        self.decompliations.append(self.statusWord["RLO"] + " => " + arg)
        self.statusWord["/FC"] = 1
        self.statusWord["RLO"] = "NegEdge[" + self.statusWord["RLO"] + "]"
    def JC(self, arg: string): #jump conditional. this implementation assumes the jump is not taken; the JC instruciton sets RLO to 1 if the jump is not taken
        self.statusWord["/FC"] = 1
        self.statusWord["RLO"] = "TRUE"
    def BLD(self, arg: string): #graphical command. Does nothing to the PLC state, meant to be interpreted by a visualizer (not on the actual production hardware)
        pass
    def CD(self, arg: string):
        print(self.statusWord["RLO"], "_/-- --", arg)
        self.decompliations.append("PosEdge["+self.statusWord["RLO"] + "] DECREMENTS " + arg)
        self.statusWord["/FC"] = 0
        self.statusWord["RLO"] = ""
    def CU(self, arg: string):
        print(self.statusWord["RLO"], "_/-- ++", arg)
        self.decompliations.append("PosEdge["+self.statusWord["RLO"] + "] INCREMENTS " + arg)
        self.statusWord["/FC"] = 0
        self.statusWord["RLO"] = ""

    def L(self, arg: string): #loads into accu1 from memory and bumps existing accu1 into accu2
        self.ACCU2 = self.ACCU1
        self.ACCU1 = arg
    def NOP(self, arg:string):
        pass
    def BTI(self, arg:string): #converts the accu1 integer from 3 digit encoded number to a binary encoded integer. (ie bottom 12 bits of register are divided into groups of 4 bits, 
        #each group representing one digit of the three digit number)
        #0x0312 (assumed to represent 312 decimal literally) -> 0x0138 (hex rep of 312 now stored in accu1)
        pass
    def T(self, arg:string): #stores accu1 into memory
        print(self.ACCU1, "=>", arg)
        pass
        

    mapping = {
        "A": A,
        "AN": A_NOT,
        "O": O,
        "ON": O_NOT,
        "X": X,
        "XN": X_NOT,
        "A(": A_NEST,
        "O(": O_NEST,
        "X(": X_NEST,
        "AN(": A_NOT_NEST,
        "ON(": O_NOT_NEST,
        "XN(": X_NOT_NEST,
        "R": R,
        "S": S,
        "=": assign,
        "FP": FP,
        "FN": FN,
        "JC": JC,
        "BLD": BLD,
        "CU": CU,
        "CD": CD,
        "L": L,
        "NOP": NOP,
        "BTI": BTI,
        "T": T,
        ")": CLOSE_NEST,
    }