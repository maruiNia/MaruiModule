import numpy
from abc import ABC , abstractmethod
import staticEqu
import EnumType

class EquFuncABC(ABC) :
    """
    트리 구조를 가지게 되는 EquFunction의 인터페이스이다.
    """
    def __init__(self) :
        """추클 생성자이다."""

    @abstractmethod
    def preprocessingTerm(self) :
        """
        전처리 과정, 즉 문자열의 배열로 이루어져 있는 함수를 연산 가능한 형태로 정렬한다.
        """
        pass

    @abstractmethod
    def getEquFunc(self) -> str:
        pass

    @abstractmethod
    def getEquVar(self)  -> str:
        pass

    @abstractmethod
    def getEquOper(self)  -> str:
        pass

    def __str__(self) :
        return "식 : " + self.getEquFunc() + " 상수, 변수 : " + self.getEquVar() + " 연산자 : " + self.getEquOper()
    
class EquFunction(EquFuncABC) : 
    """
    함수를 저장하는 식이다.
    Equation에서 사용하는 두가지 값 사이의 관계를 나타낸다.
    기본적인 기능을 사용하며, 이를 통해 값을 바로 계산하는 것이 아닌, 관계식만 저장후 최적화를 통해 식을 축약한 후, Equation에서 연산을 명령하면 연산한다.
        x + 1 같은 것을 저장
    
    해당 객체는 다른 EquFuntion으로 구성되어 있을 수도, 아니면 항으로만 이루어져 있을 수 있다.
    트리구조를 가지며, 해당 객체가 가진 자식의 종류에 따라 가지는 의미가 달라진다.
        EquTerm만 있을 경우 : 말단 함수로 지정한다. 이는 더 이상 하위 함수를 볼 필요가 없는 함수이다.
        EquFuntion이 있을 경우 : 종속 함수이다. 하위 함수를 볼 필요가 있다.
    """

    def __init__(self, equFuncStr : str = "", TestMode = False) :
        """
        만약 str로 함수 정의 할시 사용
        간단하게 식을 지정하고 싶을 때 사용용
        """
        
        self.childrenFunc = []
        self.variables = []
        self.operators = []

        if equFuncStr != "" :
            self.equFunc = equFuncStr
            self.veriablesStr, self.operatorsStr = staticEqu.parse_expression(self.equFunc)

        if TestMode :
            self.__testSet()

    def __testSet(self) :
        """
        y = x를 정의하기 위해 
        말단 함수의 형태를 가진 x를 함수로 지정한다.
        """
        self.equFunc = "x"

    def preprocessingTerm(self):
        """
        식을 구성하는 구성요소를 분석하여 계산 가능한 객체로 변환환
        """
        for var in self.veriablesStr :
            self.variables.append(EquTerm(var, EnumType.TermType.VALUE))
    
    def getEquFunc(self):
        return self.equFunc
    
    def getEquVar(self):
        return self.veriablesStr

    def getEquOper(self):
        return self.operatorsStr

class EquTerm(EquFuncABC) : 
    """
    항을 정의한다.
    수, 변수, 미지수, 상수, 연산자를 정의한다.
    가장 말단이다.
    """
    def __init__(self, name : str, type : EnumType.TermType) :
        """
        항 생성자 이다. 3 이면 상수, x면 변수, *이면 연산자를 리턴한다.

        상수의 equObj는 0을 가진다.
        숫자, 상수, 변수와 함수는 각자 서로 다른 equObj값을 가진다.
            숫자 equObj : 항상 0이다.
            상수 equObj : 상수 스택 값으로, 같은 값을 가진 상수면 같은 값을 가지고, 다른 상수면 ++equObj 된 값을 가진다.
            변수 equObj : 위와 비슷
            함수 equObj : 위와 비슷

        먼저 인식한 순서로 값을 추가하며, 변수는 같은 이름을 가지면 같은 equObj를 가지고, 
        함수는 함수의 종류와 매개변수 값이 같으면 같은 같은 equObj를 가진다.

        """
        self.termName = name # 숫자면 숫자, 상수면 상수이름, 변수면 변수 이름이 저장
        self.termValue = None # 숫자면 int, 상수면 상수수

        self.equObj = None


print(staticEqu.FormulaEqu.parse_expression("x3 + 1"))