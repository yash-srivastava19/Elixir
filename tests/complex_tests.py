from complex_engine import *

def test_complex_answers():
    # Test 1(Addition, Multiplication, Subtraction) Passed.
    c1 = Complex(-4.0, 0.0)
    c2 = Complex(2.0, 0.0)
    
    # Test 2(With Complex numbers? )
    a = ComplexValue(c1)
    b = ComplexValue(c2)

    c = a + b

    d = a*b + b**3

    c += c + ComplexValue(Complex(1, 0))

    c += ComplexValue(Complex(1, 0)) + c
    e = c - d
    f = e**2

    
    g = a + f
    print(a, f, g)
    a.backward()
    print(a, f, g)


test_complex_answers()
