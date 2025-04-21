# Build

```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc main.cpp foo.dylib
```

# Change module UUID while remain the same path

```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc main.cpp foo.dylib
lldb a.out

(lldb) image list
[  0] 1DFB169E-969E-40F9-9F0C-5EB152DB317A 0x0000000100000000 /Users/<username>/demo/module_reload/a.out
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] C1EA50EE-BA2A-4BB7-861C-2A0F018E26A9 0x0000000000000000 foo.dylib
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib
```

Change the value in foo.cpp. Rebuild. Reload.

```
(lldb) file a.out
Current executable set to '/Users/<username>/demo/module_reload/a.out' (arm64).

(lldb) image list
[  0] E84BA4A6-8FA8-44D3-9D08-2C58AF22B5F1 0x0000000100000000 /Users/<username>/demo/module_reload/a.out    <-- UUID changed
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] C771C30C-F114-4C51-BF67-A1F1E98B3ABF 0x0000000000000000 foo.dylib                                 <-- UUID changed
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib
```

Observe that UUID changed for both the main executable (a.out) and the dylib (foo.dylib).


```
(lldb) image list -g
[  0] 1DFB169E-969E-40F9-9F0C-5EB152DB317A 0x0000000100000000 /Users/<username>/demo/module_reload/a.out    <-- old module
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] C1EA50EE-BA2A-4BB7-861C-2A0F018E26A9 0x0000000000000000 foo.dylib                                 <-- old module
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib
[ 46] E84BA4A6-8FA8-44D3-9D08-2C58AF22B5F1 0x0000000100000000 /Users/<username>/demo/module_reload/a.out    <-- new module
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[ 47] C771C30C-F114-4C51-BF67-A1F1E98B3ABF 0x0000000000000000 foo.dylib                                 <-- new module
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
```

Observe that new modules are appended to the global list.
Observe that old modules still exist. This is different from the following, where the old modules will be removed.

Exit LLDB.


# Change module path while remain the same UUID


```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc main.cpp foo.dylib
lldb a.out

(lldb) image list
[  0] 69EC6339-CF21-4926-90DA-6470E1F1DDF9 0x0000000100000000 /Users/<username>/demo/module_reload/a.out
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] 73D51EB5-9335-496C-A95C-D6AEF4ED9C2C 0x0000000000000000 foo.dylib
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib
```


Move `a.out` to the `tmp` subdirectory. Reload.

```
(lldb) file tmp/a.out
Current executable set to '/Users/<username>/demo/module_reload/tmp/a.out' (arm64).

(lldb) image list
[  0] 69EC6339-CF21-4926-90DA-6470E1F1DDF9 0x0000000100000000 /Users/<username>/demo/module_reload/tmp/a.out    <-- new module
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] 73D51EB5-9335-496C-A95C-D6AEF4ED9C2C 0x0000000000000000 foo.dylib
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib

(lldb) image list -g
[  0] 69EC6339-CF21-4926-90DA-6470E1F1DDF9 0x0000000100000000 /Users/<username>/demo/module_reload/a.out        <-- old module
      /Users/<username>/demo/module_reload/a.out.dSYM/Contents/Resources/DWARF/a.out
[  1] F635824E-318B-3F0C-842C-C369737F2B68 0x00000001800b9000 /usr/lib/dyld
[  2] 73D51EB5-9335-496C-A95C-D6AEF4ED9C2C 0x0000000000000000 foo.dylib
      /Users/<username>/demo/module_reload/foo.dylib.dSYM/Contents/Resources/DWARF/foo.dylib
[  3] AAA5636D-6F3F-3FA7-9F4A-CF966F0308FE 0x000000018035f000 /usr/lib/libc++.1.dylib
...
[ 45] 749BB71D-B6F2-3C9D-A96D-65D22F7A42B3 0x000000018d09b000 /usr/lib/liboah.dylib
[ 46] 69EC6339-CF21-4926-90DA-6470E1F1DDF9 0x0000000100000000 /Users/<username>/demo/module_reload/tmp/a.out    <-- new module
```

Observe that old module isn't removed **(unexpected?) and the new module is appended to the global list.
