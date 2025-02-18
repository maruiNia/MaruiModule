import numpy
from abc import ABC , abstractmethod
import EnumType, EquFunc

class EquTerm(EquFunc.EquFuncABC) : 
    """
    항을 정의한다.
    수, 변수, 미지수, 상수, 연산자를 정의한다.
    가장 말단이다.
    """
    def __init__(self, name : str, type : EnumType.TermType) :
        """
        항 생성자 이다. 3 이면 상수, x면 변수, *이면 연산자를 리턴한다.

        termName : 각 값이 가지는 이름이다.
            숫자 name : 이름이 없다. 
            상수 name : 상수 이름이다.
            변수 name : 지정한 이름이다.
            함수 name : 함수 이름이다.
            연산자 name : 연산자 이름름

        termValue : 실제 값이다. 모든 항은 최대로 최적화 이후, 숫자로 값이 계산될 것이므로 숫자 제외한 value 값은 None이다.
            숫자 value : 숫자 값이다.
            상수 value : None
            변수 value : None
            함수 value : None
            연산자 name : None

        equObj : 숫자, 상수, 변수와 함수는 각자 서로 다른 equObj값을 가진다.
            숫자 equObj : 항상 0이다.
            상수 equObj : 상수 스택 값으로, 같은 값을 가진 상수면 같은 값을 가지고, 다른 상수면 ++equObj 된 값을 가진다.
            변수 equObj : 위와 비슷
            함수 equObj : 위와 비슷
            연산자 : None

        먼저 인식한 순서로 값을 추가하며, 변수는 같은 이름을 가지면 같은 equObj를 가지고, 
        함수는 함수의 종류와 매개변수 값이 같으면 같은 같은 equObj를 가진다.

        """
        self.termType = None

        self.termName = None # 숫자면 숫자, 상수면 상수이름, 변수면 변수 이름이 저장
        self.termValue = None # 숫자면 int, 상수면 상수
        self.equObj = None

    #--------------------------------------# 최적화용
    def getNameList(self):
        return self.termName
    
    def getValueList(self):
        return self.termValue
    
    def getEquObjList(self):
        return self.equObj
    
    #--------------------------------------# 출력용
    def getEquVar(self):
        return self.termName
    
    def getEquOper(self):
        return ""

    def getEquFunc(self):
        return self.termName
    
    @abstractmethod
    def getType(self):
        pass

class EquVal(EquTerm) :
    """
    숫자 + 상수 + 변변
    """

class EquCal(EquTerm) :
    """
    연산자자
    """