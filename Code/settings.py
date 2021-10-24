from sympy import *

y_0 = 0
x_0 = 1
X = 8
grid = 10
n_0 = 10
N = 20
title = 'y\' = y/x - x*exp(y/x)'
equation = '(-x*ln(x+C))'
general_equation = '(-x*ln(x+C))'
diff_equation = '((y/x)-(x*ep(y/x)))'
constant = 'ep(-y/x)-x'


def find_const(x, y):
    global equation, general_equation, constant
    temp_eq = constant[:]
    temp_eq = temp_eq.replace('y', str(y))
    if x == 0.0:
        x = 0.1
    temp_eq = temp_eq.replace('x', str(x))
    temp_eq = temp_eq.replace('ep', 'exp')
    c = parse_expr(temp_eq).evalf()
    equation = general_equation.replace('C', str(c))
