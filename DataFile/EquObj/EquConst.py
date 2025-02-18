from enum import Enum
import math

class EquConst(Enum) :
    PI = math.pi
    A = 1.1 #일단 한글자 상수 선언

    def getValues() : 
        return [culoper.value for culoper in EquConst]
    
    def getnames() :
        return [culname.name for culname in EquConst]