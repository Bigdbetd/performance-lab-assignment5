# Performance Lab Assignment 5

Five implemented Python algorithms with time and space analysis in multiline comments directly below each solution in `performance_lab.py`.

## Run the tests

Requires Python 3 and uses only the standard library.

```bash
python3 performance_lab.py
```

The file includes 20 tests covering assignment examples, empty inputs, ties, negative numbers, order preservation, unique pairs, resize boundaries, input validation, and input preservation. A seeded randomized test also checks 100 cases against reference implementations. All 20 tests passed locally before the code was committed.

## Solutions

1. `most_frequent`: frequency dictionary; empty input returns `None`.
2. `remove_duplicates`: set membership with a list that preserves first-occurrence order.
3. `find_pairs`: complement lookup; follows the starter's distinct-input assumption.
4. `add_n_items`: fixed initial capacity of 4, real allocation and copying when capacity doubles, and printed resize messages.
5. `running_total`: a single pass with a running sum.

## Optimization

`running_total_original` is retained for comparison. It repeatedly slices and sums prefixes in O(n²) time. The refactored `running_total` runs in O(n) time and uses O(1) auxiliary memory instead of O(n) temporary slice memory. Both return an O(n) output list. Full assumptions, best/average/worst cases, potential improvements, and trade-offs appear in `performance_lab.py`.

Starter template: https://github.com/RizeComputerScience/COMPSV-Assignment5
