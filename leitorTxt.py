import numpy as np
import re
#o leitor espera coeficiente * variável, e a função objetivo define todas as variáveis do problema (numero total)
class Leitor:
    def __init__(self, caminhoArquivo ):
        self.__caminhoArquivo = caminhoArquivo
        
        self._custo = np.array #A de Ax da funcao de custo
        self._limitacoes = np.ndarray #
        self._matrizAlvo = np.ndarray # matriz b
        
        self._dadosBrutos = []
        self._dadosSemOperadores = []
        self._listasLinhas = []
        self._listaTuplas=[]
        self._isMax = bool
        self._numRestricoes = 0
        self._operadores = []
        self._varDict = dict()
        #self.lerArquivo()
        #self.linhasParaListas()
        #self.criaTuplas()
        
        
    def lerArquivo(self):
        with open(self.__caminhoArquivo, 'r') as arquivo:
            self._dadosBrutos = arquivo.readlines()
        pass  
    
    def encontraOperadores(self):
        self._operadores = []
        for linha in self._dadosBrutos:
            posMaior = linha.find(">")
            if(posMaior != -1):
                self._operadores.append(">")
            else:
                posMenor = linha.find("<")
                if(posMenor != -1):
                    self._operadores.append("<")
                else:
                    self._operadores.append("=")
        print(self._operadores)
    
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
        print(vetorBSemFormat)
        
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
        print(self._listaTuplas)
        
    def tuplasParaDicionario(self):
        dicionario = dict()
        for i in self._listaTuplas:
            for j in i:
                if j[1] in dicionario:
                    dicionario[j[1]].append(j[0])
                else:
                    dicionario[j[1]] = [j[0]]
        print(dicionario)
        self._varDict = dicionario

    
    def dicionariosParaMatrizes(self):
        for chave in self._varDict:
            for i in self._varDict[chave]:
                
    
    
leitor = Leitor("teste.txt")
leitor.lerArquivo()
leitor.linhasParaListas()
leitor.criaTuplas()
leitor.encontraOperadores()
leitor.encontraMatrizAlvo()
leitor.tuplasParaDicionario()
leitor.dicionariosParaMatrizes()


    
    

