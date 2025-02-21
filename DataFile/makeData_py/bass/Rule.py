from abc import ABC, abstractmethod
from sympy import symbols, lambdify, Expr, Function, Basic
from sympy.core.symbol import Symbol
import warnings
import numpy as np

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

    Arrtibutes:
        __depth (int) : 트리구조에서 깊이
        __childNumber (int) : 가진 자식의 깊이이
        __expr (Funtion) : 저장된 방정식
    """
    #---------------------------------#       생성자      #---------------------------------#  
    def __init__(self, expr : Basic) :
        """
        입력 : 선형적일 경우 한줄의 입력 리스트 생성, 행렬일 경우
        
        Args:
            __depth (int) : 트리구조에서 원소의 깊이
            __expr (Basic) : 방정식 객체
        """
        self.__depth = 0
        self.__expr = None
        self.__remainDefault = 1

        self.setExpr(expr)

    #---------------------------------#     상속 함수     #---------------------------------#       
    @abstractmethod
    def operation(self) :
        """
        출력값이다. composite이면 하위 RuleLeaf의 출력값을 합치거나 볶거나 뭐하는 식으로 처리한다.
        RuleLeaf는 입력값을 처리하여 출력으로 바꾼다.
        """
        pass

    @abstractmethod
    def __iter__(self) :
        """
        설정후 크기때문에 호출시 마다 출력을 하기 위함
        """
        pass

    @abstractmethod
    def testSet(self) :
        """
        테스트 설정 conposite이면 자식끼리 단순 합, leaf이면 x = y이다.
        """
        pass
    

    #---------------------------------#     공통 함수     #---------------------------------#
    def setExpr(self, expr : Basic) :
        self.__expr = expr
    
    def __iter__(self) :
        """
        지정된 크기 만큼 만들고 리턴합니다.
        iter는 최상위 깊이를 가진 데이터만 수행합니다.
        """
        if self.depthGet() != 0 :
            raise Exception("최상위 트리의 규칙(Rule)이 아닙니다.")

    #---------------------------------#     기타 함수     #---------------------------------#

    def __str__(self):
        """
        클래스 타입, 트리의 깊이, 방정식, 설명 출력력
        """
        type_explain = "클래스 타입 : " + self.__class__.__name__ + "\n" #클래스 타입입

        expr_explain = "함수 식 : " + self.__expr.__str__() + " " # 방정식
        expr_var_explain = "=> " + self.getExpr().free_symbols.__str__()
        expr_explain = expr_explain + expr_var_explain + "\n"
        
        depth_explain = "깊이 : " + self.depthGet().__str__() + "\n" # 깊이


        explain = type_explain + expr_explain + depth_explain

        return explain
    
    def setRemainDefault(self, default : int) :
        self.__remainDefault = default

    def getRemainDefault(self) :
        return self.__remainDefault

    def getExpr(self) :
        return self.__expr

    def getCount(self):
        return self.__count
    
    def getDataSize(self) :
        return self.__data_size
    
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

    #---------------------------------#     클래스 함수     #---------------------------------#
    def inputDivider( rangeCount : list) :
        returnData = []

        if rangeCount[2] == 1 :
            # commonDifference = float(rangeCount[1] - rangeCount[0]) / rangeCount[2]
            returnData.append(rangeCount[0])
        elif rangeCount[2] >= 2 :
            commonDifference = float(rangeCount[1] - rangeCount[0]) / (rangeCount[2] - 1)
            
            for i in range(rangeCount[2]) :
                returnData.append(rangeCount[0] + i * commonDifference)

        return returnData

    def inputProcessing(expr : Basic, input_data : dict) :
        """
        미지수가 모자란 경우....
        """
        varList_expr = expr.free_symbols
        varList_input = input_data.keys()

        return_input_data = {}
        removeKey = []
        
        # 미지수 : [1, 1, 1] 형식 지키기기
        for key, item in input_data.items() :
            if type(key) != Symbol : #Symbol
                raise Exception("미지수의 타입이 Symbol이 아닙니다.")

            if len(item) > 3 : # 배열값 지키기
                temp = item.copy()

                return_input_data[key] = item[:3]
                
                warnings.warn("입력값 중 [시작, 끝 개수]의 3개의 값보다 많은 값을 받았습니다. 처음부터 3개의 값을 제외한 나머지 값은 제외됩니다. : 수정된 값의 미지수 : " + key.__str__() + ", 수정 전 값 : " + temp.__str__() + ", 수정 후 값 : " + item.__str__(), UserWarning)
            
            elif len(item) < 3 :
                temp = item.copy()

                for i in range(3 - len(item)) :
                    item.append(1)
                
                warnings.warn("입력값 중 [시작, 끝 개수]의 3개의 값보다 적은은 값을 받았습니다. 나머지 데이터는 1로 처리 됩니다. : 수정된 값의 미지수 : " + key.__str__() + ", 수정 전 값 : " + temp.__str__() + ", 수정 후 값 : " + item.__str__(), UserWarning)
             
            if item[0] > item[1] :
                temp1 = item.copy()

                temp = item[0]
                item[0] = item[1]
                item[1] = temp

                warnings.warn("입력값 중 처음 값이 뒤의 값보다 큽니다. 두개의 값을 바꿉니다. 수정된 미지수 : " + key.__str__() + ", 수정 전전 값 : " + temp1.__str__() + ", 수정 후 값 : " + item.__str__(), UserWarning)
            
            return_input_data = input_data.copy()

        # 미지수 개수 - warning
        if len(varList_expr) < len(varList_input) :
            for key in varList_expr :
                if key in varList_input :
                    return_input_data[key] = input_data[key]
                else :
                    removeKey.append(key)
            warnings.warn("입력 변수 범위 딕셔너리의 미지수 개수가 저장한 방정식의 미지수 개수보다 많습니다. 방정식에 없는 미지수의 데이터는 제거 됩니다. 제거된 미지수 : " + removeKey.__str__(), UserWarning)

        elif len(varList_expr) > len(varList_input) :
            return_input_data = input_data.copy()
            tempSet = varList_expr - set(varList_input)
            for key in tempSet :
                return_input_data[key] = [1, 1, 1]
            warnings.warn("입력 변수 범위 딕셔너리의 미지수 개수가 저장한 방정식의 미지수 개수보다 적습니다. 입력 딕셔너리에 없는 미지수의 데이터는 1로 생성됩니다. 생성된된 미지수 : " + tempSet.__str__(), UserWarning)

        return return_input_data
    
    def datasetProcessing(dataSetCount : int) :
        return dataSetCount


class RuleLeaf(Rule) :
    """
    rule트리구조의 말단객체이며, 방정식을 저장하고 미리 설정된 입력값으로 호출시마다 데이터, 혹은 데이터 셋을 리턴한다.
    입력값은 사전 설정된 범위값일 수 있으며, 아니면 다른 RuleReaf의 출력값일 수 있다.
    """
    #---------------------------------#       생성자      #---------------------------------#
    def __init__(self, expr : Basic, input_dataDict : dict, data_set_count : int = 1) :
        """ expr : Basic, input_dataDict, data_set_count
        RuleLeaf 생성자이다.
        입력 방식
            exper : 
                x + y 처럼 수식 넣기

            inputData : 변수 : [첫, 끝, 개수] => 딕셔너리리
                input_dataDict = {
                        x : [1, 2, 3],
                        y : [1, 2, 3],
                        z : [1, 2, 3]
                        } 

            data_set_count : 
                int 값값

        Args :
            __inputDataDict (dict) : 데이터 개수, 설정된 범위를 몇등분 하는지 설정한다. 원소 = x(미지수 객체) : [1, 2, 3](시작, 끝, 개수수)
            __dataSetCount (tuple) : 데이터 셋 설정시 한번에 출력할 데이터의 양 (3)
        """
        super(RuleLeaf, self).__init__(expr)

        self.__inputDataDict = Rule.inputProcessing(self.getExpr(), input_dataDict)
        self.__dataSetCount = Rule.datasetProcessing(data_set_count)
        self.varList, self.rangeList, self.sizeList = self.__setVarRange()

        if self.__dataSetCount < 1 :
            raise Exception("분할 데이터 크기는 1이상 일것. 입력된 크기 : " + self.__dataSetCount)

    #---------------------------------#     상속 함수     #---------------------------------#
    def operation(self):
        """
        들어온 모든 값을 전부 연산때린다.
        재귀가 들어간다!
        신난다!!
        """
        returnData = []
        for key, value in self.__inputDataDict.items() :
            returnData.append([key, Rule.inputDivider(value)])

        def recurCal(step : Basic, localList : list) :
            returnTotal = []
            mainList = localList[0] # [key, [valueList]]

            for value in mainList[1] :
                nextStep = step.subs(mainList[0], value)
                if len(localList) == 1 :
                    returnTotal.append(nextStep)
                else :
                    returnTotal.append(recurCal(nextStep, localList[1:]))
            return returnTotal

        return recurCal(self.getExpr(), returnData)
    
    def __iter__(self) :
        super().__iter__()

    def testSet(self):
        return super().testSet()
    
    #---------------------------------#     기타 함수     #---------------------------------#
    def __str__(self):
        __class__.__name__
        return super().__str__()

    def __setVarRange(self) :
        """
        각 변수의 범위값을 튜플 리스트로 가져온다.
        """
        varList = []
        rangeList = []
        sizeList = []

        for i in self.__inputDataDict :
            varList.append(i) # x : ...
            tempList = self.__inputDataDict[i] # ... : [1, 2, 3]

            if len(tempList) != 3 :
                raise Exception("미지수 " + i.__str__() + "의 범위값의 크기가 3이 아닙니다. 입력 값 : " + tempList.__str__())
            rangeList.append(tempList[0:2]) # [1, 2, ...]

            if (tempList[2] < 1) and (type(tempList[2]) != int) :
                raise Exception("미지수 " + i.__str__() + "의 범위속 데이터의 개수가 1 미만이거나 int형이 아닙니다. : " + tempList[2].__str__() + ", 타입 : " + type(tempList[2]).__str__())
            sizeList.append(tempList[2]) # [..., 3]

        return varList, rangeList, sizeList

    def get_input_dataDict(self) :
        return self.__inputDataDict
    
    def get_data_set_count(self) :
        return self.__dataSetCount
        




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
    def __init__(self, expr : Basic): 
        """
        symbols 모듈을 사용해서 식을 저장한다. 아무것도 입력하지 않을 경우, 하위 함수에서 출력되는 값들로 이루어진 값들의 튜플값이 출력이 된다.
        입력할 경우 하위 값의 합이 해당 규칙의 입력값이 되며, 출력값은 한가지 타입의 값이 출력된다.
        """
        super(RuleComposite, self).__init__(expr)
        self.__childNumber = 0

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

    
if __name__ == "__main__" :
    x = symbols("x")
    y = symbols("y")
    z = symbols("z")
    data = np.array([[1, 2],
                     [1, 2],
                     [1, 2]])
    dataSet = {
                x : [1, 2, 3],
                y : [1, 2, 3],
                z : [1, 2, 4]
                }
    a = RuleLeaf(z**2 + x + y + z + 1, dataSet, 1)

    # a = RuleLeaf()
    data = np.array(a.operation())