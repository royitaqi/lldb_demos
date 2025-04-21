# TL;DR

This tutorial inspects what symbols are loaded before/at main, and why.


# Setup

```
alias cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
alias ssss='dsymutil --symtab'
```

NOTE: The LLDB should have [PR #136226](https://github.com/llvm/llvm-project/pull/136226/) and [PR #136236](https://github.com/llvm/llvm-project/pull/136236).
These patches print the number of loaded symbols and prevent symbol loading during such printing.


# Tutorial: example2.cpp

## Build

```
cccc -dynamiclib bar.cpp -o bar.dylib
cccc -dynamiclib foo.cpp bar.dylib -o foo.dylib
cccc main.cpp foo.dylib
```


## Observe the number of symbols loaded at main

```
> lldb
(lldb) target create a.out
(lldb) b main
(lldb) run
Process 51230 stopped
(lldb) statistics dump
{
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/symbols_at_main/a.out",
      "symbolFilePath": "/Users/<username>/demo/symbol_loading/symbols_at_main/a.out.dSYM/Contents/Resources/DWARF/a.out",
      "symbolsLoaded": 5,
    },
    {
      "path": "foo.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_main/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib",
      "symbolsLoaded": 4,
    },
    {
      "path": "bar.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_main/bar.dylib.dSYM/Contents/Resources/DWARF/bar.dylib",
      "symbolsLoaded": 3,
    }
  ]
}
```

## Why the symbols are loaded?

So the symbol tables are loaded for all three modules.

But why? One would imagine that the symbol table for foo.dylib and bar.dylib are not needed until the functions in them are called. Apparently that's not the case.

Debugging LLDB shows that the symbols are loaded when `b main` is executed.
This makes sense, because it's a symbol breakpoint, so LLDB has to load all the symbols to see where `main` is.


## So how about we set the breakpint by file/line?

```
> lldb
(lldb) target create a.out
(lldb) b main.cpp:3
(lldb) statistics dump
{
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/symbols_at_main/a.out",
      "symbolFilePath": "/Users/<username>/demo/symbol_loading/symbols_at_main/a.out.dSYM/Contents/Resources/DWARF/a.out",
      "symbolsLoaded": 5,
    },
    {
      "path": "foo.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_main/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib",
      "symbolsLoaded": 0,
    },
    {
      "path": "bar.dylib",
      "symbolFilePath": "/System/Volumes/Data/Users/<username>/demo/symbol_loading/symbols_at_main/bar.dylib.dSYM/Contents/Resources/DWARF/bar.dylib",
      "symbolsLoaded": 0,
    }
  ]
}
```

Observe that the symbols loaded for `foo.dylib` and `bar.dylib` are now zero (0), which makes sense.

Why symbols are loaded for `a.out`? It's because LLDB resolves the *symbol contexts* in order to find a list of possible locations that can be resolved. Below is the stacktrace. See `CompileUnit::ResolveSymbolContext`.

```
dyld`start
lldb`main
Driver::MainLoop
SBDebugger::RunCommandInterpreter
CommandInterpreter::RunCommandInterpreter
Debugger::RunIOHandlers
IOHandlerEditline::Run
CommandInterpreter::IOHandlerInputComplete
CommandInterpreter::HandleCommand
CommandObjectRaw::Execute
CommandObjectRegexCommand::DoExecute
CommandInterpreter::HandleCommand
CommandObjectParsed::Execute
CommandObjectBreakpointSet::DoExecute
Target::CreateBreakpoint
Target::CreateBreakpoint
Target::AddBreakpoint
Breakpoint::ResolveBreakpoint
BreakpointResolver::ResolveBreakpoint
SearchFilter::Search
SearchFilter::DoModuleIteration
BreakpointResolverFileLine::SearchCallback
CompileUnit::ResolveSymbolContext
Address::CalculateSymbolContext
Module::ResolveSymbolContextForAddress
SymbolFileCommon::GetSymtab
ObjectFile::GetSymtab
ObjectFileMachO::ParseSymtab
```

## When is the symbols loaded for `foo.dylib` and `bar.dylib`?


The symbols of `foo.dylib` are loaded when `run`, *before* hitting the breakpoint in `main`.
```
> lldb
(lldb) target create a.out
(lldb) b main.cpp:3
(lldb) run
```

The stacktrace:
```
libsystem_pthread.dylib`_pthread_start
HostThreadMacOSX::ThreadCreateTrampoline
HostNativeThreadBase::ThreadCreateTrampoline
Process::StartPrivateStateThread
Process::RunPrivateStateThread
Process::HandlePrivateEvent
Process::ShouldBroadcastEvent
ThreadList::ShouldStop
Thread::ShouldStop
StopInfoBreakpoint::ShouldStopSynchronous
BreakpointSite::ShouldStop
BreakpointLocationCollection::ShouldStop
BreakpointLocation::ShouldStop
BreakpointLocation::InvokeCallback
Breakpoint::InvokeCallback
BreakpointOptions::InvokeCallback
DynamicLoaderMacOS::NotifyBreakpointHit --- the DYLD notification breakpoint (on "lldb_image_notifier") has been hit
DynamicLoaderMacOS::AddBinaries
DynamicLoaderDarwin::AddModulesUsingPreloadedModules
Target::ModulesDidLoad
ProcessGDBRemote::ModulesDidLoad
GDBRemoteCommunicationClient::ServeSymbolLookups --- symbol name is "dispatch_queue_offsets"
ModuleList::FindSymbolsWithNameAndType --- this loops through all modules to find the symbol
Module::FindSymbolsWithNameAndType
Module::GetSymtab
SymbolFileOnDemand::GetSymtab
SymbolFileCommon::GetSymtab
ObjectFile::GetSymtab
ObjectFileMachO::ParseSymtab
```

The two dylibs appear in `a.out`'s *load commands* (this is on macOS) - they are `a.out`'s static dependencies (though dynamically linked).
So the dylibs have to be loaded before the program is executed.
The above stacktrace suggests that the symbol tables are parsed when the dylibs are loaded - LLDB was notified that a dylib is being (or, has been) loaded, so LLDB loads the debug info for that dylib (so that we can debug).

All the above make sense.

**But why are the symbol tables of `foo.dylib` and `bar.dylib` parsed in order to resolve this symbol called "dispatch_queue_offsets"?** This is clearly a system function, and doesn't belong to the helloworld program.
