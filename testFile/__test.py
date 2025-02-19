# 방정식 선언
# 규칙 선언
# 스탬스 선언
# 색상제작 선언
# 데이터 제작

# 1. 방정식 선언 : sympy를 이용해 방정식 선언

from sympy import symbols, lambdify

x = symbols("x")
a = x + 1

b = x + 1

c = a + b

print(c)

expr = lambdify(x, a)

print()