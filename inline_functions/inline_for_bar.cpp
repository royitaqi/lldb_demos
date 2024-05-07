#include "bar.h"

__attribute__ ((always_inline)) int get_bar_ret_inlined(const bar_ret& b) {
    return b.ret;
}
