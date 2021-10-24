from sympy.parsing.sympy_parser import parse_expr
from sympy import *


class ExactMethod():
    def __init__(self, equation, step=0.1, x0=0, y0=0, rightValue=0, roundNum=8):
        self.equation = equation
        self.step = step
        if x0 != 0.0:
            self.x0 = x0
        else:
            self.x0 = 0.1
        self.y0 = y0
        self.rightValue = rightValue
        self.roundNum = roundNum
        self.x_table = [x0]
        self.y_table = [y0]

    def findYExact(self):
        if round(self.x_table[-1] + self.step, 2) == 0.0:
            self.y_table.append(parse_expr(self.equation.replace('x', str(0.1))))
        else:
            self.y_table.append(parse_expr(self.equation.replace('x', str(round(self.x_table[-1] + self.step, self.roundNum)))))

    def solve(self):
        i = round(self.x0 + self.step, self.roundNum)
        end = round(self.rightValue + self.step/2, self.roundNum)
        while i <= end:
            self.findYExact()
            self.x_table.append(i)
            i = round(i + self.step, self.roundNum)

        return self.x_table, self.y_table
