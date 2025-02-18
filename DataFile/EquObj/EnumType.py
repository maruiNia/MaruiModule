from enum import Enum

class CalculType(Enum) :
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    # SQU = "^"
    
    def getValues() : 
        return [culoper.value for culoper in CalculType]
    
    def getnames() :
        return [culname.name for culname in CalculType]

class VarType(Enum) :
    VARIABLE = 0
    CONSTANT = 1

    def getValues() : 
        return [culoper.value for culoper in VarType]
    
    def getnames() :
        return [culname.name for culname in VarType]
        
class TermType(Enum) :
    VALUE = VarType.getnames()
    OPERATOR = CalculType.getValues() # 추가 가능


