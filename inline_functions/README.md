# Setup

(See "Common Setup" in the main `README.md`.)


# Run

Compile and run:
```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc -dynamiclib bar.cpp -o bar.dylib
cccc main.cpp foo.dylib bar.dylib
./a.out
echo $?
```

See that the inline function `getRet` in `inline.h` are compiled into `foo.dylib` and `bar.dylib`:
```
dddddl foo.dylib.dSYM
dddddl bar.dylib.dSYM
```

Set file/line breakpoint and see them get resolved:
```
$ lldb a.out
(lldb) target create "a.out"
Current executable set to '/Users/<username>/demo/inline_functions/a.out' (arm64).
(lldb) br set --file inline_in_header.h --line 2
Breakpoint 1: where = foo.dylib`int getRetInHeader<foo_ret>(foo_ret const&) + 8 at inline_in_header.h:2:12, address = 0x0000000000003f84
(lldb) br set --file inline_in_source.cpp --line 2
Breakpoint 2: where = bar.dylib`int getRetInSource<bar_ret>(bar_ret const&) + 8 at inline_in_source.cpp:2:12, address = 0x0000000000003f84
```

Change settings in LLDB to resolve file/line breakpoints for inline functions ONLY IN HEADER FILES:
```
$ lldb a.out
(lldb) target create "a.out"
Current executable set to '/Users/<username>/demo/inline_functions/a.out' (arm64).
(lldb) settings set target.inline-breakpoint-strategy headers
(lldb) br set --file inline_in_header.h --line 2
Breakpoint 1: where = foo.dylib`int getRetInHeader<foo_ret>(foo_ret const&) + 8 at inline_in_header.h:2:12, address = 0x0000000000003f84
(lldb) br set --file inline_in_source.cpp --line 2
Breakpoint 2: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
```

Change settings in LLDB to NEVER resolve file/line breakpoints for inline functions:
```
$ lldb a.out
(lldb) target create "a.out"
Current executable set to '/Users/<username>/demo/inline_functions/a.out' (arm64).
(lldb) settings set target.inline-breakpoint-strategy never
(lldb) br set --file inline_in_header.h --line 2
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
(lldb) br set --file inline_in_source.cpp --line 2
Breakpoint 2: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
```
