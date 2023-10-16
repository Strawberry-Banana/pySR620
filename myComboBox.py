# -*- coding: utf-8 -*-

"""
使用此文件可以在点击QcomboBox(下拉列表)控件时，下拉列表展开之前，发出一个信号。
在信号的槽函数内更新下拉列表，就可以实现在点击空间是实时更新下拉列表内容

调用方法：
导入此文件，并在Qtdesigner中提升窗口后即可使用

示例函数（位于主程序入口最终调用的类中）
@pyqtSlot()
    def on_SerialSelectBox_popupAboutToBeShown(self):
        self.myfunction()

"""



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal  #导入这个模块才可以创建信号
 
class MyComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()   #创建一个信号
    # def mousePressEvent(self, QMouseEvent):#这个是重写鼠标点击事件
    #   self.popupAboutToBeShown.emit()
    def showPopup(self):          #重写showPopup函数
        self.popupAboutToBeShown.emit()   #发送信号
        QComboBox.showPopup(self)   # 弹出选项框
