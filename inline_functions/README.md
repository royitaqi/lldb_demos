# Setup

```
cccc='xcrun clang++ -g -O0 -std=gnu++11 -stdlib=libc++'
dddd=dwarfdump
dddddl='dwarfdump --debug-line'
```


# Run

Compile and run:
```
cccc -dynamiclib foo.cpp -o foo.dylib
cccc -dynamiclib bar.cpp -o bar.dylib
cccc main.cpp foo.dylib bar.dylib not_inline.cpp
./a.out
echo $?
```


## Inline functions show up in the `.debug_info` section of *the call site's CU*, as `DW_TAG_inlined_subroutine`

```
dddd foo.dylib.dSYM
dddd bar.dylib.dSYM
```

Example:
```
0x0000000b: DW_TAG_compile_unit
              DW_AT_producer	("Apple clang version 15.0.0 (clang-1500.3.9.4)")
              DW_AT_language	(DW_LANG_C_plus_plus_11)
              DW_AT_name	("foo.cpp")
              DW_AT_LLVM_sysroot	("/Applications/Xcode_15.3.0_15E204a_fb.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk")
              DW_AT_APPLE_sdk	("MacOSX.sdk")
              DW_AT_stmt_list	(0x00000000)
              DW_AT_comp_dir	("/Users/<username>/demo/inline_functions")
              DW_AT_low_pc	(0x0000000000003f18)
              DW_AT_high_pc	(0x0000000000003fa0)

...

0x000000cb:   DW_TAG_subprogram
                DW_AT_low_pc	(0x0000000000003f68)
                DW_AT_high_pc	(0x0000000000003fa0)
                DW_AT_frame_base	(DW_OP_reg29 W29)
                DW_AT_linkage_name	("_Z11get_foo_retv")
                DW_AT_name	("get_foo_ret")
                DW_AT_decl_file	("/Users/<username>/demo/inline_functions/foo.cpp")
                DW_AT_decl_line	(11)
                DW_AT_type	(0x0000000000000048 "int")
                DW_AT_external	(true)

...

0x000000f6:     DW_TAG_inlined_subroutine
                  DW_AT_abstract_origin	(0x00000000000000a5 "_Z19get_foo_ret_inlinedRK7foo_ret")
                  DW_AT_low_pc	(0x0000000000003f84)
                  DW_AT_high_pc	(0x0000000000003f8c)
                  DW_AT_call_file	("/Users/<username>/demo/inline_functions/foo.cpp")
                  DW_AT_call_line	(12)
                  DW_AT_call_column	(0x0b)
```

## Inline functions show up in the `.debug_line` section of *the call site's CU*

```
dddddl foo.dylib.dSYM
dddddl bar.dylib.dSYM
```

Example:
```
file_names[  1]:
           name: "foo.h"
      dir_index: 1
       mod_time: 0x00000000
         length: 0x00000000
file_names[  2]:
           name: "inline_for_foo.h"
      dir_index: 1
       mod_time: 0x00000000
         length: 0x00000000
file_names[  3]:
           name: "foo.cpp"
      dir_index: 0
       mod_time: 0x00000000
         length: 0x00000000

Address            Line   Column File   ISA Discriminator Flags
------------------ ------ ------ ------ --- ------------- -------------
0x0000000000003f18      3      0      2   0             0  is_stmt
0x0000000000003f20      4     12      2   0             0  is_stmt prologue_end
0x0000000000003f24      4     14      2   0             0
0x0000000000003f28      4      5      2   0             0
0x0000000000003f30      5      0      3   0             0  is_stmt
0x0000000000003f38      6      7      3   0             0  is_stmt prologue_end
0x0000000000003f40      7      7      3   0             0  is_stmt
0x0000000000003f44      8     20      3   0             0  is_stmt
0x0000000000003f4c      8     22      3   0             0
0x0000000000003f50      8     29      3   0             0
0x0000000000003f54      8     27      3   0             0
0x0000000000003f58      8     18      3   0             0
0x0000000000003f5c      8      3      3   0             0
0x0000000000003f68     11      0      3   0             0  is_stmt
0x0000000000003f74     12     31      3   0             0  is_stmt prologue_end
0x0000000000003f84      4     12      2   0             0  is_stmt               <-- inlined function
0x0000000000003f88      4     14      2   0             0                        <--
0x0000000000003f8c     12      7      3   0             0  is_stmt
0x0000000000003f90     13     10      3   0             0  is_stmt
0x0000000000003f94     13      3      3   0             0
0x0000000000003fa0     13      3      3   0             0  end_sequence
```

## As a comparison, regular function show up in *the implementation's CU*, as `DW_TAG_subprogram`

```
dddd a.out.dSYM
dddddl a.out.dSYM
```

Example:
```
0x00000089: DW_TAG_compile_unit
              DW_AT_producer	("Apple clang version 15.0.0 (clang-1500.3.9.4)")
              DW_AT_language	(DW_LANG_C_plus_plus_11)
              DW_AT_name	("not_inline.cpp")
              DW_AT_LLVM_sysroot	("/Applications/Xcode_15.3.0_15E204a_fb.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk")
              DW_AT_APPLE_sdk	("MacOSX.sdk")
              DW_AT_stmt_list	(0x00000067)
              DW_AT_comp_dir	("/Users/<username>/demo/inline_functions")
              DW_AT_low_pc	(0x0000000100003f80)
              DW_AT_high_pc	(0x0000000100003f88)

0x000000b0:   DW_TAG_subprogram
                DW_AT_low_pc	(0x0000000100003f80)
                DW_AT_high_pc	(0x0000000100003f88)
                DW_AT_APPLE_omit_frame_ptr	(true)
                DW_AT_frame_base	(DW_OP_reg31 WSP)
                DW_AT_linkage_name	("_Z21get_value_not_inlinedv")
                DW_AT_name	("get_value_not_inlined")
                DW_AT_decl_file	("/Users/<username>/demo/inline_functions/not_inline.cpp")
                DW_AT_decl_line	(3)
                DW_AT_type	(0x00000000000000cd "int")
                DW_AT_external	(true)
```

```
file_names[  1]:
           name: "not_inline.cpp"
      dir_index: 0
       mod_time: 0x00000000
         length: 0x00000000

Address            Line   Column File   ISA Discriminator Flags
------------------ ------ ------ ------ --- ------------- -------------
0x0000000100003f80      3      0      1   0             0  is_stmt
0x0000000100003f84      4      5      1   0             0  is_stmt prologue_end
0x0000000100003f88      4      5      1   0             0  is_stmt end_sequence
```


## Set file/line breakpoint and see inline functions get resolved
```
$ lldb a.out
(lldb) br set --file inline_for_foo.h --line 4
Breakpoint 1: where = foo.dylib`get_foo_ret_inlined(foo_ret const&) + 8 at inline_for_foo.h:4:12, address = 0x0000000000003f20
(lldb) br set --file inline_for_bar.cpp --line 4
Breakpoint 2: where = bar.dylib`get_bar_ret_inlined(bar_ret const&) + 8 at inline_for_bar.cpp:4:12, address = 0x0000000000003f20
```

## Change settings in LLDB to resolve file/line breakpoints for inline functions ONLY IN HEADER FILES
```
$ lldb a.out
(lldb) settings set target.inline-breakpoint-strategy headers
(lldb) br set --file inline_for_foo.h --line 4
Breakpoint 1: where = foo.dylib`get_foo_ret_inlined(foo_ret const&) + 8 at inline_for_foo.h:4:12, address = 0x0000000000003f20
(lldb) br set --file inline_for_bar.cpp --line 4
Breakpoint 2: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
```

## Change settings in LLDB to NEVER resolve file/line breakpoints for inline functions
```
$ lldb a.out
(lldb) settings set target.inline-breakpoint-strategy never
(lldb) br set --file inline_for_foo.h --line 4
Breakpoint 1: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
(lldb) br set --file inline_for_bar.cpp --line 4
Breakpoint 2: no locations (pending).
WARNING:  Unable to resolve breakpoint to any actual locations.
```
