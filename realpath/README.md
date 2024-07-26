# Build

```
cccc -c bar.cpp main.cpp
cccc bar.o main.o
./a.out
echo $?
```


# Run *without* realpathing

```
lldb a.out

(lldb) image dump line-table main.cpp
Line table for /Users/royshi/demo/realpath/main.cpp in `a.out
0x0000000100000f60: /Users/royshi/demo/realpath/foo.h:1
0x0000000100000f64: /Users/royshi/demo/realpath/foo.h:2:3
0x0000000100000f70: /Users/royshi/demo/realpath/main.cpp:4
0x0000000100000f7f: /Users/royshi/demo/realpath/main.cpp:5:11
0x0000000100000f84: /Users/royshi/demo/realpath/main.cpp:5:7
0x0000000100000f87: /Users/royshi/demo/realpath/main.cpp:6:11
0x0000000100000f8c: /Users/royshi/demo/realpath/main.cpp:6:7
0x0000000100000f8f: /Users/royshi/demo/realpath/main.cpp:7:10
0x0000000100000f92: /Users/royshi/demo/realpath/main.cpp:7:12
0x0000000100000f95: /Users/royshi/demo/realpath/main.cpp:7:3
0x0000000100000f9b: /Users/royshi/demo/realpath/main.cpp:7:3

(lldb) image dump line-table bar.cpp
Line table for /Users/royshi/demo/realpath/bar.cpp in `a.out
0x0000000100000f50: /Users/royshi/demo/realpath/bar.cpp:3
0x0000000100000f54: /Users/royshi/demo/realpath/bar.cpp:4:3
0x0000000100000f5b: /Users/royshi/demo/realpath/bar.cpp:4:3

(lldb) b realbar.cpp:3
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

(lldb) b bar.cpp:3
Breakpoint 2: where = a.out`bar() + 4 at bar.cpp:4:3, address = 0x0000000100000f54

(lldb) b realfoo.h:2
Breakpoint 3: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.

(lldb) b foo.h:2
Breakpoint 4: where = a.out`foo() + 4 at foo.h:2:3, address = 0x0000000100000f64
```


# Run *with* realpathing

```
lldb a.out

(lldb) b realbar.cpp:3
Breakpoint 1: where = a.out`bar() + 4 at bar.cpp:4:3, address = 0x0000000100000f54

(lldb) b realfoo.h:2
Breakpoint 2: where = a.out`foo() + 4 at foo.h:2:3, address = 0x0000000100000f64
```
