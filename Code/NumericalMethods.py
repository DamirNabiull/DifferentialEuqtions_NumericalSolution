from sympy.parsing.sympy_parser import parse_expr
from sympy import *


class EquationMethod():
    def __init__(self, equation, differentialEquation, color, leftValue=0, rightValue=0, step=0.1, x0=0, y0=0, roundNum=8):
        self.equation = equation
        self.differentialEquation = differentialEquation
        self.leftValue = leftValue
        self.rightValue = rightValue
        self.step = step
        if x0 != 0:
            self.x0 = x0
        else:
            self.x0 = 0.1
        self.y0 = y0
        self.roundNum = roundNum
        self.table = [[self.x0, self.y0, self.y0, 0, 0]]
        self.lte_table = [0]
        self.gte_table = [0]
        self.Y_table = [self.y0]
        self.color = color
        self.size = 1

    def findYExact(self, x):
        if round(x + self.step, 2) == 0.0:
            self.y = parse_expr(self.equation.replace('x', str(0.1)))
        else:
            self.y = parse_expr(self.equation.replace('x', str(x + self.step)))

    def findYApprox(self, x, y):
        self.argsApprox = {'x': x, 'y': y, 'h': self.step, 'ep': 'exp'}
        tempDiffirential = self.methodEquation[:]
        for key in self.argsApprox:
            tempDiffirential = tempDiffirential.replace(key, str(self.argsApprox[key]))
        self.Y = parse_expr(tempDiffirential)

    def findLTE(self):
        self.argsLTE = {'y': self.table[self.size - 1][1], 'x': self.table[self.size - 1][0], 'h': self.step, 'ep': 'exp'}
        tempDiffirential = self.methodEquation[:]
        for key in self.argsLTE:
            tempDiffirential = tempDiffirential.replace(key, str(self.argsLTE[key]))
        self.lte = abs(self.y - parse_expr(tempDiffirential))

    def updateTable(self):
        self.table.append([self.table[self.size - 1][0] + self.step, self.y, self.Y, self.lte, abs(self.y - self.Y)])
        self.Y_table.append(self.Y)
        self.lte_table.append(self.lte)
        self.gte_table.append(abs(self.y - self.Y))
        self.size += 1

    def roundTable(self):
        for i in range(len(self.table)):
            for j in range(1, len(self.table[i])):
                self.table[i][j] = round(self.table[i][j], self.roundNum)

    def solve(self):
        i = round(self.leftValue + self.step, self.roundNum)
        while i < self.rightValue + self.step/2:
            if abs(round(self.table[self.size - 1][0], self.roundNum)) <= 0.1:
                self.table[self.size - 1][0] = 0.1

            self.findYExact(x=self.table[self.size - 1][0])
            self.findYApprox(x=self.table[self.size - 1][0], y=self.table[self.size - 1][2])
            self.findLTE()
            self.updateTable()

            i = round(i + self.step, self.roundNum)
        return [self.Y_table, self.color], [self.lte_table, self.color]

    def findGTE(self, n_0, N):
        self.gte_arr = []
        for i in range(n_0, N+1):
            self.step = (self.rightValue-self.x0)/i
            x, y = self.x0, self.y0
            gte = 0
            j = round(self.leftValue + self.step, self.roundNum)
            while j < self.rightValue + self.step / 2:
                if (abs(x+self.step) < 0.05) or (abs(x+self.step/2) < 0.05):
                    x += 1.5*self.step

                if abs(round(x, self.roundNum)) <= 0.1:
                    x = 0.1

                self.findYExact(x)
                self.findYApprox(x, y)

                if (abs(x+self.step) < 0.05) or (abs(x+self.step/2) < 0.05):
                    x += 1.5*self.step
                else:
                    x += self.step

                y = self.Y
                gte = abs(self.y - self.Y)
                j = round(j + self.step, self.roundNum)
            self.gte_arr.append(gte)
        return [self.gte_arr, self.color]

    def get_data_to_plot(self):
        return [self.Y_table, self.color], [self.lte_table, self.color], [self.gte_arr, self.color]


class EulerEquation(EquationMethod):
    def __init__(self, equation, differentialEquation, color='g', leftValue=0, rightValue=0, step=0.1, x0=0, y0=0, roundNum=8):
        EquationMethod.__init__(self, equation, differentialEquation, color, leftValue, rightValue, step, x0, y0, roundNum)
        self.methodEquation = 'y + h*(' + self.differentialEquation + ')'


class EulerImprovedEquation(EquationMethod):
    def __init__(self, equation, differentialEquation, color='y', leftValue=0, rightValue=0, step=0.1, x0=0, y0=0, roundNum=8):
        EquationMethod.__init__(self, equation, differentialEquation, color, leftValue, rightValue, step, x0, y0, roundNum)
        self.methodEquation = differentialEquation
        self.methodEquation = self.methodEquation.replace('x', '(x + h/2)')
        self.methodEquation = self.methodEquation.replace('y', '(y + (h*' + self.differentialEquation + ')/2)')
        self.methodEquation = 'y + h*(' + self.methodEquation + ')'


class RungeKuttaEquation(EquationMethod):
    def __init__(self, equation, differentialEquation, color='r', leftValue=0, rightValue=0, step=0.1, x0=0, y0=0, roundNum=8):
        EquationMethod.__init__(self, equation, differentialEquation, color, leftValue, rightValue, step, x0, y0, roundNum)

        self.k1 = '(' + differentialEquation + ')'

        self.k2 = differentialEquation.replace('x', '(x + h/2)')
        self.k3 = self.k2[:]
        self.k2 = self.k2.replace('y', '(y + h*' + self.k1 + '/2)')
        self.k3 = self.k3.replace('y', '(y + h*' + self.k2 + '/2)')

        self.k4 = differentialEquation.replace('x', '(x + h)')
        self.k4 = self.k4.replace('y', '(y + h*' + self.k3 + ')')

        self.methodEquation = 'y + h*(' + self.k1 + ' + 2*' + self.k2 + ' + 2*' + self.k3 + ' + ' + self.k4 + ')/6'
