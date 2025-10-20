# One-Level Template

## Use *classic* linker
```
cccc -c one.cpp
cccc one.o
dsymutil -o a.out.dSYM a.out
dddd a.out.dSYM
lldb a.out -o "b one.cpp:10" -o "r" -o "p barInt" -o "quit"
```

The printed DWARF contains two `typedef` DIE's:
1. First `BarInt` which is a `typedef` of `Foo<int>`.
2. Second `BarInt` which is a `typedef` of the first `BarInt`.

LLDB can print `BarInt` as the type:
```
(lldb) p barInt
(BarInt)  {}
```

## Use *parallel* linker
```
cccc -c one.cpp
cccc one.o
dsymutil --linker=parallel -o a.out.dSYM a.out
dddd a.out.dSYM
lldb a.out -o "b one.cpp:10" -o "r" -o "p barInt" -o "quit"
```

The printed DWARF contains one `typedef` DIE:
1. `BarInt` which is a `typedef` of itself.

LLDB crashes when resolving this type:
```
(lldb) p barInt
zsh: illegal hardware instruction  lldb a.out -o "b one.cpp:10" -o "r" -o "p barInt" -o "quit"
```


# Two-Level Template

## Without indirection typedef
```
cccc -c -ggdb two.cpp
cccc two.o
dsymutil -o a.out.dSYM a.out
dddd a.out.dSYM
lldb a.out -o "b two.cpp:10" -o "r" -o "p fooBarInt" -o "quit"
```

The printed DWARF contains no `typedef` DIE.

LLDB can print `BarInt` as the type:
```
(lldb) p fooBarInt
(Foo<Foo<int> >)  {}
```
