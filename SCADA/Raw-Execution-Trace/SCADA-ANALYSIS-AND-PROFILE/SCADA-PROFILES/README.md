The analysis in this directory focuses on memory and its associated files. Primarily that comes in the form of memory dumps created by WinDbg and live memory from within WinDbg as well.
Many of the scripts found here (mainly in WinSPS_FunctionProfiles) consume the text log output of WinDbg.
To generate a log, run WinDbg with the following format:
`WinDbgX.exe -logo "path\to\some\file.txt"`


There are also text files related to the disassembly of functions related to the WinSPS PLC Mask that exist without a directory.
# Directory Organization
## *_MemDump
To find the memory dumps associated with a few of these logs, retrieve the files from @europe:/VASE/windbg/MemoryDumps/
## RawText_FunctionProfiles
These are the log files produced by WinDbg as-is. These are typically fed into the python scripts contained in WinSPS_FunctionProfiles.
## WinSPS_FunctionProfiles
Contained are two types of files. The first is the ArgumentProfile_* files which analyze and compile the arguments passed to relevent api calls for certain scenarios. The second is StackProfile_* which in a similar manner comipiles the parent functions on the stack for relevent api calls.
## MemoryChangeAnalysis
In order to determine which memory locations were related to physical space interaction, READWRITE protected memory regions were singled out. They were dumped to text then compared with a previous instance to detect changes.