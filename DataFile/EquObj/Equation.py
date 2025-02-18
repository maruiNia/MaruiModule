import numpy
import EquFunc

class Equation :
    """
    방정식을 저장할 수 있는 클래스이다.
    식을 문자열로 받고 이를 객체로 바꾸며, 값을 넣으면 계산이 가능하다. 
        y = 함수 를 저장
    """
    def __init__(self) :
        """
        문자열을 받아 객체를 생성하는 생성자이다.
        예시로 3x + 4y + z = 1을 넣으면 [3, 4, 1], [x, y, z], [1] 으로 변환된다.
        기본적으로 한가지 식을 저장한다.
        입력받은 값은 간단한 출력값의 형태를 
        """
        self.finalFunc = None

    def setEquFunc(self, equFunc : EquFunc.EquFuncABC) :
        """
        식 저장
        """
        self.Equ = equFunc
    
    def optimization(self) :
        """
        저장된 함수를 최적화 하는 함수이다.
        """
        print("일단 최적화(가라) 중...?")

    def calculation(self, data : numpy.ndarray) :
        """
        최적화 함수를 거쳐 데이터를 계산해 값을 리턴하는 함수
        """
        self.optimization()

        

    def __testOptimSet(self, data : numpy.ndarray) :
        """
        테스트용 최적화 리턴 함수이다. 외부에서 입력받은 ndarray데이터를 처리하고 내보내는 기능을 한다.
        현재 함수 : y = x
        """
        outdata = data
        return outdata
