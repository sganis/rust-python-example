import re
import string
import random
import itertools
# from numba import jit
import myrustlib  # <-- Importing Rust Implemented Library


def count_doubles(val):
    total = 0
    for c1, c2 in zip(val, val[1:]):
        if c1 == c2:
            total += 1
    return total


def count_doubles_once(val):
    total = 0
    chars = iter(val)
    c1 = next(chars)
    for c2 in chars:
        if c1 == c2:
            total += 1
        c1 = c2
    return total


def count_doubles_itertools(val):
    c1s, c2s = itertools.tee(val)
    next(c2s, None)
    total = 0
    for c1, c2 in zip(c1s, c2s):
        if c1 == c2:
            total += 1
    return total


double_re = re.compile(r'(?=(.)\1)')


def count_double_regex(val):
    return len(double_re.findall(val))


val = ''.join(random.choice(string.ascii_letters) for i in range(1000000))

    
def test_pure_python(benchmark):
    print(benchmark(count_doubles, val))


def test_pure_python_once(benchmark):
    print(benchmark(count_doubles_once, val))


def test_itertools(benchmark):
    print(benchmark(count_doubles_itertools, val))


def test_regex(benchmark):
    print(benchmark(count_double_regex, val))


def test_rust(benchmark):
    print(benchmark(myrustlib.count_doubles, val))


def test_rust_once(benchmark):
    print(benchmark(myrustlib.count_doubles_once, val))


def test_rust_peek(benchmark):
    print(benchmark(myrustlib.count_doubles_peek, val))


def test_rust_memreplace(benchmark):
    print(benchmark(myrustlib.count_doubles_memreplace, val))

def test_rust_fold(benchmark):
    print(benchmark(myrustlib.count_doubles_fold, val))

def test_rust_slice(benchmark):
    print(benchmark(myrustlib.count_doubles_slice, val))

# def test_rust_regex(benchmark):
#     print(benchmark(myrustlib.count_doubles_regex, val))


# @jit(nopython=True, cache=True)
# def count_doubles_once_numba(val):
#     total = 0
#     chars = iter(val)
#     c1 = next(chars)
#     for c2 in chars:
#         if c1 == c2:
#             total += 1
#         c1 = c2
#     return total
