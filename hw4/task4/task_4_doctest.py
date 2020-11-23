"""
How to use docstrings in python
1. Install python 3.9 from https://www.python.org/downloads/;
2. Do not forget to add python.exe path to PATH variable to be able to call it from the terminal;
3. Open terminal;
4. Type cd "path_to_your_work_directory/EPAM-training/hw4/task4" and run "python3 task_4_doctest.py";
5. If everything is ok, terminal's output should be empty;
6. Open task_4_doctest.py with your text editor and try to add your own test;
    6.1. Find docstring inside function fizzbuzz right after the definition;
    6.2. Add ">>> fizzbuzz(your_value)" to the end of this docstring(starting from a new line)
         to make python evaluate this command into test;
    6.3. Add [item1, item2] list of results on the next line. This is an expected result which will be checked;
    6.4. Return to the terminal, run "python3 task_4_doctest.py" and check on the errors again;
7. (Optional) Try to add test, which expects to rise error and catches it (look for example into docstring);
8. Profit!
"""
from typing import List


def fizzbuzz(n: int) -> List[str]:
    """Return N FizzBuzz numbers
    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    >>> fizzbuzz(15)
    ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'Fizz Buzz']

    >>> fizzbuzz(-1)
    Traceback (most recent call last):
        ...
    ValueError: n must be >= 1
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    res = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            res.append("Fizz Buzz")
        elif i % 3 == 0:
            res.append("Fizz")
        elif i % 5 == 0:
            res.append("Buzz")
        else:
            res.append(str(i))
    return res


if __name__ == "__main__":
    import doctest

    doctest.testmod()
