from abc import ABC, abstractmethod
from sympy import symbols, lambdify, Function

class Rule(ABC) :
    """
    추상 : ruleSet(self), operation(self), depth(self)
    규칙 이다.
    어떤 상태를 저장한다. 기본적으로 개수는 정해지지 않는다.
    지정된 어떤 상태가 있으면 그 상태를 만드는 원소를 리턴한다.
    그 원소는 단순한 좌표일 수도 있으며, 또다른 규칙 일 수도 있다.
    규칙은 컴포사이트 구조를 가진다.
    규칙은 더해줄 수 있다.
    연속적, 이산적 둘다 가능하다. 단 이산적인 경우, 연속적인 규칙을 설정후 이산적으로 바꿔야 한다.

    해당 규칙은 matplotlib를 통해 그래프를 출력 할 수 있다.
    """
    #---------------------------------#       생성자      #---------------------------------#  
    def __init__(self, expr : Function) :
        self.__depth = 0
        self.__childNumber = 0

        self.__expr = None
        self.__freeSymbols = None

        self.setExpr(expr)

    #---------------------------------#     상속 함수     #---------------------------------#       
    def operation(self):
        """
        출력값이다. composite이면 하위 RuleLeaf의 출력값을 합치거나 볶거나 뭐하는 식으로 처리한다.
        RuleLeaf는 입력값을 처리하여 출력으로 바꾼다.
        """
        pass
    

    #---------------------------------#     공통 함수     #---------------------------------#
    def setExpr(self, expr : Function) :
        self.__expr = expr
        self.__freeSymbols = self.__expr.free_symbols
    
    def getExpr(self) :
        return self.__expr

    #---------------------------------#     기타 함수     #---------------------------------#

    def __str__(self):
        """
        트리의 깊이, 방정식, 설명 출력력
        """
        expr_explain = self.__expr.__str__()                            # 방정식
        depth_explain = " 깊이 : " + str.format("%d", self.depthGet() )   # 깊이

        explain = expr_explain + depth_explain

        return explain
    
    def depthGet(self) :
        """
        자신의 깊이를 리턴한다.
        """
        return self.__depth

    def __depthSet(self, depth) :
        """
        자신의 깊이 +1 값을 자식을 받는 동시에 그 자식에게 할당한다. 기본값은 1이다.
        현재 깊이가 얼마나 되는지 저장
        """
        self.__depth = depth





class RuleLeaf(Rule) :
    #---------------------------------#       생성자      #---------------------------------#
    def __init__(self, expr : Function) :
        super(RuleLeaf, self).__init__(expr)
    




class RuleComposite(Rule) :
    """
    규칙 집합이다.
    규칙끼리 영향을 끼칠 수 있다.
    수평적으로 이어진 규칙끼리는 더해지며, 수직적으로 이어진 규칙끼리는 곱해진다.
    값은 단일 값, tensor, nparray, list, 등 가능하다.
    하지만 내부에서는 nparray로 처리한다.
        input : list형 자료
        output : np.array 
    """
    #---------------------------------#       생성자      #---------------------------------#  
    def __init__(self, expr : Function): 
        """
        symbols 모듈을 사용해서 식을 저장한다. 아무것도 입력하지 않을 경우, 하위 함수에서 출력되는 값들로 이루어진 값들의 튜플값이 출력이 된다.
        입력할 경우 하위 값의 합이 해당 규칙의 입력값이 되며, 출력값은 한가지 타입의 값이 출력된다.
        """
        super(RuleComposite, self).__init__(expr)
        self.children = []

    def __init__(self) :
        self.__class__(None) 

    #---------------------------------#     상속 함수     #---------------------------------#
    def operation(self):
        return super().operation()

    #---------------------------------#     객체 함수     #---------------------------------#
    def append(self, rule : Rule) : 
        rule.__depthSet(self.depthGet() + 1)
        self.children.append(rule)

    def testSet(self):
        """
        합쳐지는 구성과 규칙을 테스트용으로 출력한다.
        """
        
    #---------------------------------#     기타 함수     #---------------------------------#
    def __str__(self) :
        return super().__str__()
    
    def getChild(self) :
        return "자식 리턴 함수"

    