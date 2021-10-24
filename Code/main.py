import sys
from PyQt5 import QtWidgets
import App


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App.MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
