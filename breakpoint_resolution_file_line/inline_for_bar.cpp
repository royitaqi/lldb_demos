#include "bar.h"

__attribute__ ((always_inline)) static inline int get_bar_ret_inlined(const bar_ret& b) {
    return b.ret;
}
