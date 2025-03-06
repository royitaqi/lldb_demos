# Demos
A series of demos when learning and working with LLDB.
See the `Common Setup` section below.

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


## inline_functions

* Inline functions are compiled into each binary's `.debug_lines` table.
* `settings set target.inline-breakpoint-strategy <always|headers|never>` to control whether or not to resolve inline functions for source and header files.


## breakpoint_resolution_file_line

Logic to resolve file/line breakpoints:
* Iterate through all CU
  * Find matching CUs by looking at *both*:
    * The settings `target.inline-breakpoint-strategy`
    * The file list in the *line table prologue*
  * If a CU matches, load/look at its *line table content* to find the address
  * Load/look at its *symbol table* to find the function that contains the address


## settings__preload_symbols

When the setting is off:
```
+--------+-----------------+--------------------+
| Module | Add Symbol File | Parse Symbol Table |
+--------+-----------------+--------------------+
| user   | at attach       | at br set          |
+--------+-----------------+--------------------+
| shared | at attach       | at attach          |
+--------+-----------------+--------------------+
```


## gdb_remote

Use GDB remote logs to understand the interaction between LLDB server and applications.


## realpath

Realpath symlinks when resolving file/line breakpoints.


## swift_objc_interop

Demonstrates LLDB's behavior when accessing properties in Objective-C code from Swift code.


# Common Setup

Command line aliases.
```
cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
dddd=dwarfdump
ddddan='dwarfdump --apple-names'
dddddl='dwarfdump --debug-line'
hhhh='objdump --section-headers'
oooo='otool -lv'
ssss='dsymutil -s'
```

For the demos which includes a python script to print debug info requets from LLDB, type the following commands to set up the script.
``````
defaults delete com.apple.DebugSymbols
defaults write com.apple.DebugSymbols DBGShellCommands <full-path-to-script.py>
``````
