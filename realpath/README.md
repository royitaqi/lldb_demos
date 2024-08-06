# Build

```
cccc -c symlink/bar.cpp main.cpp
cccc bar.o main.o
./a.out
echo $?
```


# Run *without* realpathing

```
lldb a.out

(lldb) image dump line-table main.cpp
Line table for /Users/royshi/demo/realpath/main.cpp in `a.out
0x0000000100003f60: /Users/royshi/demo/realpath/symlink/foo.h:1
0x0000000100003f64: /Users/royshi/demo/realpath/symlink/foo.h:2:3
0x0000000100003f68: /Users/royshi/demo/realpath/main.cpp:4
0x0000000100003f78: /Users/royshi/demo/realpath/main.cpp:5:11
0x0000000100003f7c: /Users/royshi/demo/realpath/main.cpp:5:7
0x0000000100003f80: /Users/royshi/demo/realpath/main.cpp:6:11
0x0000000100003f84: /Users/royshi/demo/realpath/main.cpp:6:7
0x0000000100003f88: /Users/royshi/demo/realpath/main.cpp:7:10
0x0000000100003f8c: /Users/royshi/demo/realpath/main.cpp:7:14
0x0000000100003f90: /Users/royshi/demo/realpath/main.cpp:7:12
0x0000000100003f94: /Users/royshi/demo/realpath/main.cpp:7:3
0x0000000100003fa0: /Users/royshi/demo/realpath/main.cpp:7:3

(lldb) image dump line-table bar.cpp
Line table for /Users/royshi/demo/realpath/symlink/bar.cpp in `a.out
0x0000000100003f58: /Users/royshi/demo/realpath/symlink/bar.cpp:3
0x0000000100003f5c: /Users/royshi/demo/realpath/symlink/bar.cpp:4:3
0x0000000100003f60: /Users/royshi/demo/realpath/symlink/bar.cpp:4:3

(lldb) b real/bar.cpp:3
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

(lldb) b symlink/bar.cpp:3
Breakpoint 2: where = a.out`bar() + 4 at bar.cpp:4:3, address = 0x0000000100003f5c

(lldb) b real/foo.h:2
Breakpoint 3: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

(lldb) b symlink/foo.h:2
Breakpoint 4: where = a.out`foo() + 4 at foo.h:2:3, address = 0x0000000100003f64
```


# Run *with* realpathing

```
lldb a.out

# Cannot resolve breakpoint when no realpathing is done.
(lldb) b real/foo.h:2
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
(lldb) b real/bar.cpp:3
Breakpoint 2: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

# Can resolve when a valid prefix is provided.
(lldb) settings set target.source-realpath-prefixes "fake/path" "/Users/royshi/demo/realpath/"
(lldb) b real/foo.h:2
Breakpoint 3: where = a.out`foo() + 4 at foo.h:2:3, address = 0x0000000100003f64
(lldb) b real/bar.cpp:3
Breakpoint 4: where = a.out`bar() + 4 at bar.cpp:4:3, address = 0x0000000100003f5c

# Wilecard prefix works
(lldb) settings set target.source-realpath-prefixes ""
(lldb) b real/foo.h:2
Breakpoint 5: where = a.out`foo() + 4 at foo.h:2:3, address = 0x0000000100003f64
(lldb) b real/bar.cpp:3
Breakpoint 6: where = a.out`bar() + 4 at bar.cpp:4:3, address = 0x0000000100003f5c

# Clearing the setting will disable realpathing
(lldb) settings clear target.source-realpath-prefixes
(lldb) b real/foo.h:2
Breakpoint 7: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
(lldb) b real/bar.cpp:3
Breakpoint 8: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

# Stats
(lldb) statistics dump --targets=true --modules=false
{
  ...
  "targets": [
    {
      ...
      "sourceRealpathAttemptCount": 4,
      "sourceRealpathCompatibleCount": 4,
      ...
    }
  ],
  ...
}
```
