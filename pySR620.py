# -*- coding: utf-8 -*-

import sys
import serial
import serial.tools.list_ports
#import time
#import os
import numpy as np
import datetime
#import math

from PyQt5 import QtGui, QtCore, QtWidgets
#from PyQt5.QtGui import *
from PyQt5.QtCore import  QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication


from ui.mainWindow import Ui_MainWindow

#变量初始化
rx_buff = [] #存储串口传入的信息
serial_port = []
serial_port_name = ''
current_data_double = 0.0
data_count = 0
file_name = ''
translate_thread_switch = 0
data_buff = []
state = 0

#串口解析线程
class translate_thread_class(QThread):
    TranslateFinfished = pyqtSignal()   #创建一个信号
    def __init__(self):
        super(translate_thread_class, self).__init__()
    def run(self):
        global translate_thread_switch
        while(translate_thread_switch):
            self.read_serial()
            self.translate()

    def read_serial(self):
        global serial_port, rx_buff, file_name
        #time.sleep(0.2)
        num = serial_port.inWaiting()
        rx_raw = serial_port.read(num)
        rx_raw_list = list(rx_raw)

        if(len(rx_raw) != 0):
            print('本次数据长度：', len(rx_raw))
            if(len(rx_buff) <= 500):
                print('本帧接受前缓冲区长度：', len(rx_buff))
                rx_buff = rx_buff + rx_raw_list
                print('本帧接受后缓冲区长度：', len(rx_buff))
                return 0
            else:
                print('缓冲区溢出！现有长度：', len(rx_buff))
                return -1

    def translate(self):
        global rx_buff, current_data_double, data_count, file_name, data_buff

        if(len(rx_buff) > 4):
            while(rx_buff[0] != 0x0D or rx_buff[1] != 0x0A ) :
                if(len(rx_buff) > 4):
                    rx_buff = rx_buff[1: ]
                else:
                    break

        if(len(rx_buff) > 5):
            current_data_string = ''
            for i in range(3,len(rx_buff)) :
                if(rx_buff[i-1] == 0x0D and rx_buff[i] == 0x0A ) :
                    current_data_list = rx_buff[2:i-1]
                    current_data_string = ''.join('%s' %chr(j) for j in current_data_list)
                    rx_buff = rx_buff[i-1: ]
                    break

            if(current_data_string != ''):
                #current_data_string = rx_buff[2:i-2]
                print(current_data_string)
                #current_data_double = float(current_data_string)
                now_time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                print(now_time_string,' 收到数据：',current_data_string,'\r\n')
                data_count += 1

                print('正在写入',file_name)
                file_handle = open(file_name,mode='a+')
                file_handle.write(str(data_count) + ' , ' + now_time_string + ' , ' + current_data_string + '\r\n')
                file_handle.close()
                print('写入完成')

                data_buff.append(current_data_string)
                self.TranslateFinfished.emit()#发送信号



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        global file_name

        super(MainWindow, self).__init__(parent)
        self.setupUi(self) #mainWindow中的初始化
        #self.set_figure() #matplotlib在软件启动时的画面
        #self.import_serial_port() #读取串口

        #初始化定时器
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000) #单位：ms
        self.timer.timeout.connect(self.transform)  # 每隔一段时间就会触发一次函数
        self.timecount = 0

        #初始化时间间隔选择下拉框
        self.timeintervals = {"每   1s":1000 ,
                              "每 0.5s":500  ,
                              "每 0.1s":100  ,
                              "每0.05s":50   ,
                              "每0.02s":20   ,
                              "每0.01s":10    }
        self.TimeBaseSelectBox.clear()
        for i in self.timeintervals:
            self.TimeBaseSelectBox.addItem(i, self.timeintervals[i])
        self.TimeBaseSelectBox.setCurrentText("每  1s")

        #设置默认的文件保存目录
        now_filename = datetime.datetime.now().strftime('\%Y-%m-%d %H_%M_%S.txt')
        #file_name = '%s%s' %(os.getcwd(), now_filename)
        file_name = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S.txt')
        #self.FilePathLineEdit.setText(file_name)

        #初始化串口解析线程
        self.translate_thread = translate_thread_class()
        self.translate_thread.TranslateFinfished.connect(self.update_data_display) # 连接信号

        #初始化变量
        self.data_plot_list = []

    def import_serial_port(self):
        global serial_port, serial_port_name
        self.port_list = list(serial.tools.list_ports.comports())

        if len(self.port_list) == 0:
            MsgTitle = "警告：找不到可用串口"
            MsgInfo = "警告：找不到可用串口\n请连接串口硬件设备后重试"
            QtWidgets.QMessageBox.critical(self, MsgTitle, MsgInfo)
        else:
            self.SerialSelectBox.clear()
            for i in range(0, len(self.port_list)):
                str(self.port_list[i])
                self.SerialSelectBox.addItem(str(self.port_list[i]))

    def update_data_display(self):
        global data_buff
        if(data_buff != []):
            #提取新数据
            current_data_string = data_buff[0]
            now_time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S >> ')
            full_string = now_time_string + current_data_string
            #self.SerialPlainTextEdit.appendPlainText(now_time_string)
            #self.SerialPlainTextEdit.appendPlainText(current_data_string)
            self.SerialPlainTextEdit.appendPlainText(full_string)

            current_data_double = float(current_data_string)

            #更新数组
            self.data_plot_list.insert(0,current_data_double)
            if len(self.data_plot_list) > 700:
                del self.data_plot_list[-1]

            #画图
            self.MatplotlibWidget.mpl.axes.cla()
            self.MatplotlibWidget.mpl.axes.plot(self.data_plot_list, 'r')

            #self.MatplotlibWidget.mpl.fig.set_facecolor('black')
            #self.MatplotlibWidget.mpl.axes.set_facecolor('black')
            self.MatplotlibWidget.mpl.axes.set_xlim(0, 600)#x坐标范围
            #self.MatplotlibWidget.mpl.axes.set_ylim(0, 100)#y坐标范围
            self.MatplotlibWidget.mpl.axes.set_xticks(np.arange(0, 601, 100))#x坐标刻度
            #self.MatplotlibWidget.mpl.axes.set_yticks(np.arange(0, 101, 10))#y坐标刻度
            self.MatplotlibWidget.mpl.axes.grid(True)
            self.MatplotlibWidget.mpl.draw()

            #删除第一个数据
            data_buff.pop()

    def transform(self):
        global serial_port, serial_port_name
        data_xavg = bytes([0x78,0x61,0x76,0x67,0x3F,0x0D,0x0A])  #xavg?\r\n

        try:
            serial_port.write(data_xavg)
        except:
            MsgTitle = "警告：串口发送失败！"
            MsgInfo = "警告：串口发送失败！\n请重新打开串口"
            QtWidgets.QMessageBox.critical(self, MsgTitle, MsgInfo)
        else:
            pass



    @pyqtSlot()
    def on_StartButton_clicked(self):
        global serial_port, translate_thread_switch, state

        if(state == 0):
            if(serial_port_name != ''):

                try:
                    translate_thread_switch = 0
                    self.timer.stop()
                    serial_port.close()#关闭上次打开的串口
                except:
                    pass
                else:
                    pass

                try:
                    serial_port = serial.Serial(serial_port_name,9600)
                except:
                    self.timer.stop()
                    QtWidgets.QMessageBox.critical(self, "串口错误", "此串口已被占用或发生了其他错误，请更换串口号！")
                    return -1
                else:
                    self.timecount = 0
                    self.timer.start()
                    translate_thread_switch = 1
                    self.translate_thread.start()
                    self.label.setText('保存中')
                    self.StartButton.setText('停止')
                    state = 1
            else:
                MsgTitle = "请先设置串口！"
                MsgInfo = "警告：请先选择串口，再点击开始按钮"
                QtWidgets.QMessageBox.critical(self, MsgTitle, MsgInfo)
        else:
            state = 0
            self.timer.stop()
            translate_thread_switch = 0
            self.label.setText('已停止')
            self.StartButton.setText('开始')

    @pyqtSlot()
    def on_SerialSelectBox_popupAboutToBeShown(self):
        self.import_serial_port()

    @pyqtSlot(int)#下拉列表更新后设置串口号
    def on_SerialSelectBox_currentIndexChanged(self, CurrentIndex):
        global serial_port_name
        cominfro = list(self.port_list[CurrentIndex])
        serial_port_name = cominfro[0]
        print(serial_port_name)

    @pyqtSlot(str)#下拉列表更新后设置间隔时间
    def on_TimeBaseSelectBox_currentIndexChanged(self, CurrentText):
        self.timer.setInterval(self.timeintervals[CurrentText])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui = MainWindow()
    ui.show()

    sys.exit(app.exec_())

