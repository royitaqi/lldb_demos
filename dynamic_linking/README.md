# Setup

```
alias cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
alias oooo='otool -lv'
alias ssss='dsymutil --symtab'
```

# Tutorial

## Build with dynamic linking

Run
```
cccc -dynamiclib bar.cpp -o bar.dylib
cccc -dynamiclib foo.cpp bar.dylib -o foo.dylib
cccc main.cpp foo.dylib
```


## Verify that the libraries are actually __dynamically__ linked


We have multiple approaches:

**Approach 1:**
```
> oooo a.out
Load command 13
          cmd LC_LOAD_DYLIB
      cmdsize 40
         name foo.dylib (offset 24)
   time stamp 2 Wed Dec 31 16:00:02 1969
      current version 0.0.0
compatibility version 0.0.0
```
Observe that `a.out` has Mach-O load commands which load `foo.dylib`.


```
> oooo foo.dylib
Load command 11
          cmd LC_LOAD_DYLIB
      cmdsize 40
         name bar.dylib (offset 24)
   time stamp 2 Wed Dec 31 16:00:02 1969
      current version 0.0.0
compatibility version 0.0.0
```

`foo.dylib` has load commands which load `bar.dylib`.


**Approach 2: [0]**

`otool -L` Display the names and version numbers of the shared libraries that the object file uses, as well as the shared library ID if the file is a shared library.

```
> otool -L a.out
a.out:
	foo.dylib (compatibility version 0.0.0, current version 0.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 1900.178.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
```
The fact that `foo.dylib` is printed means that they are dynamically linked.
If they were statically linked, they would have not been printed.


```
> otool -L foo.dylib
foo.dylib:
	foo.dylib (compatibility version 0.0.0, current version 0.0.0)
	bar.dylib (compatibility version 0.0.0, current version 0.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 1900.178.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
```
It's interesting that `foo.dylib` includes itself in the list. Same for `bar.dylib`.


**Approach 3: [0]**

From `man dyld`:
> DYLD_PRINT_LIBRARIES
> When this is set, the dynamic linker writes to file descriptor 2
  (normally standard error) the filenames of the libraries the program is
  using. This is useful to make sure that the use of DYLD_LIBRARY_PATH is
  getting what you want.

```
> DYLD_PRINT_LIBRARIES=1 ./a.out
dyld[4662]: <FDD004EF-2302-4785-A37A-F5FD8838440B> /Users/<username>/demo/symbol_loading/dylib/a.out
dyld[4662]: <3B0872CD-42F9-435D-8E51-06BF5B7A127A> /Users/<username>/demo/symbol_loading/dylib/foo.dylib
dyld[4662]: <D6CABC56-E395-4289-8B10-2CE14DC642FC> /Users/<username>/demo/symbol_loading/dylib/bar.dylib
...
```


**Approach 4: [0]**
```
> ssss a.out
----------------------------------------------------------------------
Symbol table for: 'a.out' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     1] 00000031 64 (N_SO         ) 00     0000   0000000000000000 '/Users/<username>/demo/symbol_loading/dylib/'
[     2] 0000005a 64 (N_SO         ) 00     0000   0000000000000000 'main.cpp'
[     3] 00000063 66 (N_OSO        ) 00     0001   00000000680136c9 '/private/var/folders/tt/k30mc06n1blgsvbp_tgfbsnh0000gn/T/main-3f3d7a.o'
[     4] 00000001 2e (N_BNSYM      ) 01     0000   0000000100003f50
[     5] 00000019 24 (N_FUN        ) 01     0000   0000000100003f50 '_main'
[     6] 00000001 24 (N_FUN        ) 00     0000   0000000000000040
[     7] 00000001 4e (N_ENSYM      ) 01     0000   0000000100003f50
[     8] 00000016 20 (N_GSYM       ) 00     0000   0000000000000000 '_g'
[     9] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[    10] 00000002 0f (     SECT EXT) 01     0010   0000000100000000 '__mh_execute_header'
[    11] 00000016 0f (     SECT EXT) 05     0000   0000000100008000 '_g'
[    12] 00000019 0f (     SECT EXT) 01     0000   0000000100003f50 '_main'
[    13] 0000001f 01 (     UNDF EXT) 00     0200   0000000000000000 '__Z3barv'
[    14] 00000028 01 (     UNDF EXT) 00     0100   0000000000000000 '__Z3foov'
```

Note that `__Z3barv` and `__Z3foov` are undefined ("UNDF"), indicating that they are not defined in the current module (a.out) but are defined in other modules (the dylibs).

BTW, `__mh_execute_header` is commonly known as the "mach header".



# References

[0] https://michaelspangler.io/posts/statically-linking-on-macos.html

[1] https://manybutfinite.com/post/anatomy-of-a-program-in-memory/
