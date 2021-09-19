from compiladores_1.compilador import lexico

# from lexico import lexico
# from token import token

if __name__ == "__main__":
    arq = "exemplo.lalg.txt"
    scan = lexico.Lexico(arq)
    t = ""

    while(True):
        t = scan.next_token()
        if(t is None):
            pass
        else:
            print(t.toString())
        if(t == None):
            break
