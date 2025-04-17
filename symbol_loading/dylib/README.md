# Setup

```
alias cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
alias oooo='otool -lv'
```

# Tutorial

## Build

Run
```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc -dynamiclib bar.cpp -o bar.dylib
cccc main.cpp foo.dylib bar.dylib
```

## Debug a.out with "target.preload-symbols = true". Observe the symbols loaded.

Run
```
lldb
(lldb) settings set target.preload-symbols true
(lldb) target create a.out
(lldb) statistics dump
```

Here is a part of the output:
```
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/a.out",
      "symbolsLoaded": 7,
      ...,
    },
    {
      "path": "foo.dylib",
      "symbolsLoaded": 3,
    },
    {
      "path": "bar.dylib",
      "symbolsLoaded": 3,
    },
  ],
```


## Debug a.out with "target.preload-symbols = false". Observe the symbols loaded.

Run
```
lldb
(lldb) settings set target.preload-symbols false
(lldb) target create a.out
(lldb) statistics dump
```

Here is a part of the output:
```
  "modules": [
    {
      "path": "/Users/<username>/demo/symbol_loading/a.out",
      "symbolsLoaded": 7,
      ...,
    },
    {
      "path": "foo.dylib",
      "symbolsLoaded": 3,
    },
    {
      "path": "bar.dylib",
      "symbolsLoaded": 3,
    },
  ],
```


## Inspect why symbols in `foo.dylib` and `bar.dylib` are preloaded even when the program hasn't been started

Run:
```
oooo a.out
```

Output:
```
Load command 14
          cmd LC_LOAD_DYLIB
      cmdsize 40
         name foo.dylib (offset 24)
   time stamp 2 Wed Dec 31 16:00:02 1969
      current version 0.0.0
compatibility version 0.0.0
Load command 15
          cmd LC_LOAD_DYLIB
      cmdsize 40
         name bar.dylib (offset 24)
   time stamp 2 Wed Dec 31 16:00:02 1969
      current version 0.0.0
compatibility version 0.0.0
```

So `a.out` has Mach-O load commands which loaded the two dylibs.
