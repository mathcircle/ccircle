
"""
Dictionaries:
    {key, value} -- keys are immutable
    mutable
    add in any order
    "if key in dict"
    dict.items() -> list of tuples corresponding to dictionary entries
    if you're gonna sort, use the same types
"""
# 1) write function numbers_squared_dict(n) -> returns a dictionary
# 2) write a function sort_by_key(dict) -> returns a list of tuples sorted by key
# 3) write a function sort_by_value(dict)
import operator
def sort_by_key(d):
    return sorted(d.items())
def reverse_sort_by_key(d):
    return sorted(d.items(), reverse=True)
def sort_by_value(d):
    return sorted(d.items(), key=operator.itemgetter(1))
    # for tuple (x, y), operator.itemgetter(1) would give you y's value.

# how to loop over entries in the dictionary
d = {
    1: 'hi',
    2: 'low',
    3: 'sheep'
}
for (key, value) in d.items():
    # Do something with the dictionary values!
    print(key, value)