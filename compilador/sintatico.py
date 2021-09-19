from compiladores_1.compilador import lexico, token
import string

class Sintatico:

    def __init__(self, arq):
        self.lexico = lexico.Lexico(arq)
        simbolo = ''
        tabela_simbolo = {}
        tipo = 0

    def obtem_simbolo(self):
        self.simbolo = self.lexico.next_token()

    def verifica_simbolo(self, termo):
        return (self.simbolo is not None) and (self.simbolo.getTermo() == termo)

    def analise(self):
        self.obtem_simbolo()
        self.programa()
        if(self.simbolo is None):
            print("OK")
        else:
            raise RuntimeError("Erro sintático esperado no fim de cadeia encontrado: " + self.simbolo.getTermo())

    def programa(self):
        print("programa")
        if self.simbolo.getTermo() == "program":
            self.obtem_simbolo()
            if self.simbolo.getTipoName() == 'IDENTIFIER':
                self.obtem_simbolo()
                self.corpo()
                if(self.simbolo.getTermo() == "."):
                    self.obtem_simbolo()
                else:
                    raise RuntimeError("Erro sintático. esperado '.'")
            else:
                raise RuntimeError("Erro sintático. Esperado IDENTIFIER")
        else:
            raise RuntimeError("Erro sintático. Esperado 'program'")

    def corpo(self):
        print("corpo")
        self.dc()
        if self.simbolo.getTermo() == "begin":
            self.obtem_simbolo()
            self.comandos()
            if self.simbolo.getTermo() == "end":
                self.obtem_simbolo()
            else:
                raise RuntimeError("Erro sintático. Esperado 'end'")
        else:
            raise RuntimeError("Erro sintático. Esperado 'begin'")


    def dc(self):
        print("dc")
        if self.simbolo.getTermo() != "begin":
            self.dc_v()
            self.mais_dc()
        else:
            pass

    def dc_v(self):
        print("dc_v")
        self.tipo_var()
        if self.simbolo.getTermo() == ":":
            self.obtem_simbolo()
            self.variaveis()
        else:
            raise RuntimeError("Erro sintático. Esperado ':'")

    def tipo_var(self):
        print("tipo_var")
        if self.simbolo.getTermo() == 'integer' or self.simbolo.getTermo() == 'real':
            self.obtem_simbolo()
        else:
            raise RuntimeError("Erro sintático. Esperado 'integer' ou 'real'")


    def variaveis(self):
        print("variaveis")
        if self.simbolo.getTipoName() == 'IDENTIFIER':
            self.obtem_simbolo()
            self.mais_var()
        else:
            raise RuntimeError("Erro sintático. Esperado tipo IDENTIFIER")

    def mais_var(self):
        print("mais_var")
        if self.simbolo.getTermo() == ",":
            self.obtem_simbolo()
            self.variaveis()
        elif self.simbolo.getTermo() == ";":
            pass
        else:
            raise RuntimeError("Erro sintático. Esperado ','")

    def mais_dc(self):
        print("mais_dc")
        if self.simbolo.getTermo() == ";":
            self.obtem_simbolo()
            self.dc()
        elif self.simbolo.getTermo() == "begin":
            pass
        else:
            raise RuntimeError("Erro sintático. Esperado ';'")

    def comandos(self):
        print("comandos")
        self.comando()
        self.mais_comandos()

    def comando(self):
        print("comando")
        if self.simbolo.getTermo() == "read" or self.simbolo.getTermo() == "write":
            self.obtem_simbolo()
            if self.simbolo.getTermo() == "(":
                self.obtem_simbolo()
                if self.simbolo.getTipoName() == "IDENTIFIER":
                    self.obtem_simbolo()
                    if self.simbolo.getTermo() == ")":
                        self.obtem_simbolo()
                    else:
                        raise RuntimeError("Erro sintático. Esperado ')'")
                else:
                    raise RuntimeError("Erro sintático. Esperado tipo IDENTIFIER")
            else:
                raise RuntimeError("Erro sintático. Esperado '('")
        elif self.simbolo.getTipoName() == "IDENTIFIER":
            self.obtem_simbolo()
            if self.simbolo.getTermo() == ":=":
                self.obtem_simbolo()
                self.expressao()
            else:
                raise RuntimeError("Erro sintático. Esperado ':='")
        elif self.simbolo.getTermo() == "if":
            self.obtem_simbolo()
            self.condicao()
            if self.simbolo.getTermo() == "then":
                self.obtem_simbolo()
                self.comandos()
                self.pfalsa()
                if self.simbolo.getTermo() == "$":
                    self.obtem_simbolo()
                else:
                    raise RuntimeError("Erro sintático. Esperado '$'")
            else:
                raise RuntimeError("Erro sintático. Esperado 'then'")
        else:
            raise RuntimeError("Erro sintático. Esperado 'read', 'write', tipo IDENTIFIER ou 'if'")

    def mais_comandos(self):
        print("mais_comandos")
        if self.simbolo.getTermo() == ";":
            self.obtem_simbolo()
            self.comandos()
        elif (self.simbolo.getTermo() == "end"
                or self.simbolo.getTermo() == "$"
                or self.simbolo.getTermo() == "else"):
            pass
        else:
            raise RuntimeError("Erro sintático. Esperado ';'")

    def expressao(self):
        print("expressao")
        self.termo()
        self.outros_termos()

    def termo(self):
        print("termo")
        self.op_un()
        self.fator()
        self.mais_fatores()

    def op_un(self):
        print("op_un")
        if self.simbolo.getTermo() == "-":
            self.obtem_simbolo()
        elif (self.simbolo.getTipoName() == "IDENTIFIER"
                or self.simbolo.getTipoName() == "REAL"
                or self.simbolo.getTipoName() == "INT"
                or self.simbolo.getTermo() == "("):
            pass
        else:
            raise RuntimeError("Erro sintático. Esperado '-' ou fator")

    def fator(self):
        print("fator")
        if(self.simbolo.getTipoName() == "IDENTIFIER"
                or self.simbolo.getTipoName() == "INT"
                or self.simbolo.getTipoName() == "REAL"):
            self.obtem_simbolo()
        elif self.simbolo.getTermo() == "(":
            self.obtem_simbolo()
            self.expressao()
            if self.simbolo.getTermo() == ")":
                self.obtem_simbolo()
            else:
                raise RuntimeError("Erro sintático. Esperado ')'")
        else:
            raise RuntimeError("Erro sintático. Esperado '(' ou Tipos INDENTIFER, INT ou REAL")

    def mais_fatores(self):
        print("mais_fatores")
        if (self.simbolo.getTermo() != "+"
                and self.simbolo.getTermo() != "-"
                and self.simbolo.getTermo() != ";"
                and self.simbolo.getTermo() != ")"
                and self.simbolo.getTermo() != "then"
                and self.simbolo.getTipoName() != "RELATION"):
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            pass

    def op_mul(self):
        if self.simbolo.getTermo() == "*" or self.simbolo.getTermo() == "/":
            self.obtem_simbolo()
        else:
            raise RuntimeError("Erro sintático. Esperado '*' ou '/'")


    def outros_termos(self):
        print("outros_termos")
        if(self.simbolo.getTipoName() != "RELATION"
                and self.simbolo.getTermo() != ";"
                and self.simbolo.getTermo() != "then"
                and self.simbolo.getTermo() != ")"):
            self.op_ad()
            self.termo()
            self.outros_termos()
        else:
            pass

    def op_ad(self):
        print("op_ad")
        if self.simbolo.getTermo() == "+" or self.simbolo.getTermo() == "-":
            self.obtem_simbolo()
        else:
            raise RuntimeError("Erro sintático. Esperado '+' ou '-'")

    def condicao(self):
        print("condicao")
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        print("relacao")
        if self.simbolo.getTipoName() == "RELATION":
            self.obtem_simbolo()
        else:
            raise RuntimeError("Erro sintático. Esperado tipo RELATION")

    def pfalsa(self):
        print("pfalsa")
        if self.simbolo.getTermo() == "$":
            pass
        elif self.simbolo.getTermo() == "else":
            self.obtem_simbolo()
            self.comandos()
        else:
            raise RuntimeError("Erro sintático. Esperado 'else'")






