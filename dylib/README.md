# Setup

Need the following setup in macOS:
```
defaults delete com.apple.DebugSymbols
defaults write com.apple.DebugSymbols DBGShellCommands <path-to-repo>/dylib/print_requests.py
```

# Build dylib and main program

```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc main.cpp foo.dylib
```

# Run the program

```
./a.out
echo $?
```

Expect to see
```
123
```
