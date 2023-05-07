import re
f = open("MPI_V2_RAW.txt")
out = open("Parsed-MPI_V2.txt", "w")

linesread = 0
printline = ""
# regular expression assumes that the "kn #" function was called after ~.
#example command:
#bm <module name>!<function name> "~.; kn 3; .time; r; g"
#<module name> and <function name> can either be a specific string (ie WS7_S7AG) or a regular expression (ie WS7_*) to match a wide array
#This command sets break points at every function that matches <function name> in the modules that are matched by <module name>
#The string at the end of the command is a list of command to run each time the breakpoint is hit. [~.] gives the current thread information.
#[kn 3] prints the top 3 stack frames at runtime. [.time] prints time information of the runtime environment. [g] automatically continues until the next breakpoint.
#The module name can be changed to any other module and the export function wildcard can be changed to anything else as well (like "*Read*" for read functions)

#output is formated as follows
#<thread num>: <Called function> <- <Callee> [<Timestamp>]

for line in f.readlines():
    linesread += 1
    if(line.find(".") == 0):
        m = re.search("^.\s+[0-9]{1,2}", line) #grab thread number
        if(m != None):
            printline = m.group()[2:]
    if(line.find("00") == 0): #the current function
        m = re.search("\S*!\S*", line) #grab function that had the breakpoint
        if(m != None):
            printline = printline + ": " + m.group()
    if(line.find('01') == 0): #the format of the kn function places the caller of 00 at 01
        m = re.search("\S*!\S*", line) #grab calling function
        if(m != None):
            printline = printline + " <- " + m.group()
        else:
            m = re.search("\S*$", line) #to catch lack of function on the line
            printline = printline + " <- " + m.group()
    if(line.find("Process Uptime") == 0):
        m = re.search("\d+:\d+:\d+\.\d+", line) #match the time stamp
        if(m != None):
            printline = printline + " [" + m.group() + "]\n"
            print(printline)
            out.write(printline)

#add functionality to parse out printed registers
#analyze argument passing
