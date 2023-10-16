# -*- coding: utf-8 -*-

"""
调用方法：
导入此文件，并在Qtdesigner中提升窗口后即可使用

示例函数（位于主程序入口最终调用的类中）

def set_figure(self):
        self.MatplotlibWidget.mpl.axes.set_xlim(0, 700)#x坐标范围
        self.MatplotlibWidget.mpl.axes.set_ylim(0, 100)#y坐标范围
        self.MatplotlibWidget.mpl.axes.set_xticks(np.arange(0, 701, 100))#x坐标刻度
        self.MatplotlibWidget.mpl.axes.set_yticks(np.arange(0, 101, 10))#y坐标刻度
        self.MatplotlibWidget.mpl.axes.grid(True)

def refresh_figure(self): 
        self.MatplotlibWidget.mpl.axes.cla()
        self.MatplotlibWidget.mpl.axes.plot(self.l, 'r')
        self.set_figure()
        self.MatplotlibWidget.mpl.draw()

"""


import sys
import random
import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget

from numpy import arange, sin, pi

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=7, height=5, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=7, height=5, dpi=100)
        #self.mpl.start_dynamic_plot() #初始化的时候就呈现动态图
        #self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.layout.addWidget(self.mpl)
        #self.layout.addWidget(self.mpl_ntb)


