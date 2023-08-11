import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

# importing
from complex_engine import *


def test_complex_answers():
    # Test 1(Addition, Multiplication, Subtraction) Passed.
    c1 = Complex(-4.0, 0.0)
    c2 = Complex(0.6, 0.8)
    c3 = Complex(3, 4)

    # Test 2(With Complex numbers? )
    a = ComplexValue(c1)
    b = ComplexValue(c2)

    print(f"c = {c3}, inverse = {c3.conjugate()}")
    # d = a * b + b**3

    # c += c + ComplexValue(Complex(1, 0))

    # c += ComplexValue(Complex(1, 0)) + c
    # e = c - d
    # f = e**2

    # g = a + f
    # print(a, f, g)
    # a.backward()
    # print(a, f, g)


test_complex_answers()
