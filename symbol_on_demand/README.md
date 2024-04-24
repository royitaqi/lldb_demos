# Setup

Need the following setup in macOS:
```
% cat > ~/.lldbinit
settings set symbols.load-on-demand true
log enable -f /tmp/ondemand.txt lldb on-demand
```

# Hydration triggered by name breakpoint

```
cccc main.cpp
lldb a.out
(lldb) b main
```

Observe the log being printed in `/tmp/ondemand.txt``.
For example, see `ondemand_1.txt` in this folder.

At the time of `lldb a.out`, symbols are not loaded.
Symbols are then loaded (hydrated) by `b main`.


# Hydration triggered by file/line breakpoint

```
cccc main.cpp
lldb a.out
(lldb) b -f main.cpp -l 14
```

Observe the log being printed in `/tmp/ondemand.txt``.
For example, see `ondemand_2.txt` in this folder.

At the time of `lldb a.out`, symbols are not loaded.
Symbols are then loaded (hydrated) by `b -f main.cpp -l 14`.
