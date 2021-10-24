import design
import settings
import NumericalMethods
import ExactSolution
from PyQt5 import QtWidgets


class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label_7.setText(settings.title)
        self.lineEdit.setText(str(settings.x_0))
        self.lineEdit_2.setText(str(settings.y_0))
        self.lineEdit_3.setText(str(settings.X))
        self.lineEdit_4.setText(str(settings.n_0))
        self.lineEdit_5.setText(str(settings.N))
        self.lineEdit_6.setText(str(settings.grid))

        self.x0 = settings.x_0
        self.y0 = settings.y_0
        self.rightValue = settings.X
        self.grid = settings.grid
        self.step = (self.rightValue - self.x0) / self.grid
        self.n_0 = settings.n_0
        self.N = settings.N
        self.lte, self.gte, self.solutions = [None, None, None], [None, None, None], [None, None, None, None]
        self.x, self.y = [], []
        self.start = True
        self.n_table = []

        self.is_Euler = self.checkBox.checkState()
        self.is_ImprovedEuler = self.checkBox_2.checkState()
        self.is_RungeKutta = self.checkBox_3.checkState()

        self.Euler = None
        self.ImprovedEuler = None
        self.RungeKutta = None

        self.is_Euler_changed = False
        self.is_ImprovedEuler_changed = False
        self.is_RungeKutta_changed = False

        self.pushButton.clicked.connect(self.plot_all)

    def plot_all(self):
        did_changed = self.has_changes()
        if self.start or did_changed:
            settings.find_const(float(self.lineEdit.text()), float(self.lineEdit_2.text()))
            self.n_table = [i for i in range(self.n_0, self.N + 1)]
            self.update_Exact()
            self.is_Euler_changed = True
            self.is_ImprovedEuler_changed = True
            self.is_RungeKutta_changed = True

        self.update_Euler()
        self.update_ImprovedEuler()
        self.update_RungeKutta()

        self.Solution.plotDataPoints(self.solutions)
        self.LTE.plotDataPoints(self.lte)
        self.GTE.plotDataPoints(self.gte)

    def has_changes(self):
        if (self.x0 == float(self.lineEdit.text()) and
                self.y0 == float(self.lineEdit_2.text()) and
                self.rightValue == float(self.lineEdit_3.text()) and
                self.grid == float(self.lineEdit_6.text()) and
                self.step == (self.rightValue - self.x0) / self.grid and
                self.n_0 == int(self.lineEdit_4.text()) and
                self.N == int(self.lineEdit_5.text())):
            return False
        else:
            self.x0 = float(self.lineEdit.text())
            self.y0 = float(self.lineEdit_2.text())
            self.rightValue = float(self.lineEdit_3.text())
            self.grid = float(self.lineEdit_6.text())
            self.step = (self.rightValue - self.x0) / self.grid
            self.n_0 = int(self.lineEdit_4.text())
            self.N = int(self.lineEdit_5.text())
            return True

    def update_Exact(self):
        self.Exact = ExactSolution.ExactMethod(settings.equation, x0=self.x0, y0=self.y0,
                                               rightValue=self.rightValue, step=self.step)
        self.x, self.y = self.Exact.solve()
        self.start = False
        self.solutions[0] = [self.x, self.y, 'b', 'Exact']

    def update_Euler(self):
        # print(self.is_Euler == False)
        # print(self.checkBox.checkState())
        # print(did_changed)
        if self.is_Euler == False and self.checkBox.checkState() == 2:
            if self.is_Euler_changed or not self.Euler:
                self.Euler = NumericalMethods.EulerEquation(settings.equation, settings.diff_equation, x0=self.x0,
                                                            y0=self.y0, leftValue=self.x0, rightValue=self.rightValue,
                                                            step=self.step)
                temp = self.Euler.solve()
                self.solutions[1] = [self.x] + temp[0] + ['Euler']
                self.lte[0] = [self.x] + temp[1] + ['Euler']
                temp = self.Euler.findGTE(self.n_0, self.N)
                self.gte[0] = [self.n_table] + temp + ['Euler']
                self.is_Euler = True
            else:
                temp = self.Euler.get_data_to_plot()
                self.solutions[1] = [self.x] + temp[0] + ['Euler']
                self.lte[0] = [self.x] + temp[1] + ['Euler']
                self.gte[0] = [self.n_table] + temp[2] + ['Euler']
                self.is_Euler = True
        elif self.is_Euler == True and self.checkBox.checkState() == 0:
            self.solutions[1] = None
            self.lte[0] = None
            self.gte[0] = None
            self.is_Euler = False
        elif self.is_Euler == True and self.is_Euler_changed:
            self.Euler = NumericalMethods.EulerEquation(settings.equation, settings.diff_equation,
                                                        x0=self.x0,
                                                        y0=self.y0, leftValue=self.x0,
                                                        rightValue=self.rightValue,
                                                        step=self.step)
            temp = self.Euler.solve()
            self.solutions[1] = [self.x] + temp[0] + ['Euler']
            self.lte[0] = [self.x] + temp[1] + ['Euler']
            temp = self.Euler.findGTE(self.n_0, self.N)
            self.gte[0] = [self.n_table] + temp + ['Euler']
            self.is_Euler = True
            self.is_Euler_changed = False

    def update_ImprovedEuler(self):
        # print(self.is_ImprovedEuler == False)
        # print(self.checkBox_2.checkState())
        # print(did_changed)
        if self.is_ImprovedEuler == False and self.checkBox_2.checkState() == 2:
            if self.is_ImprovedEuler_changed or not self.ImprovedEuler:
                self.ImprovedEuler = NumericalMethods.EulerImprovedEquation(settings.equation, settings.diff_equation,
                                                                            x0=self.x0,
                                                                            y0=self.y0, leftValue=self.x0,
                                                                            rightValue=self.rightValue,
                                                                            step=self.step)
                temp = self.ImprovedEuler.solve()
                self.solutions[2] = [self.x] + temp[0] + ['ImprovedEuler']
                self.lte[1] = [self.x] + temp[1] + ['ImprovedEuler']
                temp = self.ImprovedEuler.findGTE(self.n_0, self.N)
                self.gte[1] = [self.n_table] + temp + ['ImprovedEuler']
                self.is_ImprovedEuler = True
                self.is_ImprovedEuler_changed = False
            else:
                temp = self.ImprovedEuler.get_data_to_plot()
                self.solutions[2] = [self.x] + temp[0] + ['ImprovedEuler']
                self.lte[1] = [self.x] + temp[1] + ['ImprovedEuler']
                self.gte[1] = [self.n_table] + temp[2] + ['ImprovedEuler']
                self.is_ImprovedEuler = True
        elif self.is_ImprovedEuler == True and self.checkBox_2.checkState() == 0:
            self.solutions[2] = None
            self.lte[1] = None
            self.gte[1] = None
            self.is_ImprovedEuler = False
        elif self.is_ImprovedEuler == True and self.is_ImprovedEuler_changed:
            self.ImprovedEuler = NumericalMethods.EulerImprovedEquation(settings.equation, settings.diff_equation,
                                                                        x0=self.x0,
                                                                        y0=self.y0, leftValue=self.x0,
                                                                        rightValue=self.rightValue,
                                                                        step=self.step)
            temp = self.ImprovedEuler.solve()
            self.solutions[2] = [self.x] + temp[0] + ['ImprovedEuler']
            self.lte[1] = [self.x] + temp[1] + ['ImprovedEuler']
            temp = self.ImprovedEuler.findGTE(self.n_0, self.N)
            self.gte[1] = [self.n_table] + temp + ['ImprovedEuler']
            self.is_ImprovedEuler = True
            self.is_ImprovedEuler_changed = False

    def update_RungeKutta(self):
        # print(self.is_RungeKutta == False)
        # print(self.checkBox_3.checkState())
        # print(self.is_RungeKutta_changed)
        if self.is_RungeKutta == False and self.checkBox_3.checkState() == 2:
            if self.is_RungeKutta_changed or not self.RungeKutta:
                self.RungeKutta = NumericalMethods.RungeKuttaEquation(settings.equation, settings.diff_equation,
                                                                      x0=self.x0,
                                                                      y0=self.y0, leftValue=self.x0,
                                                                      rightValue=self.rightValue,
                                                                      step=self.step)
                temp = self.RungeKutta.solve()
                self.solutions[3] = [self.x] + temp[0] + ['RungeKutta']
                self.lte[2] = [self.x] + temp[1] + ['RungeKutta']
                temp = self.RungeKutta.findGTE(self.n_0, self.N)
                self.gte[2] = [self.n_table] + temp + ['RungeKutta']
                self.is_RungeKutta = True
                self.is_RungeKutta_changed = False
            else:
                temp = self.RungeKutta.get_data_to_plot()
                self.solutions[3] = [self.x] + temp[0] + ['RungeKutta']
                self.lte[2] = [self.x] + temp[1] + ['RungeKutta']
                self.gte[2] = [self.n_table] + temp[2] + ['RungeKutta']
                self.is_RungeKutta = True
        elif self.is_RungeKutta == True and self.checkBox_3.checkState() == 0:
            self.solutions[3] = None
            self.lte[2] = None
            self.gte[2] = None
            self.is_RungeKutta = False
        elif self.is_RungeKutta == True and self.is_RungeKutta_changed:
            self.RungeKutta = NumericalMethods.RungeKuttaEquation(settings.equation, settings.diff_equation,
                                                                  x0=self.x0,
                                                                  y0=self.y0, leftValue=self.x0,
                                                                  rightValue=self.rightValue,
                                                                  step=self.step)
            temp = self.RungeKutta.solve()
            self.solutions[3] = [self.x] + temp[0] + ['RungeKutta']
            self.lte[2] = [self.x] + temp[1] + ['RungeKutta']
            temp = self.RungeKutta.findGTE(self.n_0, self.N)
            self.gte[2] = [self.n_table] + temp + ['RungeKutta']
            self.is_RungeKutta = True
            self.is_RungeKutta_changed = False