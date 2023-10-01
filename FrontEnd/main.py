# 程序主函数 2023/3/22
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import MainWindow

if __name__ == '__main__':
    # MainWindow界面启动
    app = QApplication(sys.argv)
    mainwindow = QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(mainwindow)
    mainwindow.show()
    sys.exit(app.exec_())
    
