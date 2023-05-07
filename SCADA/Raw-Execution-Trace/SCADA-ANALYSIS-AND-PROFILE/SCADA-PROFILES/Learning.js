"use strict";

function initializeScript()
{
    return [new host.apiVersionSupport(1, 7)];
}

function invokeScript()
{
    //
    // Insert your script content here.  This method will be called whenever the script is
    // invoked from a client.
    //
    // See the following for more details:
    //
    //     https://aka.ms/JsDbgExt
    //
    host.diagnostics.debugLog("Test");
    var ctl = host.namespace.Debugger.Utility.Control
    var cmd = "~";
    var output = ctl.ExecuteCommand(cmd);
    for(var line in output)
    {
        host.diagnostics.debugLog(line + "\n");

    }
}
