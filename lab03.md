# CCircle.Lab.3 : Python Lists, Functions and Objects
### Prev -> [CodingCircle Summer 2017 Documentation](index)

## Welcome to Lab 3
For questions asking you to figure out what is printed when certain code is evaluated,
please write down your solution to the problem _before_ trying to run the provided code on your computer.

## Lists
1. Complete the function below with a single line of code.
```python
    def squared_list(list_of_integers):
    """Returns a list corresponding to the input list of integers, with all elements squared.

    >>> squared_list([1, 2, 3])
    [1, 4, 9]
    """
    return _________________________
```
1. Complete the function below.
```python
    def square_elements(list_of_integers):
    """Mutates the input list of integers, squaring all elements.

    >>> ints = [1, 2, 3]
    >>> square_elements(ints)
    >>> ints
    [1, 4, 9]
    """

        __________________________

        __________________________

        __________________________
```
1. Complete the function below.
```python
    def reverse(a_list):
    """Mutates the input list, reversing the elements.

    >>> ints = [1, 2, 3]
    >>> reverse(ints)
    >>> ints
    [3, 2, 1]
    """

        __________________________

        __________________________

        __________________________
```
#### Extra for Experts
1. There is a built-in function `zip`, which takes two lists and 'zips' them together. An example is
```python
    >>> for tuple in zip([1, 2], ['a', 'b']):
    ...    print tuple
    (1, 'a')
    (2, 'b')
```
The documentation for `zip` is
```
    zip(...)
        zip(seq1 [, seq2 [...]]) -> [(seq1[0], seq2[0] ...), (...)]

    Return a list of tuples, where each tuple contains the i-th element
    from each of the argument sequences.  The returned list is truncated
    in length to the length of the shortest argument sequence.
```
Write function `my_zip` that mimics the behavior of `zip`.
```python
        def my_zip(a, b):

            __________________________

            __________________________

            __________________________

            __________________________

            __________________________

            __________________________

            __________________________

            __________________________
```


## Functions
1. Fill in the blanks in the following function definition for adding a to the absolute value of b, without calling `abs`.
```python
    from operator import add, sub

    def a_plus_positive_b(a, b):
        """Returns the sum of a and the positive value of b, without calling the abs() built-in.

        >>> a_plus_abs_b(3, 4)
        7
        >>> a_plus_abs_b(3, -4)
        7
        """

        if b < 0:
            f = _____
        else:
            f = _____
        return f(a, b)
```
1. Write what is printed when the following code is evaluated.
```python
    def boom():
        return 1 / 0

    boom
    boom()
```
1. Write what is printed when the following code is evaluated.
```python
    def hmm(a=[]):
      a.append(1)
      return a

    print(hmm())
    print(hmm())
    print(hmm())
```
1. Write what is printed when the following code is evaluated.
```python
    def magic_print(a, b):
      print(print(a), print(b))

    magic_print(1, 2)
```
#### Extras for Experts
1. Write what is printed when the following code is evaluated.
```python
    from operator import add, mul

    def f(x, y):
        print('batman ', y)
        return add(add(x, y), 1)

    def g(x, y):
        print('robin ', x)
        return mul(mul(x, y), 2)

    f(2, g(2, f(500, 2)))
```
1. These steps give the hailstore sequence, as written in Douglas Hofstadter's book _Gödel, Escher, Bach_.
```
    Pick a positive integer n as the start.
    If n is even, divide it by 2.
    If n is odd, multiply it by 3 and add 1.
    Continue this process until n is 1.
```
Write function _hailstone(n)_ to print the _hailstone sequence_ starting at n, and return its length.
```python
    def hailstone(n):

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________

        __________________________
```


## Objects
1. Write what is printed when the following code is evaluated.
```python
    class Song(object):

        def __init__(self, lyrics):
            self.lyrics = lyrics

        def print_song(self):
            for line in self.lyrics:
                print line

    roses_song = Song([
        "Roses are red"
        , "Violets are blue"
        , "Carnations can also be red..."
        , "Woohoo!"
    ])

    roses_song.print_song()
```
#### Extra for Experts
1. Write what is printed when the following code is evaluated.
```python
    o = min
    o = max
    g, h = (min, max)
    max = g
    goo = max(o(3, g(2, h(1, 5), 3)), 4)

    print(goo)
```


## Congratulations
You've completed this lab!

### Next -> [Lab 4: Python Dictionaries](lab04)