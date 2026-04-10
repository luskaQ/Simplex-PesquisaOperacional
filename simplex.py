import operacoesPO
import numpy as np

class SimplexFaseI:
    def __init__(self):
        pass

class SimplexFaseII:
    def __init__(self, matrizBasica, indicesMatrizBasica, matrizNaoBasica, indiceMatrizNaoBasica, A, b, c):
        self._x_hat_B = []
        self.x_hat_N = []
        self._A = A
        self._b = b
        self._c = c
        self._matrizBasica = matrizBasica
        self._indicesMatrizBasica = indicesMatrizBasica
        self._matrizNaoBasica = matrizNaoBasica
        self._indiceMatrizNaoBasica = indiceMatrizNaoBasica
        
    def passo1(self):
        matrizBasica_transposta = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        self._x_hat_b = operacoesPO.mult(matrizBasica_transposta, self._b)
        self.x_hat_N = np.zeros(self._n)
        
        
        
