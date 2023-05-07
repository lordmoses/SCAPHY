https://www.visualbasicplanet.info/debugging-applications/listing-81-windbg-wt-output.html

https://jpassing.com/2008/05/10/trace-and-watch-data-how-does-it-work/


The beginning part of the output (displaying the hierarchical tree) is the call information. 
In front of each call, WinDBG displays three numbers. - 
- The first number is the assembly instruction count that the function executed before calling the next function. 
- The second number is undocumented, but looks to be a running total of assembly-language instructions executed in the tracing on returns. 
- The final number in brackets is the current nesting level for the hierarchical tree.

The second portion of the output is a summary display, which is a little more understandable. In addition to providing a summary of each function called, it shows the function call count as well as 
- the minimum number of assembly-language instructions called in an invocation, 
- the maximum number of assembly-language instructions called in an invocation, and 
-  the average number of instructions called. 
The final lines of the summary display show how many system calls occurred.

As you can imagine, using the wt command can produce a huge amount of output and can really slow down your application since each line of output requires a couple of cross process transitions between the debugger and debuggee to get the information. If you want to see the all-important summary information, passing -nc as a parameter to wt will suppress the hierarchy. Of course, if you're interested in just the hierarchy, pass -ns as the parameter. To see the return value register (eax in x86 assembly language), use the -or parameter; and to see the address, source, and line information (if available) for each call, use the -oa parameter. The final parameter is -l, which allows you to set the maximum depth of calls to display. Using -l can be helpful when you want to see the high points of what's executed or keep the display to just the functions in your program.
