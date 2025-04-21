# Setup

(See "Common Setup" in the main `README.md`.)


# Run

The command (`image dump separate-debug-info`) doesn't work for dSYMs. So let's use .o files.
```
cccc -c main.cpp
cccc main.o
```

Observe that debug info can be loaded from the .o file:
```
lldb a.out
(lldb) image dump separate-debug-info
Symbol file: /Users/<username>/demo/image_dump__separate_debug_info/a.out
Type: "oso"
Mod Time           Err Oso Path
------------------ --- ---------------------
0x00000000663950ca     /Users/<username>/demo/image_dump__separate_debug_info/main.o
```

Remove the .o file. Observe that now debug info cannot be loaded:
```
mv main.o /tmp
lldb a.out
(lldb) image dump separate-debug-info
Symbol file: /Users/<username>/demo/image_dump__separate_debug_info/a.out
Type: "oso"
Mod Time           Err Oso Path
------------------ --- ---------------------
0x00000000663950ca E   debug map object file "/Users/<username>/demo/image_dump__separate_debug_info/main.o" containing debug info does not exist, debug info will not be loaded
```

Note: For .o files, `image list` will produce the same result, which doesn't point out the .o files which are supposed to be loaded. Overall, `image list` and `image dump separate-debug-info` are complementary. The former tells you which dSYMs are loaded, the latter .o files.
```
(lldb) image list
[  0] 0EF8A7AD-A169-4B5A-8C9B-7DF4B51ACF5B 0x0000000100000000 /Users/<username>/demo/image_dump__separate_debug_info/a.out
[  1] F6DD3EC2-85A4-3AB1-8486-B189CD980EBE 0x00000001800b8000 /usr/lib/dyld
```
