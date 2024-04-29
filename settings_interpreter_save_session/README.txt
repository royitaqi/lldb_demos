# Setup



# Run

Build:
```
cccc main.cpp
lldb
```

In LLDB:
```
settings set interpreter.save-session-on-quit true
settings set interpreter.save-session-directory .
target create a.out
b main
r
n
po a
```
