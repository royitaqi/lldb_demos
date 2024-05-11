# Setup

```
cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
dddd=dwarfdump
dddddl='dwarfdump --debug-line'
```

Build LLDB with Roy's logging code: https://github.com/royitaqi/llvm-project/tree/my-logs


# Run

Compile and run:
```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc -dynamiclib bar.cpp -o bar.dylib
cccc main.cpp foo.dylib bar.dylib not_inline.cpp
./a.out
echo $?
```

Start LLDB:
```
lldb
(lldb) log enable lldb roy
(lldb) log enable lldb symbol
(lldb) settings set target.preload-symbols false
(lldb) settings set target.inline-breakpoint-strategy headers
(lldb) target create a.out
(lldb) br set --file inline_for_foo.h --line 2
```

Example output:
```
(lldb) br set --file inline_for_foo.h --line 2
            BreakpointResolver::ResolveBreakpoint() : Resolving breakpoint
                  SearchFilter::DoModuleIteration() : Iterating module a.out
       BreakpointResolverFileLine::SearchCallback() : Iterating CU main.cpp
                     SearchFilter::CompUnitPasses() : Hard-coded pass
       BreakpointResolverFileLine::SearchCallback() : Iterating CU not_inline.cpp
                     SearchFilter::CompUnitPasses() : Hard-coded pass
                  SearchFilter::DoModuleIteration() : Iterating module dyld
                  SearchFilter::DoModuleIteration() : Iterating module foo.dylib
       BreakpointResolverFileLine::SearchCallback() : Iterating CU foo.cpp
                     SearchFilter::CompUnitPasses() : Hard-coded pass
 Parsing symbol table for foo.dylib
 Parsing 48 bytes of dyld trie data
           Module::ResolveSymbolContextForAddress() : Found matching symbol get_foo_ret() for address 0xf88
           Module::ResolveSymbolContextForAddress() : Found matching symbol get_foo_ret() for address 0xf8c
           Module::ResolveSymbolContextForAddress() : Found matching symbol get_foo_ret() for address 0xf88
                  SearchFilter::DoModuleIteration() : Iterating module bar.dylib
       BreakpointResolverFileLine::SearchCallback() : Iterating CU bar.cpp
                     SearchFilter::CompUnitPasses() : Hard-coded pass
                  SearchFilter::DoModuleIteration() : Iterating module libc++.1.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libSystem.B.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libc++abi.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libcache.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libcommonCrypto.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libcompiler_rt.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libcopyfile.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libcorecrypto.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libdispatch.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libdyld.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libkeymgr.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libmacho.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libquarantine.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libremovefile.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_asl.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_blocks.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_c.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_collections.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_configuration.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_containermanager.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_coreservices.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_darwin.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_darwindirectory.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_dnssd.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_eligibility.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_featureflags.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_info.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_m.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_malloc.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_networkextension.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_notify.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_sandbox.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_sanitizers.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_secinit.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_kernel.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_platform.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_pthread.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_symptoms.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libsystem_trace.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libunwind.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libxpc.dylib
                  SearchFilter::DoModuleIteration() : Iterating module libobjc.A.dylib
                  SearchFilter::DoModuleIteration() : Iterating module liboah.dylib
           Module::ResolveSymbolContextForAddress() : Found matching symbol get_foo_ret() for address 0xf88
Breakpoint 1: where = foo.dylib`get_foo_ret() + 24 [inlined] get_foo_ret_inlined(foo_ret const&) at inline_for_foo.h:4:12, address = 0x0000000000000f88
```
