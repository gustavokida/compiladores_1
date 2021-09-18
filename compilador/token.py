from enum import Enum

class Type(Enum):
    IDENTIFIER = 0
    INT = 1
    REAL = 2
    SIMBOLO = 3

class Token:

    def __init__(self, tipo, termo):
        self.tipo = tipo.value
        self.termo = termo
    
    def getTipo(self, tipo):
        return self.tipo
    
    def setTipo(self, tipo):
        self.tipo = tipo

    def getTermo(self, termo):
        return self.termo
    
    def setTermo(self, termo):
        self.termo = termo
        
    def toString(self):
        return ("Token [" + str(self.tipo) + ", " + self.termo + "]")