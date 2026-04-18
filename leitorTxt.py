import numpy as np
import re
import random
import operacoesPO
#o leitor espera coeficiente * variável, e a função objetivo define todas as variáveis do problema (numero total)
class Leitor:
    def __init__(self, caminhoArquivo ):
        self.__caminhoArquivo = caminhoArquivo
        
        self._c= np.empty((0, 0))  #A de Ax da funcao de custo
        self._A= np.empty((0, 0))  #
        self._b = np.empty((0, 0)) # matriz b
        
        self._matrizBasica = np.empty((0,0))
        self._indicesMatrizBasica = []
        
        self._matrizNaoBasica = np.empty((0,0))
        self._indicesMatrizNaoBasica = []


        self._dadosBrutos = []
        self._dadosSemOperadores = []
        self._listasLinhas = []
        self._listaTuplas=[]
        self._isMax = bool
        self._numRestricoes = 0
        self._operadores = []
        self._varDict = dict()
        self.matrizBruta = np.empty((0, 0))
        self._numLinhasA = 0
        self.numColunasA = 0

        self.lerArquivo()
        self.linhasParaListas()
        self.criaTuplas()
        self.encontraOperadores()
        self.encontraMatrizAlvo()
        self.tuplasParaDicionario()
        self.dicionariosParaMatrizes()
        self.adicionaVarFolga()
        self.separaMatrizes()
        self.maxOrMin()
        self.defineMatrizBasicaENaoBasica()
        
        
    def lerArquivo(self):
        with open(self.__caminhoArquivo, 'r') as arquivo:
            self._dadosBrutos = arquivo.readlines()
        pass  
    
    def encontraOperadores(self):
        self._operadores = []
        for linha in self._dadosBrutos:
            if ">=" in linha:
                self._operadores.append(">=")
            elif "<=" in linha:
                self._operadores.append("<=")
            elif ">" in linha:
                self._operadores.append(">")
            elif "<" in linha:
                self._operadores.append("<")
            elif "=" in linha:
                self._operadores.append("=")
        self._operadores.pop(0) # primeira linha sempre vai ser o igual do f = ....
      #  print(self._operadores)
    
    def encontraMatrizAlvo(self): #b
        vetorBSemFormat = []
        for linha in self._dadosBrutos:
            linha = linha.replace(" ", "")
            for op in ["<=", ">=", "=", "<", ">"]:
                pos = linha.find(op)
                if pos != -1:
                    valor = linha[pos + len(op):].strip()
                    vetorBSemFormat.append(valor)
                    break
        vetorBSemFormat.pop(0)
        self._b = np.array(vetorBSemFormat, dtype=float)
       # print(vetorBSemFormat)
        
    def removeOperadores(self):
        self._dadosSemOperadores = []
        for i in self._dadosBrutos:
            linha = i
            linha = linha.replace(" ", "")
            linha = linha.replace("max", "")
            linha = linha.replace("min", "")
            linha = linha.replace("f(x,y)=", "")
            linha = linha.replace("f=", "")
            linha = linha.replace("z=", "")
            pos = linha.find("=")
            if(pos != -1):
                linha = linha.replace(linha[pos:], "")
            pos = linha.find(">")
            if(pos != -1):
                linha = linha.replace(linha[pos:], "")
            pos = linha.find("<")
            if(pos != -1):
                linha = linha.replace(linha[pos:], "")
            self._dadosSemOperadores.append(linha)
        #print(self._dadosSemOperadores)
    #essa funcao so pega a matriz A, nao pega a B
    def linhasParaListas(self):
        self.linhasListas = []
        self.removeOperadores()
        for linha in self._dadosSemOperadores:
            aux = ""
            linha = linha.replace(" ", "")
            #print(linha)
            for j in range(len(linha)):
                if(linha[j].isalnum() or linha[j]== "/" or linha[j] == "." or linha[j] == "," or linha[j] == "-" or linha[j] =="_"):
                    if(linha[j] == "-"):
                        aux += " "
                    aux+=linha[j]
                else:
                    aux +=" "
            #print(aux)
            self._listasLinhas.append(aux.split())
        #print(self._listasLinhas)
        
    #leitor so vai funcionar para coeficiente * variavel -> nessa exata ordem
    def criaTuplas(self):
        self._listaTuplas = []
        idxLinha = 0
        for linha in self._listasLinhas:
            lista =[]
            for expressao in linha:
                tupla = ()
                for i in range(len(expressao)):
                    if(expressao[i].isalpha()):
                        if(expressao[:i] == ""):
                            tupla = (idxLinha,"1", expressao[i:])
                        elif(expressao[:i] == "-"):
                            tupla = (idxLinha, "-1", expressao[i:])
                        else:
                            tupla = (idxLinha, expressao[:i], expressao[i:])
                        break
                lista.append(tupla)
            self._listaTuplas.append(lista)
            idxLinha += 1
       # print(self._listaTuplas)
        
    def tuplasParaDicionario(self):
        dicionario = dict()
        self._varDict = {}
        for i in self._listaTuplas:
            for j in i:
                if re.sub(r'\D', '', j[2]) in dicionario:
                    dicionario[re.sub(r'\D', '', j[2])].append((j[0], j[1])) #(idx, valor)
                else:
                    dicionario[re.sub(r'\D', '', j[2])] = [(j[0], j[1])]
       # print(dicionario)
        self._varDict = dicionario
       # print(self.matrizBruta)
#chaves do dicionario são as colunas, o primerio valor da tupla sao as linhas
    
    def dicionariosParaMatrizes(self):
        numChaves = 0
        self.matrizBruta = np.empty((0, 0))
        numChaves = len(self._varDict)
        self.matrizBruta= np.zeros((len(self._operadores)+1, numChaves))
        #print(self.matrizBruta)
        for chave in self._varDict:
            for i in self._varDict[chave]:
                self.matrizBruta[int(i[0])][int(chave)-1] = float(eval(i[1]))
      #  print(self.matrizBruta)
    
    def adicionaVarFolga(self):
        tamanhoLinhas = self.matrizBruta.shape[0]
        
        for idx, i in enumerate(self._operadores):
            aux = np.zeros((tamanhoLinhas, 1))
            
            if i in ("<=", "<"):
                aux[idx+1] = 1
            elif i in (">=", ">"):
                aux[idx+1] = -1
            else:
                continue
            
            self.matrizBruta = np.column_stack((self.matrizBruta.astype(float), aux.astype(float)))
            
      #  print(self.matrizBruta)
        
    def separaMatrizes(self):
            self._A= self.matrizBruta[1:, :]
            self._c= self.matrizBruta[0, :]
            self.numLinhasA = self._A.shape[0]
            self.numColunasA = self._A.shape[1]
            
            if self._isMax:
                self._c= self._c* -1
            print("f objetivo (c): \n", self._c)
            print("Restrições (A):\n", self._A)
            print("Alvo (b):\n", self._b)    
    
    def maxOrMin(self):
        if("max" in self._dadosBrutos[0].lower()):
            self._isMax = True
        else:
            self._isMax = False
       # print(self._isMax)
       
    def defineMatrizBasicaENaoBasica(self):
        numVariaveis = self.numColunasA
        tamMatrizBasica = self.numLinhasA
        self._matrizBasica = np.ndarray((tamMatrizBasica,0))
        
        while(True):
            self._matrizBasica = np.ndarray((tamMatrizBasica,0))
            self._indicesMatrizBasica = random.sample(range(numVariaveis), tamMatrizBasica) #faltar fazer o verificador de matrizes com det ja calculado
            for i in self._indicesMatrizBasica:
                self._matrizBasica = np.column_stack((self._matrizBasica, self._A[:, i].reshape(-1, 1)))
            if( abs(operacoesPO.detLaplace(self._matrizBasica)) < 1e-9):
                continue
            else:
                break
            
        self._matrizNaoBasica = np.ndarray((tamMatrizBasica, 0))    
        self._indicesMatrizNaoBasica = list(set(range(numVariaveis)) - set(self._indicesMatrizBasica))
        for i in self._indicesMatrizNaoBasica:
                self._matrizNaoBasica = np.column_stack((self._matrizNaoBasica, self._A[:, i].reshape(-1, 1)))
        
        print('\n', self._indicesMatrizBasica)
        print(self._matrizBasica ,'\n')
        print('\n', self._indicesMatrizNaoBasica, '\n')
        print(self._matrizNaoBasica ,'\n')
                
                
    def get_A(self):
        return self._A
    def get_b(self):
        return self._b
    def get_c(self):
        return self._c
    def get_MatrizBasica(self):
        return self._matrizBasica
    def get_IndicesBasicos(self):
        return self._indicesMatrizBasica
    def get_MatrizNaoBasica(self):
        return self._matrizNaoBasica
    def get_IndicesNaoBasicos(self):
        return self._indicesMatrizNaoBasica
            
    
    



    
    

