# lldb_demos
A series of demos when learning and working with LLDB.

For the demos which includes a python script to print debug info requets from LLDB, type the following commands to set up the script.

``````
defaults delete com.apple.DebugSymbols
defaults write com.apple.DebugSymbols DBGShellCommands <full-path-to-script.py>
``````


## simple

A simple example of how to compile a hello world program and how to use LLDB to debug it.


## class

Set breakpoints by class and method names.


## dylib

LLDB request dsyms for dylibs at target creation time.


## pull_dsym

A shell script can be used to resolve UUIDs into dsym files when LLDB requests such dsym files.

Ref: https://lldb.llvm.org/use/symbols.html


## load_at_breakpoint

LLDB does NOT request dsyms when a breakpoint is set, nor when a breakpoint is triggered.
