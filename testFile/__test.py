# 방정식 선언
# 규칙 선언
# 스탬스 선언
# 색상제작 선언
# 데이터 제작

# 1. 방정식 선언 : sympy를 이용해 방정식 선언

from sympy import symbols, lambdify

import numpy as np

x = symbols('x')
y = symbols('y')

expr = y**2 + x + x**2

a = lambdify((x, y), expr)


print(list(expr.free_symbols)[0])
print(type(x))

a = [1, 2, 3]
b = a
b.append(4)
print(a)
# a = {"a" : 1, "b" : 2}
# print(len(a))

# a = [1, 2, 3, 4]
# print(a[1:][0])