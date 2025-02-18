from abc import ABC, abstractmethod

class Stmap(ABC) :
    """
    Stamp기본 객체이다.
    stamp의 목적은 일정한 이 클래스를 상속받은 여러 클래스들이 makecolorobj클래스에 의해 자동 생성되는 것을 목표로 한다.
    해당 클래스를 상속받은 클래스는 기본적으로 iterator의 특징을 가진다.
        __init__() : 규칙을 매개변수로 가진다. 받아온 기본적으로 x = y인 선형 방정식이 적용된다.

        __iter__() : 호출때 규칙에 따라 다음 상태를 리턴한다. 
                    (ex : ruleStamp가 어떤 선형방정식으로 설정되어 있을때, 해당 함수 호출시 규칙에 맞는 다음 상태 리턴)
    """
    def __init__(self) :
        """
        생성자 이다.
        기본 규칙을 설정한다.
        """
        
    @abstractmethod
    def __iter__(self) :
        """
        호출시 다음 상태 리턴
        """
        pass