import Simplex
import leitorTxt
import operacoesPO
import numpy as np
import time
import sys
def rodar_teste_carga(arquivo_txt, num_testes=1000, valor_esperado=-66.0):
    sucessos = 0
    falhas = 0
    resultados_diferentes = {}

    print(f"Iniciando bateria de {num_testes} testes no arquivo '{arquivo_txt}'...")
    inicio = time.time()

    for i in range(num_testes):
        try:
            # Lemos o arquivo e geramos uma base inicial aleatória (graças ao random.sample no leitor)
            leitor = leitorTxt.Leitor(arquivo_txt)
            
            B = leitor.get_MatrizBasica()
            indicesB = leitor.get_IndicesBasicos()
            N = leitor.get_MatrizNaoBasica()
            indicesN = leitor.get_IndicesNaoBasicos()
            A = leitor.get_A()
            b = leitor.get_b()
            c = np.array(leitor.get_c())
            geradorBases = leitor.get_geradorBases()

            # Instanciamos o Simplex
            simplex = Simplex.SimplexFaseII(B, indicesB, N, indicesN, A, b, c, geradorBases)
            
            # Silenciamos os prints normais redirecionando temporariamente (opcional, mas evita flood no terminal)
            import sys, os
            sys.stdout = open(os.devnull, 'w')
            
            x = simplex.loopSimplexII()
            valor_z = operacoesPO.mult(x.reshape(1, len(x)), c.reshape(len(x),1))
            
            # Restauramos o print
            sys.stdout = sys.__stdout__

            # Arredondamos para evitar falsos positivos por precisão de ponto flutuante
            valor_z_arredondado = round(float(valor_z), 4)

            if valor_z_arredondado == valor_esperado:
                sucessos += 1
            else:
                falhas += 1
                if valor_z_arredondado not in resultados_diferentes:
                    resultados_diferentes[valor_z_arredondado] = 1
                else:
                    resultados_diferentes[valor_z_arredondado] += 1

        except Exception as e:
            print(f"Erro na iteração {i}: {e}")
            falhas += 1

    fim = time.time()

    print("\n" + "="*40)
    print("RELATÓRIO DO TESTE DE CARGA")
    print("="*40)
    print(f"Total de execuções: {num_testes}")
    print(f"Sucessos (z = {valor_esperado}): {sucessos}")
    print(f"Falhas (z != {valor_esperado} ou erros): {falhas}")
    print(f"Tempo total: {(fim - inicio):.2f} segundos")
    
    if resultados_diferentes:
        print("\n⚠️ Resultados inconsistentes encontrados:")
        for res, qtd in resultados_diferentes.items():
            print(f" -> Valor z = {res} ocorreu {qtd} vezes.")
    elif falhas == 0:
        print("\n✅ SUCESSO ABSOLUTO! O seu algoritmo convergiu corretamente em 100% das vezes.")

# Chama a função assumindo que o arquivo se chama "teste.txt" e o valor ótimo é -66
# (O Simplex minimiza o -c, por isso o resultado é -66 para um Max de 66)
if __name__ == "__main__":
    rodar_teste_carga("teste.txt", num_testes=1000, valor_esperado=-11.6)