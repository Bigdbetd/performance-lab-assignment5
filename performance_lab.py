"""Performance Lab: five algorithms, analysis, and executable tests.

Run: python3 performance_lab.py
Analysis uses n = input length, k = distinct values, and p = output pairs.
Unless stated otherwise, numeric arithmetic/comparison costs O(1); arbitrarily
large Python integers add costs depending on their bit length. Hash-table
operations are expected O(1), but pathological collisions can cost O(n).
"""


# Problem 1: Find Most Frequent Element
# Return any most frequent integer. Empty input returns None.
def most_frequent(numbers):
    if not numbers:
        return None
    counts = {}
    for number in numbers:
        counts[number] = counts.get(number, 0) + 1
    # max examines distinct values; insertion order breaks ties consistently.
    return max(counts, key=counts.get)


"""
Time and Space Analysis for problem 1:
- Best-case: O(n) for nonempty input, with normal hashing. Even if every item
  is equal, all n items must be counted. Empty input takes O(1).
- Average-case: expected O(n + k) = O(n), including the final max scan.
- Worst-case: O(n^2) with adversarial hash collisions; normally O(n).
- Space complexity: O(k) auxiliary space for the dictionary, at most O(n).
  The returned integer requires O(1) additional space under the stated model.
- Why this approach? Counting each value once avoids repeatedly searching the
  whole input. It leaves the input unchanged and handles ties and negatives.
- Could it be optimized? Tracking a current winner can remove the final O(k)
  scan without changing asymptotic time or space, though tie behavior may change.
  Sorting and scanning gives O(n log n) worst-case comparisons and avoids hash
  collisions. A sorted copy uses O(n) extra storage; sorting the input changes
  it, and Python's sort can still need O(n) temporary memory.
- Trade-offs: The dictionary spends memory to obtain expected linear time.
  A fixed-size counting array is useful only for a known small value range.
"""


# Problem 2: Remove Duplicates While Preserving Order
# Inputs are integers (or other hashable values); retain the first occurrence.
def remove_duplicates(nums):
    seen = set()
    result = []
    for number in nums:
        if number not in seen:
            seen.add(number)
            result.append(number)
    return result


"""
Time and Space Analysis for problem 2:
- Best-case: O(n) for nonempty input with normal hashing; even an all-equal
  list must be scanned. Empty input takes O(1).
- Average-case: expected O(n), using expected O(1) set membership/insertion
  and amortized O(1) list append.
- Worst-case: O(n^2) with pathological collisions; normally O(n).
- Space complexity: O(k) auxiliary space for seen plus O(k) output space.
  Combined space is O(k), at most O(n), excluding the existing input.
- Why this approach? A set makes duplicate checks fast; the output list keeps
  the original order. The input is not modified.
- Could it be optimized? list(dict.fromkeys(nums)) is shorter but has the same
  expected time and asymptotic space. Checking only the output list saves the
  separate set but needs O(n^2) time when values are distinct.
- Trade-offs: Extra set storage buys faster lookups. Sorting would change the
  required order. This method does not support unhashable nested lists.
"""


# Problem 3: Return All Unique Pairs That Sum to Target
# As specified, input values are distinct integers. Output order is arbitrary.
def find_pairs(nums, target):
    seen = set()
    pairs = []
    for number in nums:
        complement = target - number
        if complement in seen:
            pairs.append((min(number, complement), max(number, complement)))
        # Insert afterward so an item cannot pair with itself.
        seen.add(number)
    return pairs


"""
Time and Space Analysis for problem 3:
- Best-case: O(n) with normal hashing, even when there are no matching pairs.
  Empty input takes O(1).
- Average-case: expected O(n + p) = O(n). With distinct values, each value
  has at most one complement, so p <= floor(n / 2).
- Worst-case: O(n^2) with pathological hash collisions; normally O(n).
- Space complexity: O(n) auxiliary storage for seen and O(p) output storage;
  combined space is O(n). The input is not modified.
- Why this approach? Searching only previously seen values finds each pair
  once. For example, (1, 4) is found when its second value is encountered.
  Canonical tuple order makes the results easy to compare in tests.
- Could it be optimized? If input is already sorted, two pointers find pairs
  in O(n) time with O(1) auxiliary space, excluding output. Sorting an unsorted
  input first requires O(n log n) time; a copy and Python sort use O(n) space.
- Trade-offs: Hashing uses memory for expected linear time on unsorted input.
  Sorting avoids collision-dependent runtime but takes longer or mutates input.
  This implementation relies on the assignment's no-duplicates assumption.
"""


# Problem 4: Simulate List Resizing and Amortized Cost
# Use a backing array, separate logical size, and fixed initial capacity 4.
def add_n_items(n):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be nonnegative")
    capacity = 4
    storage = [None] * capacity
    size = 0
    for item in range(n):
        if size == capacity:
            new_capacity = capacity * 2
            print(f"Resizing from {capacity} to {new_capacity}")
            new_storage = [None] * new_capacity
            for index in range(size):
                new_storage[index] = storage[index]
            storage = new_storage
            capacity = new_capacity
        storage[size] = item
        size += 1
    # Return occupied items only, without the unused capacity slots.
    return storage[:size]


"""
Time and Space Analysis for problem 4:
- When do resizes happen? Just before inserting the 5th, 9th, 17th, ... item,
  when all existing slots are occupied. Capacities grow 4, 8, 16, 32, ... .
  Merely filling capacity does not resize until the next insertion.
- Best-case, average-case, and worst-case for adding n items: O(n) overall
  for n > 0 in the RAM model, including initialization, copies, and the final
  output slice. n = 0 takes O(1). Individual insertion costs vary.
- Worst-case for a single append: O(m), where m is the current occupied size,
  because a full buffer requires allocating a doubled array and copying m items.
  A non-resizing insertion costs O(1).
- Amortized time per append overall: O(1). The copied sizes form a geometric
  series 4 + 8 + 16 + ... whose sum is O(n), not O(n^2). Allocating and filling
  new buffers also totals O(n). Thus n insertions have O(n) aggregate cost.
- Space complexity: O(n) auxiliary backing storage and O(n) returned output
  for n > 0. Old and new buffers coexist during resizing, but peak space stays
  O(n); the final slice also briefly coexists with the backing buffer.
- Why does doubling reduce the cost overall? A resize creates enough room for
  many future insertions, spreading the copying cost across those insertions.
- Could it be optimized? Preallocating n slots removes resizes when n is known.
  That would defeat this exercise's demonstration. A smaller growth factor
  wastes fewer slots but resizes more often; growing by one leads to O(n^2)
  total copying. Doubling can leave nearly half the capacity unused.
- Print statements document actual allocations and copies. Analysis excludes
  terminal latency; there are O(log n) resize messages with O(log n)-digit sizes.
"""


# Problem 5: Compute Running Totals
# Original implementation retained to make the optimization comparison concrete.
def running_total_original(nums):
    return [sum(nums[:index + 1]) for index in range(len(nums))]


"""
Original problem 5 analysis:
For n > 0, best/average/worst time is O(n^2): prefix lengths sum to
1 + 2 + ... + n = n(n + 1)/2. Each prefix is copied and summed again.
Auxiliary peak space is O(n) for a temporary slice, plus O(n) output.
The temporary slices are not all retained, so peak memory is not O(n^2).
Empty input takes O(1). The refactored version follows below.
"""


def running_total(nums):
    # Optimization: reuse a running sum instead of slicing and summing every
    # prefix. This reduces O(n^2) time to O(n) and temporary O(n) space to O(1).
    result = []
    total = 0
    for number in nums:
        total += number
        result.append(total)
    return result


"""
Time and Space Analysis for problem 5:
- Best-case: O(n) for nonempty input, even for all zeros; O(1) for empty input.
- Average-case: O(n), with one addition and one amortized O(1) append per item.
- Worst-case: O(n) overall. One append may resize the Python list in O(n), but
  the aggregate append cost across the complete result is O(n).
- Space complexity: O(1) auxiliary space, excluding O(n) required output.
  Including the new output list, the solution uses O(n) additional space.
- Why this approach? Every prefix reuses the previous total. The input stays
  unchanged, and negative numbers and zeros require no special handling.
- Optimization comparison: The original sums n(n + 1)/2 prefix elements and
  copies that many elements into slices. The refactor does n additions without
  prefix slices. It changes O(n^2) time to O(n) and O(n) auxiliary memory to
  O(1); both versions still allocate an O(n) output list.
- Could it be optimized? A generator could yield totals with O(1) retained
  memory if consumers do not store them, but the assignment requires a list.
  Updating the input in place avoids a separate output, but changes the input
  and does not meet the requirement to return a new list.
- Trade-offs: Retaining the result makes indexed access convenient and costs
  O(n) memory. The single pass has no time-complexity downside for integers.
  For floating-point data, rounding behavior must also be considered; tests
  and the optimization comparison here use integers.
"""


# Tests include the examples, boundary cases, and randomized oracle comparisons.
# Imports and execution are kept here so importing the solutions has no output.
if __name__ == "__main__":
    import io
    import random
    import unittest
    from contextlib import redirect_stdout

    class PerformanceLabTests(unittest.TestCase):
        def test_most_frequent_example(self):
            self.assertEqual(most_frequent([1, 3, 2, 3, 4, 1, 3]), 3)

        def test_most_frequent_empty(self):
            self.assertIsNone(most_frequent([]))

        def test_most_frequent_single_and_equal(self):
            self.assertEqual(most_frequent([8]), 8)
            self.assertEqual(most_frequent([8] * 20), 8)

        def test_most_frequent_tie_and_negatives(self):
            self.assertIn(most_frequent([1, 2, 1, 2]), {1, 2})
            self.assertEqual(most_frequent([-3, 0, -3, 2]), -3)

        def test_duplicates_example(self):
            self.assertEqual(remove_duplicates([4, 5, 4, 6, 5, 7]), [4, 5, 6, 7])

        def test_duplicates_empty_single_and_equal(self):
            self.assertEqual(remove_duplicates([]), [])
            self.assertEqual(remove_duplicates([2]), [2])
            self.assertEqual(remove_duplicates([2] * 20), [2])

        def test_duplicates_distinct_and_negative(self):
            self.assertEqual(remove_duplicates([3, 1, 2]), [3, 1, 2])
            self.assertEqual(remove_duplicates([-1, 0, -1, 0, 2]), [-1, 0, 2])

        def test_pairs_example(self):
            self.assertEqual(set(find_pairs([1, 2, 3, 4], 5)), {(1, 4), (2, 3)})

        def test_pairs_empty_and_no_matches(self):
            self.assertEqual(find_pairs([], 5), [])
            self.assertEqual(find_pairs([1, 2, 3], 20), [])

        def test_pairs_no_self_pair(self):
            self.assertEqual(find_pairs([3], 6), [])
            self.assertEqual(find_pairs([0], 0), [])

        def test_pairs_unsorted_negative_and_zero(self):
            self.assertEqual(set(find_pairs([4, -1, 0, 2, -2, 1], 0)),
                             {(-2, 2), (-1, 1)})
            self.assertEqual(find_pairs([5, 0], 5), [(0, 5)])

        def resize_output(self, n):
            output = io.StringIO()
            with redirect_stdout(output):
                result = add_n_items(n)
            return result, output.getvalue().splitlines()

        def test_resize_zero_and_initial_capacity(self):
            self.assertEqual(self.resize_output(0), ([], []))
            self.assertEqual(self.resize_output(1), ([0], []))
            self.assertEqual(self.resize_output(4), ([0, 1, 2, 3], []))

        def test_resize_example(self):
            self.assertEqual(self.resize_output(6),
                             (list(range(6)), ["Resizing from 4 to 8"]))

        def test_resize_boundaries(self):
            for n in (5, 8, 9, 16, 17, 33, 100):
                with self.subTest(n=n):
                    expected_messages = []
                    capacity = 4
                    while capacity < n:
                        expected_messages.append(
                            f"Resizing from {capacity} to {capacity * 2}")
                        capacity *= 2
                    self.assertEqual(self.resize_output(n),
                                     (list(range(n)), expected_messages))

        def test_resize_invalid_inputs(self):
            with self.assertRaises(ValueError):
                add_n_items(-1)
            for invalid in (2.5, "6", None, True):
                with self.subTest(value=invalid):
                    with self.assertRaises(TypeError):
                        add_n_items(invalid)

        def test_running_totals_example(self):
            self.assertEqual(running_total([1, 2, 3, 4]), [1, 3, 6, 10])

        def test_running_totals_empty_single_and_zero(self):
            self.assertEqual(running_total([]), [])
            self.assertEqual(running_total([7]), [7])
            self.assertEqual(running_total([0, 0, 0]), [0, 0, 0])

        def test_running_totals_negatives(self):
            self.assertEqual(running_total([3, -5, 2, -1]), [3, -2, 0, -1])

        def test_inputs_unchanged_and_new_lists(self):
            original = [3, 1, 3, -2]
            saved = original.copy()
            most_frequent(original)
            dedup = remove_duplicates(original)
            totals = running_total(original)
            self.assertEqual(original, saved)
            self.assertIsNot(dedup, original)
            self.assertIsNot(totals, original)
            distinct = [4, 1, 3, 2]
            find_pairs(distinct, 5)
            self.assertEqual(distinct, [4, 1, 3, 2])

        def test_randomized_oracles(self):
            rng = random.Random(5)
            for _ in range(100):
                nums = [rng.randrange(-10, 11) for _ in range(rng.randrange(40))]
                if nums:
                    winner = most_frequent(nums)
                    self.assertEqual(nums.count(winner),
                                     max(nums.count(x) for x in nums))
                else:
                    self.assertIsNone(most_frequent(nums))
                expected = []
                for number in nums:
                    if number not in expected:
                        expected.append(number)
                self.assertEqual(remove_duplicates(nums), expected)
                self.assertEqual(running_total(nums), running_total_original(nums))
                distinct = rng.sample(range(-30, 31), rng.randrange(25))
                target = rng.randrange(-30, 31)
                expected_pairs = {(min(a, b), max(a, b))
                                  for i, a in enumerate(distinct)
                                  for b in distinct[i + 1:] if a + b == target}
                actual_pairs = find_pairs(distinct, target)
                self.assertEqual(set(actual_pairs), expected_pairs)
                self.assertEqual(len(actual_pairs), len(set(actual_pairs)))

    unittest.main(verbosity=2)
