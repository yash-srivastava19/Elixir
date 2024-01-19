""" Remove the grad calculation, we have made a similar class. How to document and write clean code is really the important thing here. """
from typing import Any
from math import *

class MultiplyException(Exception):
    pass


class Complex:
    def __init__(self, real, img=0) -> None:
        self._real = real
        self._img = img

    def __repr__(self):
        if self._img >= 0:
            return f"{self._real}+{self._img}i"
        else:
            return f"{self._real}{self._img}i"

    def __add__(self, other):
        assert isinstance(other, Complex), "Only Complex Addition Allowed"
        return Complex(self._real + other._real, self._img + other._img)

    def __neg__(self):
        return Complex(-self._real, -self._img)

    def __sub__(self, other):
        assert isinstance(other, Complex), "Only Complex Subtraction Allowed"
        return self + (-other)

    def __pow__(self, other):
        assert isinstance(other, int), "Bro only this as of now?"
        out = Complex(self._real, self._img)  # Basically, same as self
        for _ in range(other):
            out = out * self

        return out

    def __mul__(self, other):
        if isinstance(other, Complex):
            # Then all of that different stuff
            ac = self._real * other._real
            bd = self._img * other._img

            ad = self._real * other._img
            bc = self._img * other._real

            return Complex(ac - bd, ad + bc)

        elif isinstance(other, (int, float)):
            return Complex(self._real + other._real, self._img + other._img)

        raise MultiplyException("Can't do that bro.")  # multiplication allowed for only those cases, not the other ones.

    def __truediv__(self, other):
        assert isinstance(other, Complex), "Nah bro we can't do that"
        return self * other.inverse()

        ## Special case for ComplexValue object(Issue 4). This is ok.
        elif isinstance(other, ComplexValue)
            return ComplexValue(Complex(self._real, self._img)) * other    # gradients will be automatically kept tracked of 
        
        raise MultiplyException("Can't do that bro.")
    
    # This also seems ok to me.
    def __eq__(self, other) -> bool:
        assert isinstance(other, Complex), "Nah bro we can't do that"
        return self._real == other._real and self._img == other._img

    # Although I'm not completely sure of how less than works, but as of now, this is OK. 
    def __lt__(self, value):
        return self._real < value or self._img < value

    def mod(self):
        """Modulus of a complex number, x+iy = sqrt(x**2 + y**2)"""
        return sqrt(self._real**2 + self._img**2)

    def conjugate(self):
        out = Complex(self._real, -self._img)
        return out

    # This again is OK.
    def inverse(self):
        if self._img == 0:
            real = 1 / self._real
            img = 0.0
        else:
            real = self.conjugate()._real / self.mod()
            img = self.conjugate()._img / self.mod()
        return Complex(real, img)


class ComplexValue:
    def __init__(self, data, _children=(), _op="") -> None:
        self.data = data  # here, the data is in complex form
        self.grad = Complex(
            0, 0
        )  # Most probably, I believe, the grad is also complex(multi-component for multi-gradient? idk?)

        # Internal variables for constructing autograd graph
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op

    def __add__(self, other):
        other = (
            other if isinstance(other, ComplexValue) else ComplexValue(other)
        )  # Basically, operations between ScalerValue and other is not allowed.
        out = ComplexValue(self.data + other.data, (self, other), "+")

        def _backward():  # This will be changed.
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward

        return out

    def _radd__(self, other):
        return other + self

    def __mul__(self, other):
        other = (
            other if isinstance(other, ComplexValue) else ComplexValue(other)
        )  # Basically, operations between ComplexValue and other is not allowed.
        out = ComplexValue(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += (
                other.data * out.grad
            )  # Try doing this mathematically, you'lll find this intuitive.
            other.grad += self.data * out.grad

            self.grad +=  other.data * out.grad     # Try doing this mathematically, you'll find this intuitive.
            other.grad += self.data  * out.grad
        
        # This backward loop is correct afaik.
        out._backward = _backward

        return out

    def _rmul__(self, other):
        return other * self

    def __pow__(self, other):
        assert isinstance(other, int), "Only dis"
        out = ComplexValue(self.data**other, (self,), f"**{other}")

        def _backward():
            # l1 =
            print()
            self.grad += (
                other * self.data ** (other - 1) * out.grad
            )  # Try doing this mathematically. A little difficult.

        out._backward = _backward

        return out

    def inverse(self):
        pass

    def relu(self):  # This function doesn't make sense for us right now, but still
        out = ComplexValue(
            Complex(0, 0) if self.data < 0 else self.data, (self,), "ReLU"
        )

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward

        return out

    def backward(self):
        topo = []  # topological order of all the children in the graph.
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # One variable at a time, apply the chain rule to get the gradient.
        self.grad = Complex(1, 0)
        for v in reversed(topo):
            v._backward()

    def __sub__(self, other):
        return self + (ComplexValue(Complex(-1, 0)) * other)

    def __rsub__(self, other):
        return other + (ComplexValue(Complex(-1, 0)) * self)

    def __truediv__(self, other):
        return self * other.inverse()

    def __repr__(self):
        return (
            f"ComplexValue:\n\t data = {str(self.data)},\n\t grad = {str(self.grad)}\n"
        )
