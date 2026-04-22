import operacoesPO
import numpy as np

class SimplexFaseI:
    def __init__(self):
        pass

class SimplexFaseII:
    def __init__(self, matrizBasica, indicesMatrizBasica, matrizNaoBasica, indicesMatrizNaoBasica, A, b, c):
        self._x_hat_B = []
        self.x_hat_N = []
        self._A = np.array(A, dtype=float)
        self._b = np.array(b, dtype=float)
        self._c = np.array(c, dtype=float)
        self._matrizBasica = np.array(matrizBasica, dtype=float)
        self._indicesMatrizBasica = list(indicesMatrizBasica)
        self._matrizNaoBasica = np.array(matrizNaoBasica, dtype=float)
        self._indiceMatrizNaoBasica = list(indicesMatrizNaoBasica)
        self._n = len(indicesMatrizNaoBasica)
        self._lambda = []
        self._custos_relativos = []
        self._k = -1
        self._y = -1
        self._epilson = np.inf
        self._indice_saindo_t = -1

        self.__c_B = self._c[self._indicesMatrizBasica]
        self.__c_N = self._c[self._indiceMatrizNaoBasica]
        

        
    def passo1(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        
        #VERIFICAR SE ALGUM X É MENOR QUE 0, SE SIM, VOLTAR PARA A RANDOMIZACAO DE MATRIZ BASICA, GUARDAR PERMUTACOES QUE JA FORAM
        #VER O TOTAL DE POSSIBILIDADES, SE TODAS FOREM USADAS E NENHUMA FOR VALIDA, O PROBLEMA N TEM SOLUCAO
        
        self._x_hat_B = operacoesPO.mult(matrizBasica_inversa, self._b, "Fase II, passo1")
        self.x_hat_N = np.zeros(self._n)
        
    def passo2(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        #passo 2.1
        self._lambda = operacoesPO.mult(self.__c_B.reshape(1, -1), matrizBasica_inversa, "faseII passo2.1")#reshape para fazer a matriz ficar com as dimensoes corretas para a multiplicacao, ja que a matriz era unidimensional antes
        #isto é, antes era um vetor com tamanho m, agora estou transformando em uma matriz (1, m) 
        
        #reshape funciona assim: (1, -1) -> quero 1 linha e x colunas (o programa descobre quantas colunas automaticamente com o parametro -1)
                              #(-1, 1) -> quero x linhas e 1 coluna
        #util para transpor ou garantir formatos principalmente de arrays que vem como 1D
        
        #passo 2.2
        lambda_T = np.array(self._lambda).reshape(1, -1)  # garante shape (1, m), nesse momento, ja estou transpondo o vetor unidimensional
        self._custos_relativos = []
        for j in range(len(self._indiceMatrizNaoBasica)):
            a_N_j = self._matrizNaoBasica[:, j].reshape(-1, 1)  # garante shape (m, 1)
            c_hat = self.__c_N[j] - operacoesPO.mult(lambda_T, a_N_j, "faseII passo2.2")
            self._custos_relativos.append(c_hat)
        #passo 2.3
        c_hat_N_k = self._custos_relativos[0]
        self._k = 0
        for i in range(1, len(self._custos_relativos)):
            if self._custos_relativos[i] < c_hat_N_k:
                c_hat_N_k = self._custos_relativos[i]
                self._k = i
        
    def passo3(self):
        if(self._custos_relativos[self._k] >= 0):
            return True #Solucao atual é otima
    def passo4(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        a_N_k = self._matrizNaoBasica[:, self._k].reshape(-1, 1) # coluna (m, 1)
        self._y = operacoesPO.mult(matrizBasica_inversa, a_N_k, "faseII passo4")
        
    def passo5(self):
        if(np.all(self._y <= 0)):
            return False #pare o algoritmo
        x_hat_b = np.array(self._x_hat_B)
        y = np.array(self._y)
        self._epilson = np.inf # representa infinito positivo
        self._indice_saindo_t = -1
        for i in range(len(y)):
            if y[i] > 0:
                aux = x_hat_b[i]/y[i]
                if aux < self._epilson:
                    self._epilson = aux
                    self._indice_saindo_t = i
        return True
        
    def passo6(self):        
        
        #o indice que saiu da nao basica vai receber o indice que saiu da basica
        aux = self._indiceMatrizNaoBasica[self._k]
        self._indiceMatrizNaoBasica[self._k] = self._indicesMatrizBasica[self._indice_saindo_t]
        #O item no indice que vai sair da basica vai receber o indice da nao basica que esta saindo de la
        self._indicesMatrizBasica[self._indice_saindo_t] =  aux
        
        
        colunaEntrando = self._matrizNaoBasica[:, self._k].copy() #coluna que vai entrar na basica
        colunaSaindo = self._matrizBasica[:, self._indice_saindo_t].copy() # coluna que vai sair da basica
        
        self._matrizBasica[:, self._indice_saindo_t] = colunaEntrando
        self._matrizNaoBasica[:, self._k] = colunaSaindo
        
        c = np.array(self._c)
        self.__c_B = c[self._indicesMatrizBasica]
        self.__c_N = c[self._indiceMatrizNaoBasica]
        
        
    def loopSimplexII(self):
        while True:
            self.passo1()  
            self.passo2()
            if self.passo3():
                break  # solução ótima
            self.passo4()
            if not self.passo5():
                raise Exception("Problema Ilimitado!")
            self.passo6()
        
        
        tam_x = len(self._x_hat_B) + len(self.x_hat_N)
        meusX = np.zeros(tam_x)
        for i in range(len(self._x_hat_B)):
            meusX[self._indicesMatrizBasica[i]] = self._x_hat_B[i]
            
        return meusX
  
"""A = np.array([
    [ 1,  1, 1, 0, 0],
    [ 1, -1, 0, 1, 0],
    [-1,  1, 0, 0, 1]], dtype=float)

b = np.array([[6], [4], [4]], dtype=float)

c = np.array([-1, -2, 0, 0, 0], dtype=float)

B = A[:, [2, 3, 4]].copy()
N = A[:, [0, 1]].copy()

indicesB = [2, 3, 4]
indicesN = [0, 1]

simplex = SimplexFaseII(B, indicesB, N, indicesN, A, b, c)
x = simplex.loopSimplexII()
print("Valores x: ", x)
print("Valor de f(x) = ", operacoesPO.mult(x.reshape(1, len(x)), c.reshape(len(x),1)))"""      
        

        
        
        
        
        
        
        
        
