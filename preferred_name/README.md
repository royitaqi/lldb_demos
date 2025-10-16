# Run

## Use *classic* linker
```
cccc -c main.cpp
cccc main.o
dsymutil --verify-dwarf=all -o a.out.dSYM a.out
dddd a.out.dSYM
lldb a.out -o "b main.cpp:10" -o "r" -o "p barInt" -o "quit"
```

## Use *parallel* linker
```
cccc -c main.cpp
cccc main.o
dsymutil --verify-dwarf=all --linker=parallel -o a.out.dSYM a.out
dddd a.out.dSYM
lldb a.out -o "b main.cpp:10" -o "r" -o "p barInt" -o "quit"
```
