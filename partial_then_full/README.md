# Setup

Need the following setup in macOS:
```
defaults delete com.apple.DebugSymbols
defaults write com.apple.DebugSymbols DBGShellCommands <path-to-repo>/dylib/print_requests.py
```

# Build and strip debug info

```
# Build
cccc -dynamiclib foo.cpp -o foo.dylib
cccc main.cpp foo.dylib

# Strip debug info
rm -rf full stripped
mkdir full stripped
mv a.out.dSYM full
mv foo.dylib.dSYM full
cp -r full/a.out.dSYM/ stripped/a.out.dSYM
cp -r full/foo.dylib.dSYM/ stripped/foo.dylib.dSYM
llvm-objcopy --only-section=__DWARF,__debug_line full/a.out.dSYM/Contents/Resources/DWARF/a.out stripped/a.out.dSYM/Contents/Resources/DWARF/a.out
llvm-objcopy --only-section=__DWARF,__debug_line full/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib stripped/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
ls -l full/a.out.dSYM/Contents/Resources/DWARF/a.out stripped/a.out.dSYM/Contents/Resources/DWARF/a.out full/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib stripped/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
```

```
llvm-objcopy \
  --remove-section=__DWARF,__debug_aranges \
  --remove-section=__DWARF,__debug_info \
  --remove-section=__DWARF,__debug_abbrev \
  --remove-section=__DWARF,__debug_str \
  --remove-section=__DWARF,__apple_names \
  --remove-section=__DWARF,__apple_namespac \
  --remove-section=__DWARF,__apple_types \
  --remove-section=__DWARF,__apple_objc \
  full/a.out.dSYM/Contents/Resources/DWARF/a.out stripped/a.out.dSYM/Contents/Resources/DWARF/a.out
```

```
llvm-objcopy \
  full/a.out.dSYM/Contents/Resources/DWARF/a.out stripped/a.out.dSYM/Contents/Resources/DWARF/a.out
```

# Start debug session

```
: > log.txt
dddd --uuid a.out full/a.out.dSYM stripped/a.out.dSYM foo.dylib full/foo.dylib.dSYM stripped/foo.dylib.dSYM
lldb a.out
```
