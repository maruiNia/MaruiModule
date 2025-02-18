import re
import EnumType

class FormulaEqu :
    """
    식 분석석 기능을 가진 함수 모음집이다.
    """
    def parse_expression(expression: str):
        operators_set = set(EnumType.TermType.OPERATOR.value)  # 연산자 목록을 set으로 변환하여 빠른 탐색
        tokens = re.findall(r'\d+\w+|\w+|\d+|[+\-*/]', expression)  # 숫자+문자, 문자, 숫자, 연산자 추출

        variables = []
        operators_list = []

        for token in tokens:
            if token in operators_set:  # 연산자 처리
                operators_list.append(token)
            elif re.match(r'^\d+\w+$', token):  # 계수+미지수 (예: 5xyz → 5 * x * y * z)
                num, var = re.match(r'(\d+)(\w+)', token).groups()
                variables.append(num)  # 숫자 추가
                operators_list.append('*')  # 곱셈 연산 추가
                variables.extend(var)  # 문자 개별 분리 추가 (xyz → x, y, z)
                operators_list.extend(['*'] * (len(var) - 1))  # 중간 연산자로 * 추가

            elif re.match(r'^\w+$', token):  # 연속된 문자 처리 (xyz → x, y, z)
                variables.extend(token)
                operators_list.extend(['*'] * (len(token) - 1))  # 중간 연산자로 * 추가

            else:
                variables.append(token)  # 숫자 또는 변수 추가

        return variables, operators_list