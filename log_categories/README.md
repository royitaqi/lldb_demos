# TL;DR

* `log enable` will print logs to console.
* Printed logs will __not__ be captured by `settings interpreter.save-session-on-quit`.


# Run

```
cccc foo.cpp main.cpp
lldb
```


## Category: `lldb commands`

(lldb)
```
log enable lldb commands
target create a.out
b main
r
n
p a
settings set interpreter.save-session-on-quit true
settings set  interpreter.save-session-directory .
^D
```

See example output in `lldb_session_example_lldb_commands.log`.

Short example:
```
(lldb) p a
 Processing command: p a
 HandleCommand, cmd_obj : 'dwim-print'
 HandleCommand, (revised) command_string: 'dwim-print -- a'
 HandleCommand, wants_raw_input:'True'
 HandleCommand, command line after removing command name(s): '-- a'
 HandleCommand, command succeeded
```

Log contains:
* Input command
* Command object / formal name
* Full command string
* Full command string without command name
* Success/failure of the command
