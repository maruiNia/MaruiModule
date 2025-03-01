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
        self.__iterMode = False

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
        이터레이터 설정
        """
        pass

    @abstractmethod
    def __next__(self) :
        """
        다음 값 호출
        """
        pass

    @abstractmethod
    def testSet(self) :
        """
        테스트 설정 conposite이면 자식끼리 단순 합, leaf이면 x = y이다.
        """
        pass

    @abstractmethod
    def shape(self, iterMode = False) :
        """
        출력할 데이터의 크기를 리턴한다.
        """
        pass


    #---------------------------------#     속성 함수     #---------------------------------#
    def __str__(self):
        """
        클래스 타입, 트리의 깊이, 방정식, 설명 출력력
        """
        type_explain = "클래스 타입 : " + self.__class__.__name__ + "\n" #클래스 타입입

        expr_explain = "함수 식 : " + self.__expr.__str__() + " " # 방정식
        expr_var_explain = "=> " + self.getExpr().free_symbols.__str__()
        expr_explain = expr_explain + expr_var_explain + "\n"
        
        depth_explain = "깊이 : " + self.getDepth().__str__() + "\n" # 깊이


        explain = type_explain + expr_explain + depth_explain

        return explain

    def __depthSet(self, depth) :
        """
        자신의 깊이 +1 값을 자식을 받는 동시에 그 자식에게 할당한다. 기본값은 1이다.
        현재 깊이가 얼마나 되는지 저장
        """
        self.__depth = depth
    
    def setExpr(self, expr : Basic) :
        self.__expr = expr
    
    def __iter__(self) :
        """
        지정된 크기 만큼 만들고 리턴합니다.
        iter는 최상위 깊이를 가진 데이터만 수행합니다.
        """
        if self.getDepth() != 0 :
            raise Exception("최상위 트리의 규칙(Rule)이 아닙니다.")
        
    #---------------------------------#     겟셋 함수     #---------------------------------#
    def getExpr(self) :
        return self.__expr
    
    def getDepth(self) :
        """
        자신의 깊이를 리턴한다.
        """
        return self.__depth
    
    #---------------------------------#     클래스 함수     #---------------------------------#
    def inputDivider( rangeCount : list) :
        """
        범위가 들어오면 해당하는 값을 리턴한다.
        (시작, 끝, 개수) -> [ 리스트 ]
        (1, 5, 5) -> [1, 2, 3, 4, 5]
        """
        returnData = []

        if rangeCount[2] == 1 :
            returnData.append(rangeCount[0])
        elif rangeCount[2] >= 2 :
            commonDifference = float(rangeCount[1] - rangeCount[0]) / (rangeCount[2] - 1)
            
            for i in range(rangeCount[2]) :
                returnData.append(rangeCount[0] + i * commonDifference)

        return returnData

    def inputProcessing(expr : Basic, input_data : dict, data_set_count : list) :
        """
        미지수가 모자란 경우.... 등등 입력한 값이 여러모로 부족할 때 이를 전처리하여 적절한 값으로 변경경
        """
        
        return_input_data = input_data.copy()

        varList_expr = expr.free_symbols
        varList_input = return_input_data.keys()

        removeKey = []

        # 미지수 : [1, 1, 1] 형식 지키기기
        for key, item in return_input_data.items() :
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
            

        # 미지수 개수 - warning
        if len(varList_expr) < len(varList_input) :
            # print(varList_expr)
            # print(varList_input)
            for key in varList_input :
                print(key)
                if key in varList_expr :
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

        # 분할 리스트 (1 * 2) 맞는지 확인
        if len(data_set_count) != 2 :
            raise Exception("1 * 2 형식의 리스트가 아닙니다. 입력된 형식 : " + data_set_count.__str__())
        for i in range(2) :
            if type(data_set_count[i]) != int :
                raise Exception("1 * 2 형식의 정수형 리스트가 아닙니다. 입력된 형식 : " + type(data_set_count[i]).__str__())
            
        return return_input_data



class RuleLeaf(Rule) :
    """
    rule트리구조의 말단객체이며, 방정식을 저장하고 미리 설정된 입력값으로 호출시마다 데이터, 혹은 데이터 셋을 리턴한다.
    입력값은 사전 설정된 범위값일 수 있으며, 아니면 다른 RuleReaf의 출력값일 수 있다.
    """
    #---------------------------------#       생성자      #---------------------------------#
    def __init__(self, expr : Basic, input_dataDict : dict, data_set_count : list = (1, 1)) :
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
                (총 출력할 데이터의 개수, 한번 처리시 리턴할 데이터의 개수)

        Args :
            __inputDataDict (dict) : 데이터 개수, 설정된 범위를 몇등분 하는지 설정한다. 원소 = x(미지수 객체) : [1, 2, 3](시작, 끝, 개수수)
            __dataSetCount (tuple) : 데이터 셋 설정시 한번에 출력할 데이터의 양 (3)
        """
        super(RuleLeaf, self).__init__(expr)
        
        self.__inputDataDict = Rule.inputProcessing(expr, input_dataDict, data_set_count) # 데이터
        self.__shape = self.shape()

        self.varList, self.__rangeList, self.__sizeList = self.__setVarRange() #self.varList 제외 쓰지 말것 간단 체크용

        self.__index = 0 # 이터레이터 인덱스 변수
        self.__iterAmount = data_set_count[0] # 총 개수
        self.__dataSetCount = data_set_count[1] #한번에 처리하고 리턴하는 데이터의 양 (기준 = x기분)
        self.__iterTotalData = None

    #---------------------------------#     상속 함수     #---------------------------------#
    def operation(self):
        """
        들어온 모든 값을 전부 연산때린다.
        재귀가 들어간다!
        신난다!!
        없애버릴꺼다아아아아아
        """
        return self.__oper(self.__mkData())
    
    def __next__(self) :    
        if self.__index < self.__iterAmount :
            culData = []

            tempList = [] # [x , [1, 2, 3]] 용
            tempDataList = [] # [1, 2, 3] 용용
            tempList.append(self.__iterTotalData[0][0])

            for adder in range(self.__dataSetCount) :
                addIndex = self.__index * self.__dataSetCount + adder
                addIndex = addIndex % len(self.__iterTotalData[0][1])
                print(addIndex)
                tempDataList.append(self.__iterTotalData[0][1][addIndex])

            tempList.append(tempDataList)
            culData.append(tempList)   

            for varCount in range(1, len(self.__iterTotalData), 1) :
                culData.append(self.__iterTotalData[varCount])
            
            self.__index += 1

            return self.__oper(culData)
        
        else :
            raise StopIteration

    def __iter__(self) :
        self._index = 0 # 인덱스 초기화
        self.__iterTotalData = self.__mkData()
        return self

    def testSet(self):
        return super().testSet()
    
    def shape(self, iterMode=False):
        if not iterMode :
            return self.__shape()
        else :
            return self.__iter_shape()
    
    #---------------------------------#     속성 함수     #---------------------------------#
    def __oper(self, culDataList : list) :
        returnData = culDataList

        varCount = len(returnData)
        varDataCountList = [len(varDatas[1]) for varDatas in returnData] # x, y, z 순으로 지정 되어 있다면 차례대로 해당 미지수의 데이터 개수가 들어 있다. [x, [1, 2, 3]] -> 3
        varDataCounter = [0 for dataLen in range(varCount)] # 좌표이다. 1. 나머지 계산, 2. if로 계산
        outDataList = [[] for dataLen in range(varCount)] #차원수 만큼의 빈 리스트 원소를 가진다. 하위차원이 꽉차면 해당 하원의 원소전체를 다음 차원의 리스트에 추가한다.

        tempProcessData = {}

        expr = self.getExpr()

        # while 밖 : 0, 0, ..., 0 처리
        outWhile = True
        while(outWhile) :
            #끝 : 최상위 미지수 데이터 개수 확인인
            if len(outDataList[0]) >= varDataCountList[0] :
                "outDataList의 최상위 미지수의 값이 전부 처리됨"
                break

            tempProcessData = {}
            for varCounter in range(varCount) : # {x : 1, y : 2, ...} 로 변수 값 만들기기
                tempList = returnData[varCounter] # 데이터를 가져올 리스트 ([x, [1, 2, 3, 4, ...]])
                tempProcessData[tempList[0]] = tempList[1][varDataCounter[varCounter]] #varDataCounter로 (위치 : [1, 2, 3]) 쌓은 값으로 데이터 가져오기 => dict에 추가

            #처리 : step
            tempValue = expr.subs(tempProcessData)
            print("좌표 = " + varDataCounter.__str__() + ", 값 : " + tempProcessData.__str__() + ", 결과 : " + tempValue.__str__()) # 디버깅용용
            outDataList[-1].append(tempValue)
            varDataCounter[-1] += 1 # 최하위 자리수 추가

            # 좌표 수정
            for varCounter in range(varCount -1, 0, -1) : #미지수를 최하위부터 탐색한다.
                if varDataCounter[varCounter] >= varDataCountList[varCounter] :
                    outDataList[varCounter - 1].append(outDataList[varCounter])
                    varDataCounter[varCounter - 1] += 1

                    varDataCounter[varCounter] = 0
                    outDataList[varCounter] = []
                    
                else :
                    break #해당 varCounter 의 미지수를 전부 처리하지 않을시 나간다.

        # print(varDataCounter) # 디버깅 용
        return outDataList[0] 
    
    def __str__(self):
        __class__.__name__
        return super().__str__()
    
    def __mkData(self):
        """
        지정된 순서로 데이터 만들기, 데이터 필드 만들기
        self.varList 에는 미지수가 순서대로 정렬되어 있는 리스트가 저장되어 있다.
        self.__inputDataDict에는 데이터가 들어 있으며, dict형태로 저장되어 있는 자료를 리스트로 저장하여 순서를 추가한다.
            ex)
                {x : [1, 2, 3], y : [4, 5, 6]}
                self.varList = [x, y] ->
                [[x, [1, 2, 3]], [y, [4, 5, 6]]]
        """
        returnData = []
        for key in self.varList :
            returnData.append([key, Rule.inputDivider(self.__inputDataDict[key])])
            
        return returnData

    def __setVarRange(self) :
        """
        각 변수의 범위값을 튜플 리스트로 가져온다.
        """
        varList = [] #[x, y, z]
        rangeList = [] #[1, 2]
        sizeList = [] # [3, 3, 4]

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

    def __shape(self) :
        shapeList = []
        for key in self.varList :
            shapeList.append(len(self.__inputDataDict[key]))

        return shapeList
    
    def __iter_shape(self) :
        shapeList = []
        for key in self.varList :
            shapeList.append(len(self.__inputDataDict[key]))
        shapeList[0] = self.__dataSetCount
        return shapeList

    
    #---------------------------------#     겟셋 함수     #---------------------------------#

    def get_input_dataDict(self) :
        return self.__inputDataDict
    
    def get_data_set_count(self) :
        return self.__dataSetCount
    
    def changeVarList(self, sequenceList : list) :
        numSequence = list(range(1, len(sequenceList) + 1, 1))

        if len(self.varList) != len(numSequence) :
            raise Exception("미지수 변수와 입력한 리스트의 원소값이 일치하지 않습니다. 미지수 : " + self.varList.__str__() + " 입력한 자료의 개수 : " + sequenceList.__str__())
        
        for i in sequenceList :
            if not(i in numSequence) :
                raise Exception("1, 2, 3, 4... 처럼 1부터 순서대로 모두 들어가게끔 입력해 주세요")
            
        returnVar = []
        for keyNum in sequenceList:
            returnVar.append(self.varList[keyNum - 1])

        self.varList = returnVar




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

    dataSet = {
                x : [1, 10, 10],
                y : [1, 10, 10],
                z : [1, 10, 10]
                }
                # ,z : [1, 3, 3]
    a = RuleLeaf(x + y + z, dataSet, (5, 1))

    for data in a :
        print(data)

