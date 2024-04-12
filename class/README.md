# Run

```
cccc main.cpp foo.cpp
lldb a.out
```

In LLDB, breakpoints can be set in multiple ways for the `Foo::GetValue()` function:
```
(lldb) b Foo::GetValue
(lldb) br s -f foo.cpp -l 8
(lldb) br s -f foo.cpp -n GetValue
```
