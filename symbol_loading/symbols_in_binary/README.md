# Setup

```
> alias cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
> alias ssss='dsymutil --symtab'
```

# Tutorial: example1.cpp

## Build
```
> cccc example1.cpp -o example1
```

## Observe the symbol table in `example1`

```
> ssss example1
----------------------------------------------------------------------
Symbol table for: 'example1' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     1] 0000002e 64 (N_SO         ) 00     0000   0000000000000000 '/Users/royshi/demo/symbol_loading/symbols_in_binary/'
[     2] 00000063 64 (N_SO         ) 00     0000   0000000000000000 'example1.cpp'
[     3] 00000070 66 (N_OSO        ) 00     0001   000000006803eec1 '/private/var/folders/m8/fkx9dg8n7k517w7rq2blxhkw0000gn/T/example1-8ab731.o'
[     4] 00000001 2e (N_BNSYM      ) 01     0000   0000000100003f04
[     5] 0000000b 24 (N_FUN        ) 01     0000   0000000100003f04 '__Z3foov'
[     6] 00000001 24 (N_FUN        ) 00     0000   0000000000000030
[     7] 00000001 4e (N_ENSYM      ) 01     0000   0000000100003f04
[     8] 00000001 2e (N_BNSYM      ) 01     0000   0000000100003f34
[     9] 00000002 24 (N_FUN        ) 01     0000   0000000100003f34 '__Z3barv'
[    10] 00000001 24 (N_FUN        ) 00     0000   0000000000000030
[    11] 00000001 4e (N_ENSYM      ) 01     0000   0000000100003f34
[    12] 00000001 2e (N_BNSYM      ) 01     0000   0000000100003f64
[    13] 00000028 24 (N_FUN        ) 01     0000   0000000100003f64 '_main'
[    14] 00000001 24 (N_FUN        ) 00     0000   000000000000003c
[    15] 00000001 4e (N_ENSYM      ) 01     0000   0000000100003f64
[    16] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[    17] 00000002 0f (     SECT EXT) 01     0000   0000000100003f34 '__Z3barv'
[    18] 0000000b 0f (     SECT EXT) 01     0000   0000000100003f04 '__Z3foov'
[    19] 00000014 0f (     SECT EXT) 01     0010   0000000100000000 '__mh_execute_header'
[    20] 00000028 0f (     SECT EXT) 01     0000   0000000100003f64 '_main'
```

General structure of the symbol table:
1. The first `N_SO` entry is always empty.
2. The second and third `N_SO` entries are the path and the filename of the main source file.
3. The `N_OSO` entry points to the .o file which was used to create this binary.
4. The `N_BNSYM` and `N_ENSYM` pairs describe a list of symbols.
5. Within each pair, the first `N_FUN` entry describes the name of the function. Its value indicates the function's low/starting address. The second `N_FUN` entry's value indicates the function's size (i.e. low address + size = high address).
6. The `EXT` entries list the external symbols.

It makes sense that the binary contains the functions that are defined in the source file:
1. `__Z3foov`: the `foo` function
2. `__Z3barv`: the `bar` function
3. `_main`: the `main` function

There is one additional symbol: `__mh_execute_header`.
It's commonly known as the "mach header".
It's inserted by the linker to represent the beginning of the Mach-O image in an executable.

`SECT` means where the symbol's definition (for functions, it's the function's code) is stored within the current object file.

`EXT` means the symbol is external and is visible/can be accessed from other object files.


## Observe the symbol table in the dSYM

```
> ssss example1.dSYM/Contents/Resources/DWARF/example1
----------------------------------------------------------------------
Symbol table for: 'example1.dSYM/Contents/Resources/DWARF/example1' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000002 0f (     SECT EXT) 01     0000   0000000100003f34 '__Z3barv'
[     1] 0000000b 0f (     SECT EXT) 01     0000   0000000100003f04 '__Z3foov'
[     2] 00000014 0f (     SECT EXT) 01     0010   0000000100000000 '__mh_execute_header'
[     3] 00000028 0f (     SECT EXT) 01     0000   0000000100003f64 '_main'
```

This is the exactly same info as in the symbol table of `example1` (index 17-20).


# Tutorial: example2.cpp

## Build

```
cccc -dynamiclib bar.cpp -o bar.dylib
cccc -dynamiclib foo.cpp bar.dylib -o foo.dylib
cccc example2.cpp foo.dylib -o example2
```


## Observer the symbol table in `example2`

```
> ssss example2
----------------------------------------------------------------------
Symbol table for: 'example2' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     1] 00000025 64 (N_SO         ) 00     0000   0000000000000000 '/Users/royshi/demo/symbol_loading/symbols_in_binary/'
[     2] 0000005a 64 (N_SO         ) 00     0000   0000000000000000 'example2.cpp'
[     3] 00000067 66 (N_OSO        ) 00     0001   000000006803f0c8 '/private/var/folders/m8/fkx9dg8n7k517w7rq2blxhkw0000gn/T/example2-b7236c.o'
[     4] 00000001 2e (N_BNSYM      ) 01     0000   0000000100003f70
[     5] 00000016 24 (N_FUN        ) 01     0000   0000000100003f70 '_main'
[     6] 00000001 24 (N_FUN        ) 00     0000   000000000000002c
[     7] 00000001 4e (N_ENSYM      ) 01     0000   0000000100003f70
[     8] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     9] 00000002 0f (     SECT EXT) 01     0010   0000000100000000 '__mh_execute_header'
[    10] 00000016 0f (     SECT EXT) 01     0000   0000000100003f70 '_main'
[    11] 0000001c 01 (     UNDF EXT) 00     0100   0000000000000000 '__Z3foov'
```

It makes sense that `main` defined in `example2`.

`foo` is marked as `EXT`, because `example2.cpp` includes a forward declaration of `foo` from `foo.h`. It is `UNDF` because the definition isn't included in the binary due to dynamic linking.

There is no symbol `bar`, because `example2` doesn't have anything to do with `bar` - `foo.dylib` does, see below.


## Observer the symbol table in `foo.dylib`

```
> ssss foo.dylib
----------------------------------------------------------------------
Symbol table for: 'foo.dylib' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     1] 00000014 64 (N_SO         ) 00     0000   0000000000000000 '/Users/royshi/demo/symbol_loading/symbols_in_binary/'
[     2] 00000049 64 (N_SO         ) 00     0000   0000000000000000 'foo.cpp'
[     3] 00000051 66 (N_OSO        ) 00     0001   000000006803f0c8 '/private/var/folders/m8/fkx9dg8n7k517w7rq2blxhkw0000gn/T/foo-19abad.o'
[     4] 00000001 2e (N_BNSYM      ) 01     0000   0000000000003f74
[     5] 00000002 24 (N_FUN        ) 01     0000   0000000000003f74 '__Z3foov'
[     6] 00000001 24 (N_FUN        ) 00     0000   0000000000000028
[     7] 00000001 4e (N_ENSYM      ) 01     0000   0000000000003f74
[     8] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     9] 00000002 0f (     SECT EXT) 01     0000   0000000000003f74 '__Z3foov'
[    10] 0000000b 01 (     UNDF EXT) 00     0100   0000000000000000 '__Z3barv'
```

See `bar` being mentioned as `EXT` and `UNDF`.



## Observer the symbol table in `bar.dylib`

Now finally the symbol table of `bar.dylib`
```
> ssss bar.dylib
----------------------------------------------------------------------
Symbol table for: 'bar.dylib' (arm64)
----------------------------------------------------------------------
Index    n_strx   n_type             n_sect n_desc n_value
======== -------- ------------------ ------ ------ ----------------
[     0] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     1] 0000000b 64 (N_SO         ) 00     0000   0000000000000000 '/Users/royshi/demo/symbol_loading/symbols_in_binary/'
[     2] 00000040 64 (N_SO         ) 00     0000   0000000000000000 'bar.cpp'
[     3] 00000048 66 (N_OSO        ) 00     0001   000000006803f0c8 '/private/var/folders/m8/fkx9dg8n7k517w7rq2blxhkw0000gn/T/bar-755d67.o'
[     4] 00000001 2e (N_BNSYM      ) 01     0000   0000000000003fa0
[     5] 00000002 24 (N_FUN        ) 01     0000   0000000000003fa0 '__Z3barv'
[     6] 00000001 24 (N_FUN        ) 00     0000   0000000000000008
[     7] 00000001 4e (N_ENSYM      ) 01     0000   0000000000003fa0
[     8] 00000001 64 (N_SO         ) 01     0000   0000000000000000
[     9] 00000002 0f (     SECT EXT) 01     0000   0000000000003fa0 '__Z3barv'
```

Besides `bar`, it has no other `EXT` symbols.
