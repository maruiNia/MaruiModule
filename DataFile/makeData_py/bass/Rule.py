from abc import ABC, abstractmethod

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
    @abstractmethod
    def __init__(self, explain : str) :
        self.__depth = 0
        self.__explain = explain

    @abstractmethod
    def ruleSet(self) :
        """
        규칙을 설정합니다.
        """
        pass

    @abstractmethod
    def append(self) :
        """
        곱할 규칙을 넣습니다.
        """
        pass

    @abstractmethod
    def operation(self):
        """
        그래프이다.
        """
        pass

    def __str__(self):
        """
        트리의 깊이, 방정식, 설명 출력력
        """
        return self.__explain + " 깊이 : " + str.format("%d", self.depthGet() ) 
    
    def depthGet(self) :
        """
        자신의 깊이를 리턴한다.
        """
        return self.__depth

    def depthSet(self, depth) :
        """
        자신의 깊이 +1 값을 자식을 받는 동시에 그 자식에게 할당한다. 기본값은 1이다.
        현재 깊이가 얼마나 되는지 저장
        """
        self.__depth = depth

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
    
    def __init__(self, explain : str = "규칙 입니다."): 
        super(RuleComposite, self).__init__(explain)
        self.children = []

    def append(self, rule : Rule) :
        rule.depthSet(self.depthGet() + 1)
        self.children.append(rule)

    def ruleSet(self):
        pass
    
    def operation(self):
        print("규칙 수행")

    def testSet(self):
        """
        구현전 규칙의 테스트 모드로 설정하는 것이다.
        기본적으로 y = x 를 규칙으로 설정한다.
        행렬을 이용한다. 
            x^2 + 3x + 1 => [1, 3, 1], [X^2, x, 1] => {{"x" : 2} : 2 , {"x" : 1} : 1, {"1" : 1} : 1}
            2x + 3y + 4z + d => [2, 3, 4, d], [x, y, z, d] => ... 이런식
        """
        

    