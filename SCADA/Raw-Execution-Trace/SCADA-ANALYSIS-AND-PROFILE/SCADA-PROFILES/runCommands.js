"use strict";
function runCommands()
{
    var ctl = host.namespace.Debugger.Utility.Control;
    var output = ctl.ExecuteCommand("~");
    host.diagnostics.debugLog("***Command output:\n");
    for(var line in output)
    {
        host.diagnostics.debugLog(" ", line, "\n");

    }
    host.diagnostics.debugLog("***Exiting command\n");
}