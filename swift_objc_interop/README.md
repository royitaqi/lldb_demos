# Overview

This example demonstrates LLDB's behavior when accessing properties in Objective-C code from Swift code.


# Breakpoints to set

There are two breakpoints to set: one in Swift, another in Objective-C. Search for "// breakpoint here" in this project to find them, or see file/line below.


# Commands to try in Swift

Set a breakpoint in `main.swift` at the line `print("Hello, World!")`, hit the breakpoint, then try the following in LLDB:

```
# Print a non-`direct` property
(lldb) po response.caption

# Print a non-`direct` property (which is an array)
(lldb) p response.comments
(lldb) po response.comments

# Print the inner property of a non-`direct` property
(lldb) po response.comments.first?.user

# Print a `direct` property (which is an array)
(lldb) po response.quickResponseEmojis

# Print the inner `direct` property of a `direct` property
(lldb) po response.quickResponseEmojis?.first?.emoji
```


# Commands to try in Objective-C

Set a breakpoint in `CommentThread.m` at the line `return self;`, hit the breakpoint, then try the following in LLDB:

```
# Print a `direct` property
(lldb) po self.quickResponseEmojis
(lldb) p self.quickResponseEmojis
(lldb) v self->_quickResponseEmojis

# Print a `direct` property via selector
(lldb) po [self quickResponseEmojis]
(lldb) p [self quickResponseEmojis]
```


# Notes

Tested on Xcode 16.0 and 16.2.
