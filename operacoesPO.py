import numpy as np

def detLaplace(A : np.ndarray): #n dimensioal array 
    n = len(A)
    A = A.astype(dtype=np.float64)

    if(n == 1):
        return A[0][0]
    resultado = 0.0
    for i in range(n):
        iMaisJ = pow(-1, i+1) #estamos somando 1, que na matematica é a primeira coluna, mas em codigo é a coluna 0
        valor = A[i][0]
        novoA = np.delete(A, i, axis=0)
        novoA = np.delete(novoA, 0, axis=1)
        resultado += iMaisJ * valor * detLaplace(novoA) #pense que cada submatriz possui um novo somatorio para o det daquela submatriz, que sera retornado para a chamada acima
    return resultado

def matrizIdentidade(n : int):
    identidade = np.zeros((n,n))
    for i in range(n):
        identidade[i][i] = 1
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

A = np.array([[1,2,3],
     [4,7,6],
     [7,8,9]])

print(matrizInversa(A))
print(np.linalg.inv(A))