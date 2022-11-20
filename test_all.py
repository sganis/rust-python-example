import re
import string
import random
import itertools
import numpy as np
from numba import jit
import myrustlib  # <-- Importing Rust Implemented Library
import myrustpyo3  # <-- Importing Rust Implemented Library
import mycythonlib 

import sys
# sys.path.append('./pyext-myclib')
# import myclib  # <-- Importing C Implemented Library


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

def count_doubles_regex(val):
    return len(double_re.findall(val))

def count_doubles_numpy(val):
    ng = np.fromstring(val, dtype=np.byte)
    return np.sum(ng[:-1] == ng[1:])

def count_doubles_comprehension(val):
    return sum(1 for c1, c2 in zip(val, val[1:]) if c1 == c2)

@jit(nopython=True, cache=True)
def count_doubles_once_numba(val):
    total = 0
    chars = iter(val)
    c1 = next(chars)
    for c2 in chars:
        if c1 == c2:
            total += 1
        c1 = c2
    return total

# @jit(nopython=True, cache=True)
# def count_doubles_numpy_numba(ng):
#     return np.sum(ng[:-1] == ng[1:])



val = ''.join(random.choice(string.ascii_letters) for i in range(1000000))


def test():
    a = count_doubles(val)
    assert a == count_doubles(val)
    assert a == count_doubles_once(val)
    assert a == count_doubles_itertools(val)
    assert a == count_doubles_regex(val)
    assert a == count_doubles_numpy(val)
    assert a == count_doubles_comprehension(val)
    assert a == myrustlib.count_doubles(val)
    assert a == myrustlib.count_doubles_once(val)
    assert a == myrustlib.count_doubles_peek(val)
    assert a == myrustlib.count_doubles_slice(val)
    assert a == myrustlib.count_doubles_memreplace(val)
    assert a == myrustlib.count_doubles_once_bytes(val)
    assert a == myrustlib.count_doubles_fold(val)
    assert a == mycythonlib.count_doubles(val)
    # assert a == count_doubles_numpy_numba(val)
    assert a == count_doubles_once_numba(val)

    assert a == myrustpyo3.count_doubles_slice(val)

def test_pure_python(benchmark):
    print(benchmark(count_doubles, val))

def test_pure_python_once(benchmark):
    print(benchmark(count_doubles_once, val))

def test_itertools(benchmark):
    print(benchmark(count_doubles_itertools, val))

def test_regex(benchmark):
    print(benchmark(count_doubles_regex, val))

def test_numpy(benchmark):
    print(benchmark(count_doubles_numpy, val))

def test_python_comprehension(benchmark):
    print(benchmark(count_doubles_comprehension, val))

def test_rust(benchmark):
    print(benchmark(myrustlib.count_doubles, val))

def test_rust_once(benchmark):
    print(benchmark(myrustlib.count_doubles_once, val))

def test_rust_bytes_once(benchmark):
    print(benchmark(myrustlib.count_doubles_once_bytes, val))

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

def test_pure_python_once_numba(benchmark):
    print(benchmark(count_doubles_once_numba, val.encode()))

# def test_numpy_numba(benchmark):
#     ng = np.fromstring(val, dtype=np.byte)
#     print(benchmark(count_doubles_numpy_numba, ng))

def test_cython(benchmark):
    print(benchmark(mycythonlib.count_doubles, val))

# def test_c_swig_bytes_once(benchmark):
#     print(benchmark(myclib.count_byte_doubles, val))

def test_rust_pyo3_slice(benchmark):
    print(benchmark(myrustpyo3.count_doubles_slice, val))
