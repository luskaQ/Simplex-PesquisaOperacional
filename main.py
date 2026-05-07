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
operadores = leitor.get_Operadores()
geradorBases = leitor.get_geradorBases()

verificador = Simplex.VerificaNecessidadeFaseI(A, b, operadores)

A, b, operadores, faseI = verificador.verifica()

if(faseI):
    print("ENTREI NA FASE I")
    simplexI = Simplex.SimplexFaseI(B, indicesB, N, indicesN, A, b, c, operadores)
    A, b, c, indicesB, indicesN = simplexI.loopSimplexI()
    A = leitor.corrigePrecisao(A)
    B = A[:, indicesB]
    print(N, indicesN)
    N = A[:, indicesN]

simplexII = Simplex.SimplexFaseII(B, indicesB, N, indicesN, A, b, c, geradorBases)

print(A,"\n", B)

x = simplexII.loopSimplexII() 

print("Valores de c (f objetivo): ", c)
#print(x, c)
print("Valores x: ", x)
print("Valor de f(x) = ", operacoesPO.mult(x.reshape(1, len(x)), c.reshape(len(x),1)))

''' A = np.array([
    [ 1,  1, 1, 0, 0],
    [ 1, -1, 0, 1, 0],
    [-1,  1, 0, 0, 1]], dtype=float)

b = np.array([[6], [4], [4]], dtype=float)

c = np.array([-1, -2, 0, 0, 0], dtype=float)

B = A[:, [2, 3, 4]].copy()
N = A[:, [0, 1]].copy()

indicesB = [2, 3, 4]
indicesN = [0, 1]

simplex = Simplex.SimplexFaseII(B, indicesB, N, indicesN, A, b, c, geradorBases)
x = simplex.loopSimplexII()

print("\n Valor fixo:", x)
print("\n Valores x: ", x)
print("Valor de f(x) = ", operacoesPO.mult(x.reshape(1, len(x)), c.reshape(len(x),1)))   '''
