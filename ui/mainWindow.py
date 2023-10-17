# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from ui.MatplotlibWidget import MatplotlibWidget
from ui.myComboBox import MyComboBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 329)
        MainWindow.setMinimumSize(QtCore.QSize(700, 0))
        MainWindow.setMaximumSize(QtCore.QSize(700, 510))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("banana.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SerialSelectBox = MyComboBox(self.centralwidget)
        self.SerialSelectBox.setGeometry(QtCore.QRect(10, 290, 301, 31))
        self.SerialSelectBox.setEditable(False)
        self.SerialSelectBox.setObjectName("SerialSelectBox")
        self.SerialSelectBox.addItem("")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(570, 290, 121, 31))
        self.StartButton.setObjectName("StartButton")
        self.TimeBaseSelectBox = QtWidgets.QComboBox(self.centralwidget)
        self.TimeBaseSelectBox.setGeometry(QtCore.QRect(320, 290, 91, 31))
        self.TimeBaseSelectBox.setCurrentText("")
        self.TimeBaseSelectBox.setObjectName("TimeBaseSelectBox")
        self.MatplotlibWidget = MatplotlibWidget(self.centralwidget)
        self.MatplotlibWidget.setGeometry(QtCore.QRect(-10, 0, 421, 281))
        self.MatplotlibWidget.setObjectName("MatplotlibWidget")
        self.SerialPlainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.SerialPlainTextEdit.setGeometry(QtCore.QRect(420, 10, 271, 271))
        self.SerialPlainTextEdit.setObjectName("SerialPlainTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(423, 292, 141, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.TimeBaseSelectBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "草莓味的SR620记录仪"))
        self.SerialSelectBox.setItemText(0, _translate("MainWindow", "选择串口…"))
        self.StartButton.setText(_translate("MainWindow", "开始"))
        self.label.setText(_translate("MainWindow", "已停止"))

