# Overview

This example demonstrates LLDB's behavior when accessing properties in Objective-C code from Swift code.


# Commands to try

Set a breakpoint in `main.swift` at the line `print("Hello, World!")`, hit the breakpoint, then try the following in LLDB:

```
# Print a non-`direct` property
(lldb) po response.caption

# Print the inner property of a non-`direct` property
(lldb) po response.comments.first?.user

# Print a `direct` property
(lldb) po response.quickResponseEmojis

# Print the inner `direct` property of a `direct` property
(lldb) po response.quickResponseEmojis?.first?.emoji
```


# Notes

Tested on Xcode 16.0.
