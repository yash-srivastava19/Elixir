""" Remove the grad calculation, we have made a similar class. How to document and write clean code is really the important thing here. """
from typing import Any


class MultiplyException(Exception):
    pass

class Complex:
    def __init__(self, real, img=0) -> None:
        self._real = real
        self._img = img


    def __repr__(self):
        return f'Complex({self._real}, {self._img})'
    

    def __add__(self, other):
        assert isinstance(other, Complex) , "Only Complex Addition Allowed"
        return Complex(self._real + other._real, self._img + other._img)
    

    def __neg__(self):
        return Complex(-self._real, -self._img)
    

    def __sub__(self, other):
        assert isinstance(other, Complex) , "Only Complex Subtraction Allowed"
        return self + (-other)
    

    def __pow__(self, other):
        assert isinstance(other, int), "Bro only this as of now?"
        out = Complex(self._real, self._img)   # Basically, same as self
        for _ in range(other):
            out =  out*self

        return out
    
    def __mul__(self, other):
        if isinstance(other, Complex):
            # Then all of that different stuff
            ac = self._real*other._real
            bd = self._img*other._img

            ad = self._real*other._img
            bc = self._img*other._real
            
            return Complex(ac-bd, ad+bc)
        
        elif  isinstance(other, (int, float)) :
            return Complex(self._real + other._real, self._img + other._img)
        
        raise MultiplyException("Can't do that bro.")

    def __eq__(self, other) -> bool:
        assert isinstance(other, Complex), "Nah bro we can't do that"
        return self._real == other._real and self._img == other._img

    def __lt__(self, value):
        return self._real < value or self._img < value




class ComplexValue:
    def __init__(self, data, _children = (), _op = '' ) -> None:
        self.data = data   # here, the data is in complex form
        self.grad = Complex(0, 0)      # Most probably, I believe, the grad is also complex(multi-component for multi-gradient? idk?) 

        # Internal variables for constructing autograd graph
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op


    def __add__(self, other):
        other = other if isinstance(other, ComplexValue) else ComplexValue(other)  # Basically, operations between ScalerValue and other is not allowed.
        out = ComplexValue(self.data + other.data, (self, other), "+")

        def _backward():  # This will be changed.
            self.grad += out.grad
            other.grad += out.grad
        
        out._backward = _backward

        return out


    def _radd__(self, other):
        return  other + self



    def __mul__(self, other):
        other = other if isinstance(other, ComplexValue) else ComplexValue(other)  # Basically, operations between ComplexValue and other is not allowed.
        out = ComplexValue(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad +=  other.data * out.grad     # Try doing this mathematically, you'lll find this intuitive.
            other.grad += self.data  * out.grad
        
        out._backward = _backward

        return out

    def _rmul__(self, other):
        return  other * self


    def __pow__(self, other):
        assert isinstance(other, int),  "Only dis"
        out = ComplexValue(self.data**other, (self, ), f'**{other}')

        def _backward():
            # l1 = 
            print()
            self.grad +=  other * self.data**(other-1) * out.grad   # Try doing this mathematically. A little difficult.
        
        out._backward = _backward

        return out
    

    def relu(self):   # This function doesn't make sense for us right now, but still
        out = ComplexValue(Complex(0, 0) if self.data < 0 else self.data, (self, ), 'ReLU')

        def _backward():
            self.grad +=  (out.data > 0) * out.grad
        
        out._backward = _backward

        return out
    
    def backward(self):
        topo = []       # topological order of all the children in the graph.
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        
        build_topo(self)

        # One variable at a time, apply the chain rule to get the gradient. 
        self.grad = Complex(1, 1)
        for v in reversed(topo):
            v._backward()


    def __neg__(self):
        return self * ComplexValue(Complex(-1, 0))  # Doesn't make sense. Let's see why?
    

    def __sub__(self, other):
        return self + (-other)


    def __rsub__(self, other):
        return other + (-self)

    """ Division doesn't actually makes sense for """
    def __repr__(self):
        return f'ComplexValue(data={str(self.data)}, grad={str(self.grad)})'
