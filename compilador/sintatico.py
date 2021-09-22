from compiladores_1.compilador import lexico, simbolo

class Sintatico:

    def __init__(self, arq):
        self.lexico = lexico.Lexico(arq)
        #self.simbolo = ''
        self.tabela_simbolo = {}
        self.tipo = ''
        self.temp = 0
        self.codigo = ""

    def gera_temp(self):
        temporario = self.temp
        self.temp += 1
        return "t" + str(temporario)

    def code(self, op, arg1, arg2, result):
        self.codigo += op + ";" + arg1 + ";" + arg2 + ";" + result + "\n"

    def obtem_simbolo(self):
        self.simbolo = self.lexico.next_token()

    def verifica_termo(self, termo):
        return (self.simbolo is not None) and (str(self.simbolo.getTermo()) == str(termo))

    def verifica_tipo(self, tipo):
        return (self.simbolo is not None) and (str(self.simbolo.getTipoName()) == str(tipo))

    def verifica_tabela(self, termo):
        return not termo in self.tabela_simbolo.keys()


    def analise(self):
        self.obtem_simbolo()
        self.programa()
        if(self.simbolo is None):
            print("OK")
        else:
            raise RuntimeError(f"Erro sintático esperado no fim de cadeia encontrado: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def programa(self):
        print("programa")
        if self.verifica_termo("program"):
            self.obtem_simbolo()
            if self.verifica_tipo('IDENTIFIER'):
                self.obtem_simbolo()
                self.corpo()
                if self.verifica_termo("."):
                    self.obtem_simbolo()
                else:
                    raise RuntimeError(f"Erro sintático. esperado '.' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'program' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def corpo(self):
        print("corpo")
        self.dc()
        if self.verifica_termo("begin"):
            self.obtem_simbolo()
            self.comandos()
            if self.verifica_termo("end"):
                self.obtem_simbolo()
            else:
                raise RuntimeError(f"Erro sintático. Esperado 'end' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'begin' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def dc(self):
        print("dc")
        if not self.verifica_termo("begin"):
            self.dc_v()
            self.mais_dc()
        else:
            pass

    def dc_v(self):
        print("dc_v")
        self.tipo_var()
        if self.verifica_termo(":"):
            self.obtem_simbolo()
            self.variaveis()
        else:
            raise RuntimeError(f"Erro sintático. Esperado ':' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def tipo_var(self):
        print("tipo_var")
        if self.verifica_termo("integer") or self.verifica_termo("real"):
            self.tipo = self.simbolo.getTipoName()
            self.obtem_simbolo()
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'integer' ou 'real' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def variaveis(self):
        print("variaveis")
        if self.verifica_tipo('IDENTIFIER'):
            if self.verifica_tabela(self.simbolo.getTermo()):
                self.tabela_simbolo[self.simbolo.getTermo()] = simbolo.Simbolo(self.simbolo.getTermo(), self.tipo)
            else:
                raise RuntimeError(f"Erro semântico. Identificador '{self.simbolo.getTermo()}' já encontrado.")
            self.obtem_simbolo()
            self.mais_var()
        else:
            raise RuntimeError(f"Erro sintático. Esperado tipo IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_var(self):
        print("mais_var")
        if self.verifica_termo(","):
            self.obtem_simbolo()
            self.variaveis()
        elif self.verifica_termo(";"):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ',' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_dc(self):
        print("mais_dc")
        if self.verifica_termo(";"):
            self.obtem_simbolo()
            self.dc()
        elif self.verifica_termo("begin"):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ';' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def comandos(self):
        print("comandos")
        self.comando()
        self.mais_comandos()

    def comando(self):
        print("comando")
        if self.verifica_termo("read") or self.verifica_termo("write"):
            self.obtem_simbolo()
            if self.verifica_termo("("):
                self.obtem_simbolo()
                if self.verifica_tipo("IDENTIFIER"):
                    self.obtem_simbolo()
                    if self.verifica_termo(")"):
                        self.obtem_simbolo()
                    else:
                        raise RuntimeError(f"Erro sintático. Esperado ')' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
                else:
                    raise RuntimeError(f"Erro sintático. Esperado tipo IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado '(' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        elif self.verifica_tipo("IDENTIFIER"):
            self.obtem_simbolo()
            if self.verifica_termo(":="):
                self.obtem_simbolo()
                self.expressao()
            else:
                raise RuntimeError(f"Erro sintático. Esperado ':=' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        elif self.verifica_termo("if"):
            self.obtem_simbolo()
            self.condicao()
            if self.verifica_termo("then"):
                self.obtem_simbolo()
                self.comandos()
                self.pfalsa()
                if self.verifica_termo("$"):
                    self.obtem_simbolo()
                else:
                    raise RuntimeError(f"Erro sintático. Esperado '$' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado 'then' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'read', 'write', tipo IDENTIFIER ou 'if' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_comandos(self):
        print("mais_comandos")
        if self.verifica_termo(";"):
            self.obtem_simbolo()
            self.comandos()
        elif (self.verifica_termo("end")
                or self.verifica_termo("$")
                or self.verifica_termo("else")):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ';' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

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
        if self.verifica_termo("-"):
            self.obtem_simbolo()
        elif (self.verifica_tipo("IDENTIFIER")
                or self.verifica_tipo("REAL")
                or self.verifica_tipo("INT")
                or self.verifica_termo("(")):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado '-' ou fator obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def fator(self):
        print("fator")
        if(self.verifica_tipo("IDENTIFIER")
                or self.verifica_tipo("INT")
                or self.verifica_tipo("REAL")):
            self.obtem_simbolo()
        elif self.verifica_termo("("):
            self.obtem_simbolo()
            self.expressao()
            if self.verifica_termo(")"):
                self.obtem_simbolo()
            else:
                raise RuntimeError(f"Erro sintático. Esperado ')' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado '(' ou Tipos INDENTIFER, INT ou REAL obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_fatores(self):
        print("mais_fatores")
        if (not self.verifica_termo("+")
                and not self.verifica_termo("-")
                and not self.verifica_termo(";")
                and not self.verifica_termo(")")
                and not self.verifica_termo("then")
                and not self.verifica_tipo("RELATION")):
            self.op_mul()
            self.fator()
            self.mais_fatores()
        else:
            pass

    def op_mul(self):
        if self.verifica_termo("*") or self.verifica_termo("/"):
            self.obtem_simbolo()
        else:
            raise RuntimeError(f"Erro sintático. Esperado '*' ou '/' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def outros_termos(self):
        print("outros_termos")
        if(not self.verifica_tipo("RELATION")
                and not self.verifica_termo(";")
                and not self.verifica_termo("then")
                and not self.verifica_termo(")")):
            self.op_ad()
            self.termo()
            self.outros_termos()
        else:
            pass

    def op_ad(self):
        print("op_ad")
        if self.verifica_termo("+") or self.verifica_termo("-"):
            self.obtem_simbolo()
        else:
            raise RuntimeError(f"Erro sintático. Esperado '+' ou '-' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def condicao(self):
        print("condicao")
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        print("relacao")
        if self.verifica_tipo("RELATION"):
            self.obtem_simbolo()
        else:
            raise RuntimeError(f"Erro sintático. Esperado tipo RELATION obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def pfalsa(self):
        print("pfalsa")
        if self.verifica_termo("$"):
            pass
        elif self.verifica_termo("else"):
            self.obtem_simbolo()
            self.comandos()
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'else' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")






