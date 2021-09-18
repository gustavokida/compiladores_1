from compilador import lexico, token

# from lexico import lexico
# from token import token

if __name__ == "__main__":
    arq = "exemplo.lalg.txt"
    scan = lexico.Lexico(arq)
    t = ""
    print(scan.next_token())

    while(True):
        t = scan.next_token()
        print(t)
        if(t == None):
            break
