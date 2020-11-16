"""
Here's a not very efficient calculation function that calculates something important::

    import time
    import struct
    import random
    import hashlib

    def slow_calculate(value):
        #Some weird voodoo magic calculations
        time.sleep(random.randint(1,3))
        data = hashlib.md5(str(value).encode()).digest()
        return sum(struct.unpack('<' + 'B' * len(data), data))

Calculate total sum of slow_calculate() of all numbers starting from 0 to 500.
Calculation time should not take more than a minute. Use functional capabilities of multiprocessing module.
You are not allowed to modify slow_calculate function.

"""
import hashlib
import random
import struct
from multiprocessing import Pool
from time import perf_counter, sleep
from typing import Any, Callable, Sequence


def slow_calculate(value: Any):
    """Some weird voodoo magic calculations"""
    sleep(random.randint(1, 3))
    data = hashlib.md5(str(value).encode()).digest()
    return sum(struct.unpack("<" + "B" * len(data), data))


def call_func(data: Sequence[Any], func: Callable = slow_calculate) -> Sequence[Any]:
    with Pool(25) as p:
        return p.map(func, data)


if __name__ == "__main__":
    t1 = perf_counter()
    call_func(list(range(0, 501)))
    t2 = perf_counter()
    print("Elapsed time during the whole program in seconds:", t2 - t1)
