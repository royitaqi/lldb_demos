#include "foo.h"

__attribute__ ((always_inline)) int get_foo_ret_inlined(const foo_ret& f) {
    return f.ret;
}
