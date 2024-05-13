# Setup

```
cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
```

Build LLDB with Roy's logging code: https://github.com/royitaqi/llvm-project/tree/my-logs


# Run

Compile and run:
```
cccc main.cpp
./a.out
echo $?
```

Start LLDB and setup:
```
log enable lldb roy
log enable lldb symbol
settings set target.preload-symbols false
settings set target.inline-breakpoint-strategy headers
```

Create target:
```
(lldb) target create a.out
                            Module::GetObjectFile() : Getting object file for a.out
                            Module::GetSymbolFile() : Getting symbol file for a.out
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /Users/royshi/demo/settings__preload_symbols/a.out.dSYM/Contents/Resources/DWARF/a.out
                            Module::GetObjectFile() : Getting object file for dyld
                            Module::GetObjectFile() : Getting object file for libc++.1.dylib
                            Module::GetObjectFile() : Getting object file for libSystem.B.dylib
                            Module::GetObjectFile() : Getting object file for libc++abi.dylib
                            Module::GetObjectFile() : Getting object file for libcache.dylib
                            Module::GetObjectFile() : Getting object file for libcommonCrypto.dylib
                            Module::GetObjectFile() : Getting object file for libcompiler_rt.dylib
                            Module::GetObjectFile() : Getting object file for libcopyfile.dylib
                            Module::GetObjectFile() : Getting object file for libcorecrypto.dylib
                            Module::GetObjectFile() : Getting object file for libdispatch.dylib
                            Module::GetObjectFile() : Getting object file for libdyld.dylib
                            Module::GetObjectFile() : Getting object file for libkeymgr.dylib
                            Module::GetObjectFile() : Getting object file for libmacho.dylib
                            Module::GetObjectFile() : Getting object file for libquarantine.dylib
                            Module::GetObjectFile() : Getting object file for libremovefile.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_asl.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_blocks.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_c.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_collections.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_configuration.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_containermanager.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_coreservices.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_darwin.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_darwindirectory.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_dnssd.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_eligibility.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_featureflags.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_info.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_m.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_malloc.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_networkextension.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_notify.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_sandbox.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_sanitizers.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_secinit.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_kernel.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_platform.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_pthread.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_symptoms.dylib
                            Module::GetObjectFile() : Getting object file for libsystem_trace.dylib
                            Module::GetObjectFile() : Getting object file for libunwind.dylib
                            Module::GetObjectFile() : Getting object file for libxpc.dylib
                            Module::GetObjectFile() : Getting object file for libobjc.A.dylib
                            Module::GetObjectFile() : Getting object file for liboah.dylib
                            Module::GetObjectFile() : Getting object file for (null)
                            Module::GetSymbolFile() : Getting symbol file for dyld
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/dyld
 Parsing symbol table for dyld
 Parsing 120 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libc++.1.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/libc++.1.dylib
 Parsing symbol table for libc++.1.dylib
 Parsing 69976 bytes of dyld trie data.
                            Module::GetSymbolFile() : Getting symbol file for libSystem.B.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/libSystem.B.dylib
 Parsing symbol table for libSystem.B.dylib
 Parsing 120 bytes of dyld trie datalib...
                            Module::GetSymbolFile() : Getting symbol file for libc++abi.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/libc++abi.dylib
 Parsing symbol table for libc++abi.dylib
 Parsing 7344 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libcache.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libcache.dylib
 Parsing symbol table for libcache.dylib
 Parsing 680 bytes of dyld trie data...
                            Module::GetSymbolFile() : Getting symbol file for libcommonCrypto.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libcommonCrypto.dylib
 Parsing symbol table for libcommonCrypto.dylib
 Parsing 4336 bytes of dyld trie data.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libcompiler_rt.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libcompiler_rt.dylib
 Parsing symbol table for libcompiler_rt.dylib
 Parsing 1168 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libcopyfile.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libcopyfile.dylib
 Parsing symbol table for libcopyfile.dylib
 Parsing 232 bytes of dyld trie datalib...
                            Module::GetSymbolFile() : Getting symbol file for libcorecrypto.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libcorecrypto.dylib
 Parsing symbol table for libcorecrypto.dylib
 Parsing 22952 bytes of dyld trie datalib...
                            Module::GetSymbolFile() : Getting symbol file for libdispatch.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libdispatch.dylib
 Parsing symbol table for libdispatch.dylib
 Parsing 8440 bytes of dyld trie dataib...
                            Module::GetSymbolFile() : Getting symbol file for libdyld.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libdyld.dylib
 Parsing symbol table for libdyld.dylib
 Parsing 4768 bytes of dyld trie data.
                            Module::GetSymbolFile() : Getting symbol file for libkeymgr.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libkeymgr.dylib
 Parsing symbol table for libkeymgr.dylib
 Parsing 360 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libmacho.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libmacho.dylib
 Parsing symbol table for libmacho.dylib
 Parsing 2352 bytes of dyld trie data..
                            Module::GetSymbolFile() : Getting symbol file for libquarantine.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libquarantine.dylib
 Parsing symbol table for libquarantine.dylib
 Parsing 1576 bytes of dyld trie dataylib...
                            Module::GetSymbolFile() : Getting symbol file for libremovefile.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libremovefile.dylib
 Parsing symbol table for libremovefile.dylib
 Parsing 248 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_asl.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_asl.dylib
 Parsing symbol table for libsystem_asl.dylib
 Parsing 4160 bytes of dyld trie dataylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_blocks.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_blocks.dylib
 Parsing symbol table for libsystem_blocks.dylib
 Parsing 408 bytes of dyld trie dataks.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_c.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_c.dylib
 Parsing symbol table for libsystem_c.dylib
 Parsing 21544 bytes of dyld trie datab...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_collections.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_collections.dylib
 Parsing symbol table for libsystem_collections.dylib
 Parsing 960 bytes of dyld trie dataections.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_configuration.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_configuration.dylib
 Parsing symbol table for libsystem_configuration.dylib
 Parsing 896 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_containermanager.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_containermanager.dylib
 Parsing symbol table for libsystem_containermanager.dylib
 Parsing 8432 bytes of dyld trie datainermanager.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_coreservices.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_coreservices.dylib
 Parsing symbol table for libsystem_coreservices.dylib
 Parsing 440 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_darwin.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_darwin.dylib
 Parsing symbol table for libsystem_darwin.dylib
 Parsing 1776 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_darwindirectory.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_darwindirectory.dylib
 Parsing symbol table for libsystem_darwindirectory.dylib
 Parsing 64 bytes of dyld trie datawindirectory.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_dnssd.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_dnssd.dylib
 Parsing symbol table for libsystem_dnssd.dylib
 Parsing 1296 bytes of dyld trie data.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_eligibility.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_eligibility.dylib
 Parsing symbol table for libsystem_eligibility.dylib
 Parsing 264 bytes of dyld trie dataibility.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_featureflags.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_featureflags.dylib
 Parsing symbol table for libsystem_featureflags.dylib
 Parsing 56 bytes of dyld trie datatureflags.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_info.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_info.dylib
 Parsing symbol table for libsystem_info.dylib
 Parsing 8040 bytes of dyld trie datadylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_m.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_m.dylib
 Parsing symbol table for libsystem_m.dylib
 Parsing 5536 bytes of dyld trie dataib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_malloc.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_malloc.dylib
 Parsing symbol table for libsystem_malloc.dylib
 Parsing 3096 bytes of dyld trie datac.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_networkextension.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_networkextension.dylib
 Parsing symbol table for libsystem_networkextension.dylib
 Parsing 4896 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_notify.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_notify.dylib
 Parsing symbol table for libsystem_notify.dylib
 Parsing 440 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_sandbox.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_sandbox.dylib
 Parsing symbol table for libsystem_sandbox.dylib
 Parsing 3680 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_sanitizers.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_sanitizers.dylib
 Parsing symbol table for libsystem_sanitizers.dylib
 Parsing 1000 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_secinit.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_secinit.dylib
 Parsing symbol table for libsystem_secinit.dylib
 Parsing 176 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libsystem_kernel.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_kernel.dylib
 Parsing symbol table for libsystem_kernel.dylib
 Parsing 31448 bytes of dyld trie data.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_platform.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_platform.dylib
 Parsing symbol table for libsystem_platform.dylib
 Parsing 3048 bytes of dyld trie dataorm.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_pthread.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_pthread.dylib
 Parsing symbol table for libsystem_pthread.dylib
 Parsing 4608 bytes of dyld trie dataad.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_symptoms.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_symptoms.dylib
 Parsing symbol table for libsystem_symptoms.dylib
 Parsing 296 bytes of dyld trie datatoms.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libsystem_trace.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libsystem_trace.dylib
 Parsing symbol table for libsystem_trace.dylib
 Parsing 3512 bytes of dyld trie data.dylib...
                            Module::GetSymbolFile() : Getting symbol file for libunwind.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libunwind.dylib
 Parsing symbol table for libunwind.dylib
 Parsing 1064 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libxpc.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/system/libxpc.dylib
 Parsing symbol table for libxpc.dylib
 Parsing 17560 bytes of dyld trie data
                            Module::GetSymbolFile() : Getting symbol file for libobjc.A.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/libobjc.A.dylib
 Parsing symbol table for libobjc.A.dylib
 Parsing 9184 bytes of dyld trie data...
                            Module::GetSymbolFile() : Getting symbol file for liboah.dylib
        SymbolVendor::AddSymbolFileRepresentation() : Adding symbol file /usr/lib/liboah.dylib
 Parsing symbol table for liboah.dylib
 Parsing 1296 bytes of dyld trie data
Current executable set to '/Users/royshi/demo/settings__preload_symbols/a.out' (arm64).
```


Set file/line breakpoint:
```
(lldb) br set --file main.cpp --line 10
            BreakpointResolver::ResolveBreakpoint() : Resolving breakpoint
       BreakpointResolverFileLine::SearchCallback() : Iterating CU main.cpp
    SearchFilterByModuleListAndCU::CompUnitPasses() : Testing CU main.cpp
 Parsing symbol table for a.out
 Parsing 72 bytes of dyld trie data
           Module::ResolveSymbolContextForAddress() : Found matching symbol main for address 0x100003f70
           Module::ResolveSymbolContextForAddress() : Found matching symbol main for address 0x100003f74
           Module::ResolveSymbolContextForAddress() : Found matching symbol main for address 0x100003f70
           Module::ResolveSymbolContextForAddress() : Found matching symbol main for address 0x100003f70
           Module::ResolveSymbolContextForAddress() : Found matching symbol main for address 0x100003f70
Breakpoint 1: where = a.out`main + 16 at main.cpp:10:11, address = 0x0000000100003f70
(lldb)
```
