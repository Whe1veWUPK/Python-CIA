from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCursor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QFileSystemModel

import subprocess

import sys, time, os

from py2neo import Graph

tempPath = sys.path[0]
tempPath = tempPath[:-9]

sys.path[0] = tempPath

selected_directory = " "  # 选取根目录的全局变量

with open('config.txt', 'r') as file:
    lines = file.readlines()
# 去除每行末尾的换行符
lines = [line.strip() for line in lines]
# 将值分别赋给变量
neo_adr = lines[0]
neo_acc = lines[1]
neo_pwd = lines[2]


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1080, 800))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 30, 51, 31))
        font = QtGui.QFont()
        font.setFamily("等线 Light")
        font.setPointSize(6)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(230, 30, 521, 31))
        font = QtGui.QFont()
        font.setFamily("等线")
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)

        self.textEdit.setGeometry(QtCore.QRect(230, 70, 811, 681))
        font = QtGui.QFont()
        font.setFamily("等线")
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setLineWrapMode(QTextEdit.NoWrap)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 220, 801))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        # analyzer button
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(50, 460, 131, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        # settings button (kill)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(50, 505, 131, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 415, 131, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 10, 121, 16))
        font = QtGui.QFont()
        font.setFamily("等线")
        self.label.setFont(font)
        self.label.setObjectName("label")
        # 侧边浏览工具
        self.treeView = QtWidgets.QTreeView(self.frame)
        self.treeView.setGeometry(QtCore.QRect(20, 30, 191, 371))
        self.treeView.setObjectName("treeView")

        self.frame.raise_()
        self.pushButton.raise_()
        self.treeView.raise_()
        self.lineEdit.raise_()
        self.textEdit.raise_()
        self.label.raise_()
        self.indexview()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.openFile)
        self.pushButton.clicked.connect(self.indexview)

        self.pushButton_3.clicked.connect(self.make_graph)
        self.pushButton_4.clicked.connect(self.openAnalyzer)
        self.pushButton_5.clicked.connect(self.setup_dialog)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PythonCIA"))
        self.pushButton.setText(_translate("MainWindow", "browse..."))

        self.lineEdit.setPlaceholderText(_translate("MainWindow", "current directory..."))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "#import .py files "))

        self.pushButton_3.setText(_translate("MainWindow", "Graph"))
        self.pushButton_4.setText(_translate("MainWindow", "Analyze"))
        self.pushButton_5.setText(_translate("MainWindow", "Settings"))
        self.label.setText(_translate("MainWindow", "File Directory"))
        subprocess.Popen('neo4j.bat console', shell=True)

    def setup_dialog(self):
        self.setup = QWidget()
        self.dialog = Ui_neo4jSet()
        self.dialog.setupUi(self.setup)
        self.setup.show()

    def openFile(self):
        file_dir = QFileDialog.getExistingDirectory()  # 打开filedialog

        if file_dir == "":
            print("no file")
        else:
            self.lineEdit.setText(file_dir)

        global selected_directory
        if selected_directory != file_dir:
            selected_directory = file_dir

        #print(selected_directory)

    def make_graph(self):

        if selected_directory == ' ':
            msg_box = QMessageBox(QMessageBox.Warning, 'error', 'NO PATH GIVEN')
            msg_box.exec_()
            return
        graph = Graph(neo_adr, auth=(neo_acc, neo_pwd))
        query = "MATCH (n) DETACH DELETE n"
        graph.run(query)

        from BackEnd import astree, file_scanner

        dir_path = selected_directory  # 路径
        #print(selected_directory)
        dir_path = dir_path.replace('/', '\\')
        # 找出目录下的所有.py文件
        file_scanner.py_files.clear()
        file_scanner.get_py(dir_path)

        for file in file_scanner.py_files:
            # 构造ast
            f = open('ast.txt', 'w')
            f.seek(0)
            f.truncate()
            temp_o = sys.stdout
            temp_e = sys.stderr
            sys.stdout = f
            sys.stderr = f

            tree = astree.ast_constructor(file)
            visit = astree.my_visitor(file)
            visit.visit(tree)
            f.seek(0)

            sys.stdout = temp_o
            sys.stderr = temp_e
            from BackEnd import ast_node_scanner
            ast_node_scanner.graph_constructor('ast.txt', 1)
            f.close()
        for file in file_scanner.py_files:
            # 构造ast
            f = open('ast.txt', 'w')
            f.seek(0)
            f.truncate()
            temp_o = sys.stdout
            temp_e = sys.stderr
            sys.stdout = f
            sys.stderr = f

            tree = astree.ast_constructor(file)
            visit = astree.my_visitor(file)
            visit.visit(tree)
            f.seek(0)

            sys.stdout = temp_o
            sys.stderr = temp_e

            from BackEnd import ast_node_scanner
            ast_node_scanner.graph_constructor('ast.txt', 2)
            f.close()

        self.windowMDG = QWidget()
        self.windowMDG.setWindowTitle("MDG")
        self.windowMDG.resize(1800, 900)
        self.windowMDG.setMinimumSize(QtCore.QSize(1080, 800))
        layoutMDG = QVBoxLayout()
        web_viewMDG = QWebEngineView()
        web_viewMDG.load(QUrl("http://localhost:7474"))
        layoutMDG.addWidget(web_viewMDG)
        self.windowMDG.setLayout(layoutMDG)
        self.windowMDG.show()

    def openAnalyzer(self):
        if selected_directory == ' ':
            msg_box = QMessageBox(QMessageBox.Warning, 'error', 'NO PATH GIVEN')
            msg_box.exec_()
            return
        self.setup = QWidget()
        self.window = Ui_analyzeWindow()
        self.window.setupUi(self.setup)
        self.setup.show()

    def indexview(self):  # 边栏文件浏览setup
        self.model = QFileSystemModel()
        self.treeView.setModel(self.model)

        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

        get_root_index = self.lineEdit.text()
        root_index = self.model.setRootPath(get_root_index)
        self.treeView.setRootIndex(root_index)
        self.treeView.setItemsExpandable(True)
        self.treeView.clicked.connect(self.openfile)

        filepath = self.lineEdit.text()
        file_info = self.model.index(filepath)
        while file_info.isValid():
            self.treeView.setExpanded(file_info, True)
            file_info = file_info.parent()

    def openfile(self, index):  # 仅作为读取目录使用
        # 获取所选文件的路径
        file_dir = self.model.filePath(index)
        # 将点击的目录显示在line上
        if file_dir[-3:].upper() == '.PY':
            self.lineEdit.setText(file_dir)
            with open(file_dir, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
            self.textEdit.setText(data)


class Ui_neo4jSet(object):
    def setupUi(self, neo4jSet):
        neo4jSet.setObjectName("neo4jSet")
        neo4jSet.resize(426, 311)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.okButton = QtWidgets.QPushButton(neo4jSet)
        self.okButton.setGeometry(QtCore.QRect(80, 230, 93, 28))
        self.okButton.setObjectName("okButton")
        self.okButton.setFont(font)
        self.cancelButton = QtWidgets.QPushButton(neo4jSet)
        self.cancelButton.setGeometry(QtCore.QRect(250, 230, 93, 28))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setFont(font)
        self.addressLineEdit = QtWidgets.QLineEdit(neo4jSet)
        self.addressLineEdit.setGeometry(QtCore.QRect(80, 30, 261, 31))
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.addressLineEdit.setFont(font)
        self.label = QtWidgets.QLabel(neo4jSet)
        self.label.setGeometry(QtCore.QRect(80, 10, 261, 16))
        self.label.setObjectName("label")
        self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(neo4jSet)
        self.label_2.setGeometry(QtCore.QRect(80, 70, 261, 16))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.label_3 = QtWidgets.QLabel(neo4jSet)
        self.label_3.setGeometry(QtCore.QRect(80, 140, 261, 16))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)
        self.nameLineEdit = QtWidgets.QLineEdit(neo4jSet)
        self.nameLineEdit.setGeometry(QtCore.QRect(80, 100, 261, 31))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.nameLineEdit.setFont(font)
        self.passwordLineEdit = QtWidgets.QLineEdit(neo4jSet)
        self.passwordLineEdit.setGeometry(QtCore.QRect(80, 170, 261, 31))
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.passwordLineEdit.setFont(font)

        self.addressLineEdit.setPlaceholderText('neo4j://localhost:7687')
        self.nameLineEdit.setPlaceholderText('neo4j')
        self.passwordLineEdit.setPlaceholderText('abc123')

        self.retranslateUi(neo4jSet)
        QtCore.QMetaObject.connectSlotsByName(neo4jSet)

        # 添加槽函数
        self.okButton.clicked.connect(self.okButtonfunc)
        self.cancelButton.clicked.connect(self.quitWindow)

    def retranslateUi(self, neo4jSet):
        _translate = QtCore.QCoreApplication.translate
        neo4jSet.setWindowTitle(_translate("neo4jSet", "Dialog"))
        self.okButton.setText(_translate("neo4jSet", "OK"))
        self.cancelButton.setText(_translate("neo4jSet", "Cancel"))
        self.label.setText(_translate("neo4jSet", "Input your neo4j server address："))
        self.label_2.setText(_translate("neo4jSet", "Input your neo4j user name："))
        self.label_3.setText(_translate("neo4jSet", "Input your neo4j user password："))

    def okButtonfunc(self):
        ''' 下面三个变量分别为地址，用户，密码'''
        global neo_adr, neo_acc, neo_pwd
        neo_adr = self.addressLineEdit.text()
        neo_acc = self.nameLineEdit.text()
        neo_pwd = self.passwordLineEdit.text()

        new_values = [neo_adr, neo_acc, neo_pwd]
        # 将新的默认值写入文件
        with open('config.txt', 'w') as file:
            file.write('\n'.join(new_values))

        neo4jSet = self.okButton.window()
        if neo4jSet is not None:
            neo4jSet.close()

    def quitWindow(self):
        neo4jSet = self.cancelButton.window()
        if neo4jSet is not None:
            neo4jSet.close()


class Ui_analyzeWindow(object):
    def setupUi(self, analyzeWindow):
        analyzeWindow.setObjectName("analyzeWindow")
        analyzeWindow.resize(1042, 632)
        analyzeWindow.setMinimumSize(QtCore.QSize(1042, 632))
        analyzeWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        analyzeWindow.setAutoFillBackground(False)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        analyzeWindow.setFont(font)

        self.tab_params = {}
        self.node = QtWidgets.QLineEdit(analyzeWindow)
        self.node.setGeometry(QtCore.QRect(40, 154, 171, 23))
        self.node.setObjectName("node")
        self.path = QtWidgets.QLineEdit(analyzeWindow)
        self.path.setGeometry(QtCore.QRect(40, 54, 171, 23))
        self.path.setObjectName("path")
        self.line = QtWidgets.QLineEdit(analyzeWindow)
        self.line.setGeometry(QtCore.QRect(40, 104, 171, 23))
        self.line.setObjectName("line")

        self.add = QtWidgets.QRadioButton(analyzeWindow)
        self.add.setGeometry(QtCore.QRect(40, 190, 117, 21))
        self.add.setObjectName("add")
        self.dele = QtWidgets.QRadioButton(analyzeWindow)
        self.dele.setGeometry(QtCore.QRect(40, 250, 117, 21))
        self.dele.setObjectName("del")
        self.edit = QtWidgets.QRadioButton(analyzeWindow)
        self.edit.setGeometry(QtCore.QRect(40, 220, 117, 21))
        self.edit.setObjectName("edit")

        self.buttonGroup = QtWidgets.QButtonGroup(analyzeWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.add)
        self.buttonGroup.addButton(self.dele)
        self.buttonGroup.addButton(self.edit)

        self.engage = QtWidgets.QPushButton(analyzeWindow)
        self.engage.setGeometry(QtCore.QRect(30, 284, 191, 41))
        self.engage.setObjectName("engage")

        self.label_3 = QtWidgets.QLabel(analyzeWindow)
        self.label_3.setGeometry(QtCore.QRect(40, 134, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(analyzeWindow)
        self.label_2.setGeometry(QtCore.QRect(40, 84, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(analyzeWindow)
        self.label.setGeometry(QtCore.QRect(40, 34, 72, 15))
        self.label.setObjectName("label")

        self.treeView = QtWidgets.QTreeView(analyzeWindow)
        self.treeView.setGeometry(QtCore.QRect(30, 344, 191, 261))
        self.treeView.setObjectName("treeView")

        header = self.treeView.header()
        header.hide()
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)

        self.tabWidget = QtWidgets.QTabWidget(analyzeWindow)
        self.tabWidget.setGeometry(QtCore.QRect(240, 10, 781, 591))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.clear()

        self.retranslateUi(analyzeWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(analyzeWindow)
        self.buttonGroup.buttonClicked.connect(self.buttonClicked)
        self.engage.clicked.connect(self.engage_anal)
        self.open_py()

    def retranslateUi(self, analyzeWindow):
        _translate = QtCore.QCoreApplication.translate
        analyzeWindow.setWindowTitle(_translate("analyzeWindow", "Form"))
        self.engage.setText(_translate("analyzeWindow", "ANALYZE"))
        self.add.setText(_translate("analyzeWindow", "ADD"))
        self.edit.setText(_translate("analyzeWindow", "MODIFY"))
        self.dele.setText(_translate("analyzeWindow", "DELETE"))
        self.label.setText(_translate("analyzeWindow", "Path"))
        self.label_2.setText(_translate("analyzeWindow", "Line"))
        self.label_3.setText(_translate("analyzeWindow", "Node"))

    def open_py(self):
        from BackEnd import file_scanner
        file_scanner.py_files = []
        dir_path = selected_directory  # 路径
        # 找出目录下的所有.py文件
        file_scanner.py_files.clear()
        file_scanner.get_py(dir_path)

        for file in file_scanner.py_files:
            dirStr, ext = os.path.splitext(file)
            name = dirStr.split("\\")[-1]

            self.textedit = TabTextEdit(self.tabWidget)
            self.textedit.setGeometry(QtCore.QRect(10, 10, 761, 541))

            self.textedit.lineClicked.connect(self.updateLineNum)
            self.tabWidget.currentChanged.connect(self.updateFilePath)
            params = {"file_path": file}
            self.tab_params[self.textedit] = params

            self.tabWidget.addTab(self.textedit, name)
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
            self.textedit.setText(data)

    def updateLineNum(self, line_number):
        self.line.setText(f'{line_number}')

    def updateFilePath(self):
        file = self.tabWidget.currentWidget()
        if file:
            data = self.tab_params.get(file)
            if data:
                get_path = data.get("file_path")
                self.path.setText(get_path)
                #print(get_path)

    mode = ''

    def buttonClicked(self, button):
        if button.text() == "ADD":
            self.mode = 'Add'
        elif button.text() == "MODIFY":
            self.mode = 'Modify'
        elif button.text() == "DELETE":
            self.mode = 'Delete'

    def engage_anal(self):
        from BackEnd import analyzer
        a_line = self.line.text()
        a_path = self.path.text()
        a_node = self.node.text()
        a_mode = self.mode

        tab = self.tabWidget.currentWidget()
        if a_mode != 'Delete':
            with open(a_path, 'w', encoding='utf-8', errors='ignore') as edit_file:
                data = tab.toPlainText()
                edit_file.write(data)

            with open(a_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
            tab.setText(data)

        self.tabWidget.clear()
        self.open_py()
        self.model.clear()

        ana = analyzer.analyzer(a_mode, a_path, a_line, a_node)
        ana.analyze()
        print(len(analyzer.impact_set))
        for node in analyzer.impact_set:
            print(node)
            node_name = node['Name']
            node_path = node['Path']
            node_start = 'Start Line: ' + node['StartLine']
            node_end = 'End Line: ' + node['EndLine']

            name_s, ext = os.path.splitext(node_path)
            name_h = name = name_s.split("\\")[-1]
            name = name_s.split("\\")[-1] + '-' + node_name

            self.highlight_tab(name_h, int(node['StartLine']) - 1, int(node['EndLine']))

            item_root = QStandardItem(name)
            self.model.appendRow(item_root)
            item_path = QStandardItem(node_path)
            item_root.appendRow(item_path)
            item_start = QStandardItem(node_start)
            item_root.appendRow(item_start)
            item_end = QStandardItem(node_end)
            item_root.appendRow(item_end)
            self.treeView.expandAll()
            self.treeView.resizeColumnToContents(0)
            self.treeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def highlight_tab(self, tab_name, start_line, end_line):
        # 找到要高亮显示的Tab
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == tab_name:
                tab = self.tabWidget.widget(i)

                # 创建一个QTextCursor并设置高亮
                cursor = tab.textCursor()
                cursor.setPosition(0)  # 移动到文本的开头

                # 移动到起始行的开头
                for _ in range(start_line):
                    cursor.movePosition(QTextCursor.NextBlock)

                # 计算选定文本的长度
                selection_start = cursor.position()

                # 移动到结束行的开头
                for _ in range(end_line - start_line):
                    cursor.movePosition(QTextCursor.NextBlock)

                selection_length = cursor.position() - selection_start

                # 设置选定文本的格式（高亮显示）
                format = cursor.charFormat()
                format.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0)))  # 设置背景色为黄色
                cursor.setPosition(selection_start)
                cursor.setPosition(selection_start + selection_length, QTextCursor.KeepAnchor)
                cursor.setCharFormat(format)

                # 将QTextCursor设置为TextEdit的光标
                tab.setTextCursor(cursor)


class LineNumberSignal(QtCore.QObject):
    lineClicked = QtCore.pyqtSignal(int)


class TabTextEdit(QtWidgets.QTextEdit):  # 继承 原本组件
    lineClicked = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        QtWidgets.QTextEdit.__init__(self)
        self.parent = parent

    def mousePressEvent(self, event):
        QtWidgets.QTextEdit.mousePressEvent(self, event)
        print('press', event)
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            cur = self.textCursor()
            row = cur.blockNumber() + 1
            print(row)
            self.lineClicked.emit(row)
