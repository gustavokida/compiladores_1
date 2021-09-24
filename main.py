#LINK GITHUB: https://github.com/gustavokida/compiladores_1

from compiladores_1.compilador import sintatico

if __name__ == "__main__":
    arq = "exemplo.lalg.txt"
    scan = sintatico.Sintatico(arq)
    scan.analise()
    print()
    print(scan.codigo)
