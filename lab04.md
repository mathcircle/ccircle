# CCircle.Lab.4 : Python Dictionaries
### Prev -> [Lab 3: Python Lists, Functions and Objects](lab03)

## Dictionaries
1. Fill in the function with one line such that it behaves according to the pydoc.
```python
    import operator

    def sort(dict, by_value=False, reverse=False):
    """Return a list of tuples corresponding to the dictionary's entries sorted by either key or value;
            potentially reverse-sorted.

    :param dict: The dictionary to sort.
    :param by_value: To sort by value instead of by key.
    :param reverse: Output list in reverse-sorted order.

    >>> sort({3: 'b', 2: 'c', 1: 'a'})
    [(1, 'a'), (2, 'c'), (3, 'b')]

    >>> sort({3: 'b', 2: 'c', 1: 'a'}, by_value=True)
    [(1, 'a'), (3, 'b'), (2, 'c')]

    >>> sort({3: 'b', 2: 'c', 1: 'a'}, reverse=True)
    [(3, 'b'), (2, 'c'), (1, 'a')]
    """
    return _______________________________________________________________________________________________________
```

## Congratulations
You've completed this lab!
