# Build
```
cccc -c -gsplit-dwarf main.cpp -o main.o
/opt/llvm/bin/llvm-dwp main.dwo -o main.dwp
cccc main.o
```

# Debug

```
lldb a.out

(lldb) image list
[  0] 2376ED89 0x0000000000000000 /home/royshi/demo/split_dwarf/a.out

(lldb) image dump separate-debug-info
Symbol file: /home/royshi/demo/split_dwarf/a.out
Type: "dwo"
Dwo ID             Err Dwo Path
------------------ --- -----------------------------------------
0x19833a0bad5e2d66     /home/royshi/demo/split_dwarf/main.dwo
```

