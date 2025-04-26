#! /usr/bin/env python3

import json
import sys

def reduce_stats_dump(stats, init, reducer):
    state = init
    for module_stats in stats["modules"]:
        state = reducer(state, module_stats)
    return state

def reducer(state, module_stats):
    category = "unknown"
    if "/Users/royshi/fbsource/buck-out/" in module_stats["path"]:
        category = "user_code"
    elif "/Library/Developer/CoreSimulator/" in module_stats["path"]:
        category = "simulator_runtime"
    
    if category not in state:
        state[category] = 0
    state[category] += module_stats["symbolTableSymbolCount"]

    return state

def main():
    text = sys.stdin.read()
    stats = json.loads(text)
    state = reduce_stats_dump(stats, {}, reducer)
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()
