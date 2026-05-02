import operacoesPO
import numpy as np

class VerificaNecessidadeFaseI:
    def __init__(self, A, b, operadores):
        self._A = np.array(A, dtype=float)
        self._b = np.array(b, dtype=float)
        self._operadores = list(operadores)
        self._faseI = False
        
    
    def inverteRetricao(self, idx):
        self._A[idx] *= -1
        self._b[idx] *= -1        
        if self._operadores[idx] == ">=":
            self._operadores[idx] = "<="
        elif self._operadores[idx] == "<=":
            self._operadores[idx] = ">="
        elif self._operadores[idx] == ">":
            self._operadores[idx] = "<"
        elif self._operadores[idx] == "<":
            self._operadores[idx] = ">"
    
    def verifica(self):
        for i in range(len(self._b)):
            if self._b[i] < -1e-8:
                self.inverteRetricao(i)
        if any(op  ==  ">" or op  ==  ">=" or op  ==  "=" for op in self._operadores):
            self._faseI = True
        
        return self._A, self._b, self._operadores, self._faseI
                
            

class SimplexFaseI:
    def __init__(self, matrizBasica, indicesMatrizBasica, matrizNaoBasica, indicesMatrizNaoBasica, A, b, c, operadores):
        self._x_hat_B = []
        self.x_hat_N = []
        self._A = np.array(A, dtype=float)
        self._b = np.array(b, dtype=float)
        self._c = np.array(c, dtype=float)
        self._matrizBasica = np.array(matrizBasica, dtype=float)
        self._indicesMatrizBasica = list(indicesMatrizBasica)
        self._matrizNaoBasica = np.array(matrizNaoBasica, dtype=float)
        self._indicesMatrizNaoBasica = list(indicesMatrizNaoBasica)
        self._n = len(indicesMatrizNaoBasica)
        self._lambda = []
        self._custos_relativos = []
        self._k = -1
        self._y = -1
        self._epilson = np.inf
        self._indice_saindo_t = -1
        self.__c_B = []
        self.__c_N = []
        self._operadores = operadores
        self._indicesArtificiais = []
        self._A_Artificial = self._A.copy()
        self._c_Artificial = self._c.copy()
        
        self._c_Fase1 = np.zeros(len(self._c))
        self._m = self._A.shape[1]

        
    def criaProblemaArtificial(self):
        self._A_Artificial = self._A.copy()
                
        self._c_Fase1 = np.zeros(len(self._c)) 
        
        self._indicesArtificiais = []
        numDeVarArtificiais = 0
        linha = 0
        for i in self._operadores:
            if i in [">=", ">", "="]:
                aux = np.zeros((self._A.shape[0], 1))
                aux[linha] = 1.0
                self._A_Artificial = np.column_stack((self._A_Artificial.astype(float), aux.astype(float)))
                numDeVarArtificiais += 1
                idx = self._A_Artificial.shape[1] - 1
                self._indicesArtificiais.append(idx)
                
                self._c_Fase1 = np.append(self._c_Fase1, 1.0) 
                
            linha += 1

        if(numDeVarArtificiais == self._A.shape[0]):
            self._casoA = True 
            
    def montaBaseInicial(self):
        m, totalColunas = self._A_Artificial.shape
        self._matrizBasica = operacoesPO.matrizIdentidade(m)
        self._indicesMatrizBasica = []
        self._indicesMatrizNaoBasica = []
        
        for linha in range(m):
            vetor_identidade_esperado = self._matrizBasica[:, linha] #Ex: pegamos [1,0,0], depois
            
            for col in range(totalColunas - 1, -1, -1): #E vemos se existe alguma coluna em A_artificial igual
                coluna_atual = self._A_Artificial[:, col]
                if np.array_equal(coluna_atual, vetor_identidade_esperado):
                    self._indicesMatrizBasica.append(col) #colocamos o idx dessa coluna igual no indices basicos
                    break 
                    
        for col in range(totalColunas):
            if col not in self._indicesMatrizBasica:
                self._indicesMatrizNaoBasica.append(col)
        
        self._matrizNaoBasica = self._A_Artificial[:, self._indicesMatrizNaoBasica] #todas as linhas, mas apenas com as colunas da nao basica
        self.__c_B = self._c_Fase1[self._indicesMatrizBasica]
        self.__c_N = self._c_Fase1[self._indicesMatrizNaoBasica]
        
    def passo1(self):
        
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        self._x_hat_B = operacoesPO.mult(matrizBasica_inversa, self._b, "Fase I, passo1")
        self.x_hat_N = np.zeros(self._n)
        
            
                
    def passo2(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        #passo 2.1
        self.__c_B = np.array(self.__c_B )
        self._lambda = operacoesPO.mult(self.__c_B.reshape(1, -1), matrizBasica_inversa, "faseI passo2.1")#reshape para fazer a matriz ficar com as dimensoes corretas para a multiplicacao, ja que a matriz era unidimensional antes
       
        #isto é, antes era um vetor com tamanho m, agora estou transformando em uma matriz (1, m) 
        
        #reshape funciona assim: (1, -1) -> quero 1 linha e x colunas (o programa descobre quantas colunas automaticamente com o parametro -1)
                              #(-1, 1) -> quero x linhas e 1 coluna
        #util para transpor ou garantir formatos principalmente de arrays que vem como 1D
        
        #passo 2.2
        lambda_T = np.array(self._lambda).reshape(1, -1)  # garante shape (1, m), nesse momento, ja estou transpondo o vetor unidimensional
        self._custos_relativos = []
        for j in range(len(self._indicesMatrizNaoBasica)):
            a_N_j = self._matrizNaoBasica[:, j].reshape(-1, 1)  # garante shape (m, 1)
            c_hat = self.__c_N[j] - operacoesPO.mult(lambda_T, a_N_j, "faseI passo2.2")
            self._custos_relativos.append(c_hat)
        #passo 2.3
        c_hat_N_k = self._custos_relativos[0]
        self._k = 0
        for i in range(1, len(self._custos_relativos)):
            if self._custos_relativos[i] < c_hat_N_k:
                c_hat_N_k = self._custos_relativos[i]
                self._k = i
        
    def passo3(self):
        if(self._custos_relativos[self._k] >= -1e-8):
            for idx in self._indicesMatrizBasica:
                if idx in self._indicesArtificiais:
                    raise Exception("problema inviável: artificial na base")
            return True #solucao atual é otima
    def passo4(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        a_N_k = self._matrizNaoBasica[:, self._k].reshape(-1, 1) # coluna (m, 1)
        self._y = operacoesPO.mult(matrizBasica_inversa, a_N_k, "faseI passo4")
        
    def passo5(self):
        if(np.all(self._y <= 1e-8)):
            return False #pare o algoritmo
        x_hat_b = np.array(self._x_hat_B)
        y = np.array(self._y)
        self._epilson = np.inf # representa infinito positivo
        self._indice_saindo_t = -1
        for i in range(len(y)):
            if y[i] > 1e-8:
                aux = x_hat_b[i]/y[i]
                if aux < (self._epilson - 1e-8):
                    self._epilson = aux
                    self._indice_saindo_t = i
        return True
        
    def passo6(self):        
        
        #o indice que saiu da nao basica vai receber o indice que saiu da basica
        aux = self._indicesMatrizNaoBasica[self._k]
        self._indicesMatrizNaoBasica[self._k] = self._indicesMatrizBasica[self._indice_saindo_t]
        #O item no indice que vai sair da basica vai receber o indice da nao basica que esta saindo de la
        self._indicesMatrizBasica[self._indice_saindo_t] =  aux
        
        
        colunaEntrando = self._matrizNaoBasica[:, self._k].copy() #coluna que vai entrar na basica
        colunaSaindo = self._matrizBasica[:, self._indice_saindo_t].copy() # coluna que vai sair da basica
        
        self._matrizBasica[:, self._indice_saindo_t] = colunaEntrando
        self._matrizNaoBasica[:, self._k] = colunaSaindo
        
        c = np.array(self._c)
        self.__c_B = self._c_Fase1[self._indicesMatrizBasica]
        self.__c_N = self._c_Fase1[self._indicesMatrizNaoBasica]    
        

                
    def loopSimplexI(self):
        self.criaProblemaArtificial()
        self.montaBaseInicial()
        i = 0
        while True:
            self.passo1()
            self.passo2()
            if self.passo3(): 
                break
            self.passo4()
            if not self.passo5():
                raise Exception("Fase I ilimitada — erro de formulação")
            self.passo6()
            # verificação pós-pivô: se ainda há artificiais, continua; senão encerra
            if not any(idx in self._indicesArtificiais for idx in self._indicesMatrizBasica):
                break  # todas as artificiais saíram → Fase II
            i += 1

        colunasReais = [j for j in range(self._A_Artificial.shape[1])
                        if j not in self._indicesArtificiais]
        indicesNaoBasicosReais = [idx for idx in self._indicesMatrizNaoBasica if idx not in self._indicesArtificiais]
        return self._A_Artificial[:, colunasReais], self._b, self._c, self._indicesMatrizBasica, indicesNaoBasicosReais
    

class SimplexFaseII:
    def __init__(self, matrizBasica, indicesMatrizBasica, matrizNaoBasica, indicesMatrizNaoBasica, A, b, c, geradorBases):
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
        
        self._geradorBases = geradorBases           

        
    def passo1(self):
        while True:
            matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
            self._x_hat_B = operacoesPO.mult(matrizBasica_inversa, self._b, "Fase II, passo1")

            if all(x >= -1e-8 for x in self._x_hat_B):
                print("x_hat_B: ", self._x_hat_B, '\n')
                break 
            #numeros negativos, proxima base:
            indices, _ = next(self._geradorBases)  # Exception aqui = sem solução
            self._indicesMatrizBasica = indices
            self._matrizBasica = self._A[:, indices] # Nao preciso pegar a matriz do gerador (ela nao esta atualizada depois da alteracao do verificador), preciso apenas dos indices
            self._indiceMatrizNaoBasica = list(
                set(range(len(self._c))) - set(indices)
            )
            self._matrizNaoBasica = np.ndarray((self._matrizBasica.shape[0], 0))
            for i in self._indiceMatrizNaoBasica:
                self._matrizNaoBasica = np.column_stack(
                    (self._matrizNaoBasica, self._A[:, i].reshape(-1, 1))
                )
            self.__c_B = self._c[self._indicesMatrizBasica]
            self.__c_N = self._c[self._indiceMatrizNaoBasica]

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
        if(self._custos_relativos[self._k] >= -1e-8): #ISSO FOI MUDADO, ANTES ERA 0 AO INVES DE -1e-8 E ESTAVA FUNCIONANDO
            return True #solucao atual é otima
    def passo4(self):
        matrizBasica_inversa = np.array(operacoesPO.matrizInversa(self._matrizBasica))
        a_N_k = self._matrizNaoBasica[:, self._k].reshape(-1, 1) # coluna (m, 1)
        self._y = operacoesPO.mult(matrizBasica_inversa, a_N_k, "faseII passo4")
        
    def passo5(self):
        if(np.all(self._y <= 1e-8)):
            return False #pare o algoritmo
        x_hat_b = np.array(self._x_hat_B)
        y = np.array(self._y)
        self._epilson = np.inf # representa infinito positivo
        self._indice_saindo_t = -1
        for i in range(len(y)):
            if y[i] > 1e-8:
                aux = x_hat_b[i]/y[i]
                if aux < (self._epilson - 1e-8):
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
        i = 0
        while True:
            print(f"Iteração {i}: \n" )
            self.passo1()  
            self.passo2()
            if self.passo3():
                break  # solução ótima
            self.passo4()
            if not self.passo5():
                raise Exception("Problema Ilimitado!")
            self.passo6()
            i+= 1
        
        
        tam_x = len(self._x_hat_B) + len(self.x_hat_N)
        meusX = np.zeros(tam_x)
        for i in range(len(self._x_hat_B)):
            meusX[self._indicesMatrizBasica[i]] = self._x_hat_B[i]
            
        return meusX
  

        

        
        
        
        
        
        
        
        
