import operacoesPO
import numpy as np

class SimplexFaseI:
    def __init__(self):
        pass

class SimplexFaseII:
    def __init__(self, B, b, n):
        self._x_hat_B = []
        self.x_hat_N = []
        self._B = B
        self._b = b
        self._n = n
        
    def passo1(self):
        B_transposto = np.array(operacoesPO.matrizInversa(self._B))
        self._x_hat_b = operacoesPO.mult(B_transposto, self._b)
        self.x_hat_N = np.zeros(self._n)
        
        
        
