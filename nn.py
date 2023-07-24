import random
from engine import ScalerValue

class Module:

    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):  # Will be overwritten
        return []
    

class Neuron(Module):
    """ A simple neuron. """
    def __init__(self, n_in, non_lin = True) -> None:
        self.w = [ScalerValue(random.uniform(-1, 1)) for _ in range(n_in)]
        self.b = ScalerValue(0)

        self.non_lin = non_lin


    def __call__(self, x):
        act = sum((wi*xi for wi,xi in zip(self.w,x)), self.b)
        return act.relu() if self.non_lin else act
    

    def parameters(self):
        return self.w + [self.b]
    

    def __repr__(self) -> str:
        return f"{'ReLU' if self.non_lin else 'Linear'}Neuron({len(self.w)})"


class Layer(Module):
    def __init__(self, n_in, n_out, **kwargs) -> None:
        self.neurons = [Neuron(n_in, **kwargs) for _ in range(n_out)]

    
    def __call__(self, x):
        out = [n(x) for n in self.neurons]
        return out[0] if len(out) == 1 else out
    

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]
    

    def __repr__(self) -> str:
        neu_str = ", ".join(str(n) for n in self.neurons)
        
        repr_obj = f""" Layer of:[
            {neu_str}] """
        
        return repr_obj


class MLP(Module):

    def __init__(self, n_in, n_outs) -> None:
        sz = [n_in] + n_outs
        self.layers = [Layer(sz[i], sz[i+1], non_lin = i!=len(n_outs)-1) for i in range(len(n_outs))]

    
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]
    

    def __repr__(self) -> str:
        lay_str = "\n".join(str(l) for l in self.layers)
        repr_obj = f""" 
        MLP of:[
            {lay_str}] """
        return repr_obj
