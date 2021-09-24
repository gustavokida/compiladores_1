from compiladores_1.compilador import sintatico

# from lexico import lexico
# from token import token

if __name__ == "__main__":
    arq = "exemplo.lalg.txt"
    scan = sintatico.Sintatico(arq)
    scan.analise()
    print()
    print(scan.codigo)