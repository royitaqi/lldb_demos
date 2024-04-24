# Run

Build.
Remove dsym.
Start LLDB.
```
cccc main.cpp
rm -rf a.out.dSYM
lldb a.out
```

A list of dsym requests will be appended to `log.txt`.
In a different console, clear the file so that later requests are obvious.
```
: > log.txt
```

In LLDB, set breakpoints, then run process through the breakpoints.
```
(lldb) b main
(lldb) b foo
(lldb) r      <-- will stop at main()
(lldb) c      <-- will stop at foo()
(lldb) c      <-- will terminate
```

Observe that `log.txt` is empty. I.e. no dsym request is made after the initial attempt.
