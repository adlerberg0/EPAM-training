"""
This task is optional.

Write a generator that takes a number N as an input
and returns a generator that yields N FizzBuzz numbers*
Don't use any ifs, you can find an approach for the implementation in this video**.


Definition of done:
 - function is created
 - function is properly formatted
 - function has tests


* https://en.wikipedia.org/wiki/Fizz_buzz
** https://www.youtube.com/watch?v=NSzsYWckGd4
"""
from typing import Generator


def fizzbuzz(n: int) -> Generator[str, int, None]:
    """Return N FizzBuzz numbers

    >>> list(fizzbuzz(5))
    ['1', '2', 'Fizz', '4', 'Buzz']
    >>> list(fizzbuzz(15))
    ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'Fizz Buzz']
    >>> list(fizzbuzz(-1))
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 1
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    k = 1
    # find first zero item in mask and yield arr[mask_idx]
    while k <= n:
        mask = [k % 3 | k % 5, k % 3, k % 5, 0]
        arr = ["Fizz Buzz", "Fizz", "Buzz", f"{k}"]
        mask_idx = 0
        while mask[mask_idx]:
            mask_idx += 1
        k += 1

        yield arr[mask_idx]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
