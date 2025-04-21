# Build

```
cccc main.cpp
```


# Run

Start LLDB and load the target, then we can observe:

1. `foo.h` don't have a line table (because it's not a compilation unit by itself).
2. The lines in `foo.h` are inlined into `main.cpp`.


```
% lldb a.out
(lldb) target create "a.out"
Current executable set to '/Users/<username>/demo/header/a.out' (arm64).


(lldb) image dump line-table foo.h
warning: No source filenames matched 'foo.h'.
error: no source filenames matched any command arguments

(lldb) image dump line-table main.cpp
Line table for /Users/<username>/demo/header/main.cpp in `a.out
0x0000000100003ee8: /Users/<username>/demo/header/main.cpp:3
0x0000000100003ef8: /Users/<username>/demo/header/main.cpp:4:11
0x0000000100003efc: /Users/<username>/demo/header/main.cpp:4:7
0x0000000100003f04: /Users/<username>/demo/header/main.cpp:7:15
0x0000000100003f08: /Users/<username>/demo/header/main.cpp:7:7
0x0000000100003f0c: /Users/<username>/demo/header/main.cpp:9:10
0x0000000100003f10: /Users/<username>/demo/header/main.cpp:9:14
0x0000000100003f14: /Users/<username>/demo/header/main.cpp:9:12
0x0000000100003f18: /Users/<username>/demo/header/main.cpp:9:3
0x0000000100003f24: /Users/<username>/demo/header/foo.h:3
0x0000000100003f2c: /Users/<username>/demo/header/foo.h:4:9
0x0000000100003f34: /Users/<username>/demo/header/foo.h:5:9
0x0000000100003f38: /Users/<username>/demo/header/foo.h:6:12
0x0000000100003f40: /Users/<username>/demo/header/foo.h:6:14
0x0000000100003f44: /Users/<username>/demo/header/foo.h:6:21
0x0000000100003f48: /Users/<username>/demo/header/foo.h:6:19
0x0000000100003f4c: /Users/<username>/demo/header/foo.h:6:5
0x0000000100003f54: /Users/<username>/demo/header/foo.h:9
0x0000000100003f60: /Users/<username>/demo/header/foo.h:10:9
0x0000000100003f68: /Users/<username>/demo/header/foo.h:11:9
0x0000000100003f6c: /Users/<username>/demo/header/foo.h:12:12
0x0000000100003f74: /Users/<username>/demo/header/foo.h:12:14
0x0000000100003f78: /Users/<username>/demo/header/foo.h:12:21
0x0000000100003f7c: /Users/<username>/demo/header/foo.h:12:19
0x0000000100003f80: /Users/<username>/demo/header/foo.h:12:5
0x0000000100003f88: /Users/<username>/demo/header/foo.h:12:5
```
