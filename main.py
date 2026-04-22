import Simplex
import operacoesPO
import leitorTxt
import numpy as np

leitor = leitorTxt.Leitor("teste.txt")

input()
print('\n')
B = leitor.get_MatrizBasica()
indicesB = leitor.get_IndicesBasicos()
N = leitor.get_MatrizNaoBasica()
indicesN = leitor.get_IndicesNaoBasicos()
A = leitor.get_A()
b = leitor.get_b()
c = np.array(leitor.get_c())


simplex = Simplex.SimplexFaseII(B, indicesB, N, indicesN, A, b, c)
x = simplex.loopSimplexII()
print("Valores x: ", x)
print("Valor de f(x) = ", operacoesPO.mult(x.reshape(1, len(x)), c.reshape(len(x),1)))