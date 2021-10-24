from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, dpi=100):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure(dpi=dpi)
        self.canvas = Canvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def plotDataPoints(self, data=None):
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)

        ax.grid(which='minor')
        ax.grid(which='major')

        for i in data:
            if i is not None:
                x = i[0]
                y = i[1]
                color = i[2]
                ax.plot(x, y, color, label=f'{i[3]}')
        ax.legend()
        self.canvas.draw()