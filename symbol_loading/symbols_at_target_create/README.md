# TL;DR

This tutorial explains why no symbol is loaded for the main executable after `target create` *when a dSYM is available*,
while symbols are loaded *when dSYM is unavailable*.


# Setup

```
alias cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
alias ssss='dsymutil --symtab'
```

NOTE: The LLDB should have [PR #136226](https://github.com/llvm/llvm-project/pull/136226/) and [PR #136236](https://github.com/llvm/llvm-project/pull/136236).
These patches print the number of loaded symbols and prevent symbol loading during such printing.


# Tutorial: main.cpp

## Build two binaries: with dSYM and .o as symbol file, respectively

```
# dSYM
cccc main.cpp -o main_dSYM.out

# .o
cccc main.cpp -c -o main.o
cccc main.o -o main_o.out
```

## Compare symbol count after `target create`

With dSYM, LLDB doesn't load any symbols for the main executable.
```
> lldb
(lldb) target create main_dSYM.out
(lldb) statistics dump
{
  ...
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/symbols_at_target_create/main_dSYM.out",
      "symbolFilePath": "/Users/<username>/demo/symbol_loading/symbols_at_target_create/main_dSYM.out.dSYM/Contents/Resources/DWARF/main_dSYM.out",
      "symbolsLoaded": 0,
    },
    ...
  ],
  ...
}
```


As a comparison, with .o, LLDB will load symbols.
```
> lldb
(lldb) target create main_o.out
(lldb) statistics dump
{
  ...
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/symbols_at_target_create/main_o.out",
      "symbolFileModuleIdentifiers": [
        4366287000
      ],
      "symbolsLoaded": 6,
    },
    ...
  ],
  ...
}
```

`4366287000` is a symbol file module that represent the .o file, which is not printed in the above list.
The 6 symbols are NOT loaded from the .o file, but from the main executable `main_o.out` (see below).


## Why the difference?

The short answer:

1. When a module is loaded, LLDB looks for the *symbol plug-in* which provides the best [*symbol file abilities*](https://github.com/llvm/llvm-project/blob/5c3789811fd5b50df1178e7068efb75c5b359383/lldb/include/lldb/Symbol/SymbolFile.h#L61-L76).
2. A well formed dSYM contains all the necessary information to support **all** abilities. LLDB knows about this without parsing the symbol table.
3. Without a dSYM (or, if the dSYM doesn't contain all the necessary information), LLDB loads the symbol table in order to check what the compile units can support.


The longer answer (at LLDB class level):

1. When LLDB creates a `Target`, it creates the `Module` of the main executable and the `SymbolFile` of that module.
2. LLDB then goes through a list of symbol plug-ins (i.e. subclasses of `SymbolFileCommon`) and chooses the one that provides the best abilities.
3. Two plug-ins are of particular interest here:
    1. `SymbolFileDWARF` represent a single symbol file in DWARF format.
    2. `SymbolFileDWARFDebugMap` represent a symbol file which may have `OSO` entries which point to a list of other symbol files (the compile units), hence "map".
4. When `SymbolFileCommon::GetAbilities` is called to get the abilities of a particular plug-in on a particular symbol file, depending on the plug-in, it goes into `SymbolFileDWARF::CalculateAbilities` or `SymbolFileDWARFDebugMap::CalculateAbilities`, in this order.
5. `SymbolFileDWARF::CalculateAbilities` looks at the DWARF, [checks the availability of different debug sections](https://github.com/llvm/llvm-project/blob/5c3789811fd5b50df1178e7068efb75c5b359383/lldb/source/Plugins/SymbolFile/DWARF/SymbolFileDWARF.cpp#L619-L646), and [returns the abilities](https://github.com/llvm/llvm-project/blob/5c3789811fd5b50df1178e7068efb75c5b359383/lldb/source/Plugins/SymbolFile/DWARF/SymbolFileDWARF.cpp#L676-L681).
6. If the dSYM is well formed (i.e. contains all debug sections), the returned value is 127 (max). This [breaks the loop of finding the best plug-in](https://github.com/llvm/llvm-project/blob/5c3789811fd5b50df1178e7068efb75c5b359383/lldb/source/Symbol/SymbolFile.cpp#L74-L77).
7. However, without a dSYM (or, if the dSYM doesn't provide all abilities), the loop will continue and call `SymbolFileDWARFDebugMap::CalculateAbilities`, where it [loads the symbol table, checks the existence of all compile units, then checks the abilities of the first compile unit](https://github.com/llvm/llvm-project/blob/5c3789811fd5b50df1178e7068efb75c5b359383/lldb/source/Plugins/SymbolFile/DWARF/SymbolFileDWARFDebugMap.cpp#L568-L571).


See stacktraces below.

With dSYM:
```
dyld`start
lldb`main
lldb`Driver::MainLoop
SBDebugger::RunCommandInterpreter
CommandInterpreter::RunCommandInterpreter
Debugger::RunIOHandlers
IOHandlerEditline::Run
CommandInterpreter::IOHandlerInputComplete
CommandInterpreter::HandleCommand
CommandObjectParsed::Execute
CommandObjectTargetCreate::DoExecute
TargetList::CreateTarget
TargetList::CreateTargetInternal
Target::SetExecutableModule
ModuleList::Append
ModuleList::AppendImpl
Target::NotifyModuleAdded
Target::ModulesDidLoad
LoadScriptingResourceForModule
Module::LoadScriptingResourceInTarget
PlatformDarwin::LocateExecutableScriptingResources
Module::GetSymbolFile
SymbolVendor::FindPlugin
SymbolVendorMacOSX::CreateInstance
SymbolVendor::AddSymbolFileRepresentation
SymbolFile::FindPlugin
SymbolFileCommon::GetAbilities
SymbolFileDWARF::CalculateAbilities <--- The stack ends here, because we have a well formed dSYM. This returned 127 (max), thus breaking the loop of getting the best abilities.
```


Without dSYM, below is LLDB's stacktrace when the symbols are loaded:
```
...
SymbolFileCommon::GetAbilities
SymbolFileDWARFDebugMap::CalculateAbilities <--- this is because a previous call to SymbolFileDWARF::CalculateAbilities didn't return 127 (max)
SymbolFileCommon::GetNumCompileUnits
SymbolFileDWARFDebugMap::CalculateNumCompileUnits
SymbolFileDWARFDebugMap::InitOSO
ObjectFile::GetSymtab
ObjectFileMachO::ParseSymtab <--- Symbols are loaded here.
```



# Conclude

In this tutorial, we investigated why symbols are not loaded for the main executable after `target create` when dSYM is available,
and why symbols are loaded when dSYM is unavailable. We learned a bit more about symbol plug-ins, and symbol file abilities.



# BTW

In Linux, there is no such loop to find the best symbol plug-in.
It doesn't even call `Module::GetSymbolFile` to create the symbol file.

Why the difference bewteen macOS and Linux? (Linux also has a second plug-in called `SymbolFileDWARFDwo`. Why not loop to find the best?)

```
lldb`_start
__libc_start_main_impl
__libc_start_call_main
lldb`main
Driver::MainLoop
SBDebugger::RunCommandInterpreter
CommandInterpreter::RunCommandInterpreter
Debugger::RunIOHandlers
IOHandlerEditline::Run
CommandInterpreter::IOHandlerInputComplete
CommandInterpreter::HandleCommand
CommandObjectParsed::Execute
CommandObjectTargetCreate::DoExecute
TargetList::CreateTarget
TargetList::CreateTargetInternal
Target::SetExecutableModule
ModuleList::Append
ModuleList::AppendImpl
Target::NotifyModuleAdded
Target::ModulesDidLoad
LoadScriptingResourceForModule
Module::LoadScriptingResourceInTarget
Platform::LocateExecutableScriptingResources --- This immediately returns an empty FileSpecList.
```


# Tutorial: example2.cpp

## Build

```
cccc -dynamiclib bar.cpp -o bar.dylib
cccc -dynamiclib foo.cpp bar.dylib -o foo.dylib
cccc example2.cpp foo.dylib -o example2
```


## Observe the number of symbols loaded for each module

```
> lldb
(lldb) target create example2
(lldb) statistics dump
{
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/symbols_at_target_create/example2",
      "symbolFilePath": "/Users/<username>/demo/symbol_loading/symbols_at_target_create/example2.dSYM/Contents/Resources/DWARF/example2",
      "symbolsLoaded": 0
    },
    {
      "path": "foo.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_target_create/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib",
      "symbolsLoaded": 0,
    },
    {
      "path": "bar.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_target_create/bar.dylib.dSYM/Contents/Resources/DWARF/bar.dylib",
      "symbolsLoaded": 0,
    }
  ]
}
```

Same as our understanding in "Tutorial: main.cpp", the symbol tables in all the modules have not be loaded yet.
