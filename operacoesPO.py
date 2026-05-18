import numpy as np

def detLaplace(A : np.ndarray): #n dimensioal array 
    #return np.linalg.det(A)
    n = len(A)
    A = A.astype(dtype=np.float64)
    if (n == 3):
        return detSarrus(A)
    if (n == 2):
        return (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])
    if(n == 1):
        return A[0][0]
    resultado = 0.0
    for i in range(n):
        iMaisJ = pow(-1, i) # i_matematica = i_codigo + 1 ; (i+1) + 1 = i + 2 = i (pois a base é -1 e j é fixo em 1)
        valor = A[i][0]
        novoA = np.delete(A, i, axis=0)
        novoA = np.delete(novoA, 0, axis=1)
        
        resultado += iMaisJ * valor * detLaplace(novoA) #pense que cada submatriz possui um novo somatorio para o det daquela submatriz, que sera retornado para a chamada acima
    return resultado
def detSarrus(matriz : np.ndarray):
    positivos1 = (matriz[0][0]*matriz[1][1]*matriz[2][2])
    positivos2 = (matriz[0][1]*matriz[1][2]*matriz[2][0])
    positivos3 = (matriz[0][2]*matriz[1][0]*matriz[2][1])
    positivos = positivos1 + positivos2 + positivos3

    negativos1 =(matriz[0][2]*matriz[1][1]*matriz[2][0])*(-1)
    negativos2 = (matriz[0][0]*matriz[1][2]*matriz[2][1])*(-1)
    negativos3 = (matriz[0][1]*matriz[1][0]*matriz[2][2])*(-1)
    negativos = negativos1 + negativos2 + negativos3
    det = positivos + negativos
    return det

def matrizIdentidade(n : int):
    identidade = np.zeros((n,n))
    for i in range(n):
        identidade[i][i] = 1.0
    return identidade

def matrizInversa(A : np.ndarray):
    if abs(detLaplace(A)) < 1e-9: #como estamos lidando com floats, é melhor verificar se é um resultado muito pequeno (absoluto), isto é, muito próximo de 0
        return Exception("Matriz especificada sem inversa")
    n = len(A)
    identidade = matrizIdentidade(n)
    matrizAumentada = np.column_stack((A, identidade))
    matrizAumentada = matrizAumentada.astype(float)
    for i in range(n):
        pivo = matrizAumentada[i][i] 
        if pivo == 0:
            for k in range(i+1, n):
                if matrizAumentada[k][i] != 0:
                    matrizAumentada[[i, k]] = matrizAumentada[[k, i]] #pegue linha i e k e troque por k e i
                    pivo = matrizAumentada[i][i]
                    break
            else:
                raise Exception("Sistema sem solução única (pivô zero)")
        for j in range(i+1, n):
            multiplicador =  matrizAumentada[j][i] / pivo 
            matrizAumentada[j] = matrizAumentada[j] - multiplicador * matrizAumentada[i]
    #segundo FOR nao precisa de verificao de pivo == 0, o primeiro for ja garante toda a diagonal principal != 0
    for i in range(n-1, -1, -1): #agora o for começa em [n-1][n-1] e vai diminuindo zerando em cima
        pivo = matrizAumentada[i][i] 
        for j in range(i-1, -1, -1):
            multiplicador =  matrizAumentada[j][i] / pivo 
            matrizAumentada[j] = matrizAumentada[j] - multiplicador * matrizAumentada[i]
    for i in range(n):
        matrizAumentada[i] = matrizAumentada[i] / matrizAumentada[i][i]
    #print(matrizAumentada)
    return matrizAumentada[0:n, n:n*2]

def mult(A : np.ndarray, B : np.ndarray, localErro = ""): #sempre que chamar uma mult, colocar o local onde ela esta sendo chamada para facilitar debuging
    if(A.ndim == 1):
        A=A.reshape(1, -1)
    if(B.ndim == 1):
        B=B.reshape(-1, 1)
    
    linhasA, colunasA = A.shape[0], A.shape[1]
    linhasB, colunasB = B.shape[0], B.shape[1]
    
    if colunasA == linhasB:
        resultado = np.zeros((linhasA, colunasB))
        
        for i in range(linhasA):
            for j in range(colunasB):
                valor = 0
                for k in range(colunasA): #como o num de colunas de A == num de linhas de B, podemos usar k para iterar pelas colunas e linhas de respectivamente A e B
                    valor += A[i][k] * B[k][j]
                resultado[i][j] = valor
        return resultado.squeeze()
    else:
        raise Exception(f" {localErro}: Matrizes {A.shape} e {B.shape} não permite multiplicaçao")
    
def pivoteamento_parcial(matrizA : np.ndarray, matrizB : np.ndarray):
    n = len(matrizA)
    x = np.zeros(n)
    matrizAumentada = np.column_stack((matrizA, matrizB)).astype(float)
    
    for i in range(n):
        linha_pivo = i
        valor_max = abs(matrizAumentada[i][i])
        for j in range(i+1, n):
            if abs(matrizAumentada[j][i]) > valor_max:
                linha_pivo = j
                valor_max = abs(matrizAumentada[j][i])
        if linha_pivo != i:
            matrizAumentada[[i, linha_pivo]] = matrizAumentada[[linha_pivo, i]]
        pivo = matrizAumentada[i][i]
        if abs(pivo) < 1e-10:
            raise Exception("Divisao por 0 - sem solução única")
        for j in range(i+1, n):
            multiplicador = matrizAumentada[j][i] / pivo
            matrizAumentada[j] -= multiplicador * matrizAumentada[i]

    for i in range(n-1, -1, -1):
        soma = matrizAumentada[i][-1]
        for j in range(i+1, n):
            soma -= matrizAumentada[i][j] * x[j]
        x[i] = soma / matrizAumentada[i][i]

    return x
    