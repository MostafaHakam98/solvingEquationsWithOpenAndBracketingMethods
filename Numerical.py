#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

from scipy.misc import derivative
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    text = ""
    gtext = ""
    
    def toFunction(self, text, x):
        return eval(text,{'__builtins__':{'cos': math.cos, "x":x,"sin":math.sin,"e":math.exp,"tan":math.tan,"sqrt":math.sqrt}})

    def f(self, x):
        return self.toFunction(self.text, x)
    
    def g(self, x):
        return self.toFunction(self.gtext, x)
    
    def read_file(self):
        file = open("Numerical.txt", "r")
        
        self.functionField.setText(file.readline())
        self.functionField_G.setText(file.readline())
        
        file.close()
    
    def popupmsg(msg):
        msg = "Unavailable Method for this Function"
        NORM_FONT = ("Verdana", 10)
        popup = tk.Tk()
        popup.wm_title("Test Failed")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill = "x", pady = 60, padx = 60)
        B1 = ttk.Button(popup, text = "Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()
        
    def changeLabels(self, MainWindow, label0, label1, label2, label3):
        _translate = QtCore.QCoreApplication.translate
        
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", label0))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", label1))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", label2))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", label3))


    #_______________________________________________________________________________________________________________________
    
    def bisectionMethod (self, xl, xu, Es, iterations):
        if (self.f(xl) * self.f(xu) >= 0):
            self.popupmsg()
            return 0
            
        E = 100
        xr = 0
        i = 0
        
        array = []
        x = []
        y = []
        
        j = -100
        k = xu
        
        while(j < 100):
            x.append(j)
            y.append(self.f(j))
            j += 0.1
        
        j = xl
        
        while(E > Es and i < iterations):
            xr = (xl + xu) / 2
            test = self.f(xl) * self.f(xr)
            self.setItem(str(xl), i, 0)
            self.setItem(str(xu), i, 1)
            self.setItem(str(xr), i, 2)
            
            array.append(xr)
            
            if (test == 0):
                break
            elif (test > 0):
                xl = xr
            elif (test < 0):
                xu = xr
            
            if (i > 0):
                val = float(self.getItem(i - 1, 2))
                E = abs((xr - val) / xr)
                self.setItem(str(E), i, 3)
            else:
                self.setItem("-", i, 3)
                
            i += 1
        
        plt.axis([xr-1, xr+1, -2, 10])
        plt.plot(x, y)
        plt.axhline(0,  label = 'pyplot horizontal line', color ="k")
        for p in array:
            plt.scatter(p,  0)
            plt.pause(1)
        plt.axvline(xr,  label = 'pyplot vertical line', color ="r")
        plt.show()
        
        return xr
            
    def falsePosition (self, xl, xu, Es, iterations):
        if (self.f(xl) * self.f(xu) >= 0):
            self.popupmsg()
            return 0

        E = 100
        xr = 0
        i = 0
        
        array = []
        x = []
        y = []
        j = -100
        k = xu
        while(j<100):
            x.append(j)
            y.append(self.f(j))
            j += 0.1
        j = xl
        
        while(E > Es and i < iterations):
            xr = (xl * self.f(xu) - xu * self.f(xl)) / (self.f(xu) - self.f(xl))
            
            self.setItem(str(xl), i, 0)
            self.setItem(str(xu), i, 1)
            self.setItem(str(xr), i, 2)
            
            array.append(xr)
            
            if (self.f(xr) == 0):
                break
            elif (self.f(xr) > 0):
                xu = xr
            elif (self.f(xr) < 0):
                xl = xr
            
            if (i > 0):
                val = float(self.getItem(i - 1, 2))
                E = abs((xr - val) / xr)
                self.setItem(str(E), i, 3)
            else:
                self.setItem("-", i, 3)
            i += 1
            
        plt.axis([xr-1, xr+1, -2, 10])
        plt.plot(x, y)
        plt.axhline(0,  label = 'pyplot horizontal line', color ="k")
        for p in array:
            plt.scatter(p,  0)
            plt.pause(1)
        plt.axvline(xr,  label = 'pyplot vertical line', color ="r")
        plt.show()
        
        return xr

    def fixedPoint (self, xi, Es, iterations):
        if(derivative(self.g, xi, dx = 1e-6) >= 1):
            self.popupmsg()
            return 0
        
        E = 100
        i = 0
        
        array = []
        x = []
        y = []
        j = -100
        k = 0
        while(j<100):
            x.append(j)
            y.append(self.f(j))
            j += 0.1
        j = xi

        while(E > Es and i < iterations):
            xj = self.g(xi)
            
            self.setItem("-", i, 0)
            self.setItem(str(xi), i, 1)
            self.setItem(str(xj), i, 2)
            
            array.append(xj)
            
            E = abs((xj - xi) / xj)
            
            if (i > 0):
                self.setItem(str(E), i, 3)
            else:
                self.setItem("-", i, 3)

            i += 1
            xi = xj
            
        plt.axis([xj-1, xj+1, -2, 10])
        plt.plot(x, y)
        plt.axhline(0,  label = 'pyplot horizontal line', color ="k")
        for p in array:
            plt.scatter(p,  0)
            plt.pause(1)
        plt.axvline(xj,  label = 'pyplot vertical line', color ="r")
        plt.show()
        
        return xi
            
    def newtonRaphson (self, xi, Es, iterations):
        E = 100
        xj = 0
        i = 0
        
        array = []
        x = []
        y = []
        j = -100
        k = 0
        while(j<100):
            x.append(j)
            y.append(self.f(j))
            j += 0.1
        j = xi

        while(E > Es and i < iterations):
            if  derivative(self.f, xi, dx = 1e-6) == 0:
                self.popupmsg()
                return
            else:
                xj = xi - (self.f(xi) / derivative(self.f, xi, dx = 1e-6))
            
            self.setItem("-", i, 0)
            self.setItem(str(xi), i, 1)
            self.setItem(str(xj), i, 2)
            
            array.append(xj)
            
            E = abs((xj - xi) / xj)
            
            if i > 0:
                self.setItem(str(E), i, 3)
            else:
                self.setItem("-", i, 3)

            i += 1
            xi = xj
        
        plt.axis([xj-1, xj+1, -2, 10])
        plt.plot(x, y)
        plt.axhline(0,  label = 'pyplot horizontal line', color ="k")
        for p in array:
            plt.scatter(p,  0)
            plt.pause(1)
        plt.axvline(xj,  label = 'pyplot vertical line', color ="r")
        plt.show()
            
        return xi

    def secant (self, xi, xj, Es, iterations):
        E = 100
        xk = 0
        i = 0
        
        array = []
        x = []
        y = []
        
        j = -100
        k = xj
        
        while(j < 100):
            x.append(j)
            y.append(self.f(j))
            j += 0.1
        
        j = xi

        while(E > Es and i < iterations):
            xk = xi - (self.f(xi) * (xi - xj)) / (self.f(xi) - self.f(xj))
            
            self.setItem(str(xj), i, 0)
            self.setItem(str(xi), i, 1)
            self.setItem(str(xk), i, 2)
            
            array.append(xk)
            
            E = abs((xk - xi) / xk)
            
            if i > 0:
                self.setItem(str(E), i, 3)
            else:
                self.setItem("-", i, 3)
            i += 1
            xj = xi
            xi = xk
        
        plt.axis([xk-1, xk+1, -2, 10])
        plt.plot(x, y)
        plt.axhline(0,  label = 'pyplot horizontal line', color ="k")
        for p in array:
            plt.scatter(p,  0)
            plt.pause(1)
        plt.axvline(xk,  label = 'pyplot vertical line', color ="r")
        plt.show()
            
        return xi
    
    def evaluate(self, method = ""):
        self.text = self.functionField.text()
        self.gtext = self.functionField_G.text()
        
        root = 0
        
        if method == "Bisection":
            xl = float(self.lineEdit_x_low.text())
            xu = float(self.lineEdit_x_up.text())
            Es = float(self.lineEdit_tolerance.text())
            iterations = int(self.lineEdit_iterations.text())
            root = self.bisectionMethod(xl, xu, Es, iterations)
        elif method == "False":
            xl = float(self.lineEdit_x_low.text())
            xu = float(self.lineEdit_x_up.text())
            Es = float(self.lineEdit_tolerance.text())
            iterations = int(self.lineEdit_iterations.text())
            root = self.falsePosition(xl, xu, Es, iterations)
        elif method == "Fixed Point":
            xi = float(self.lineEdit_x_low.text())
            Es = float(self.lineEdit_tolerance.text())
            iterations = int(self.lineEdit_iterations.text())
            root = self.fixedPoint(xi, Es, iterations)
        elif method == "Newton Raphson":
            xi = float(self.lineEdit_x_low.text())
            Es = float(self.lineEdit_tolerance.text())
            iterations = int(self.lineEdit_iterations.text())
            root = self.newtonRaphson(xi, Es, iterations)
        elif method == "Secant":
            xi = float(self.lineEdit_x_low.text())
            xj = float(self.lineEdit_x_up.text())
            Es = float(self.lineEdit_tolerance.text())
            iterations = int(self.lineEdit_iterations.text())
            root = self.secant(xi, xj, Es, iterations)
        
        self.textEdit.setText(str(root))
            
    def setItem(self, text, i, j):
        val = text
        item = QtWidgets.QTableWidgetItem(text)
        self.tableWidget.setItem(i, j, item)
                          
    def getItem(self, i, j):
        return self.tableWidget.item(i, j).text()
    
    #____________________________________________________________________________________________________________________
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 963)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.functionField = QtWidgets.QLineEdit(self.centralwidget)
        self.functionField.setGeometry(QtCore.QRect(100, 20, 631, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.functionField.setFont(font)
        self.functionField.setText("")
        self.functionField.setObjectName("functionField")
        self.button_method_bisection = QtWidgets.QPushButton(self.centralwidget)
        self.button_method_bisection.setGeometry(QtCore.QRect(150, 190, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_method_bisection.setFont(font)
        self.button_method_bisection.setObjectName("button_method_bisection")
        self.button_method_fixedPoint = QtWidgets.QPushButton(self.centralwidget)
        self.button_method_fixedPoint.setGeometry(QtCore.QRect(520, 180, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_method_fixedPoint.setFont(font)
        self.button_method_fixedPoint.setObjectName("button_method_fixedPoint")
        self.button_method_falsePosition = QtWidgets.QPushButton(self.centralwidget)
        self.button_method_falsePosition.setGeometry(QtCore.QRect(150, 240, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_method_falsePosition.setFont(font)
        self.button_method_falsePosition.setObjectName("button_method_falsePosition")
        self.button_method_secant = QtWidgets.QPushButton(self.centralwidget)
        self.button_method_secant.setGeometry(QtCore.QRect(520, 260, 171, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_method_secant.setFont(font)
        self.button_method_secant.setObjectName("button_method_secant")
        self.button_method_newtonRaphson = QtWidgets.QPushButton(self.centralwidget)
        self.button_method_newtonRaphson.setGeometry(QtCore.QRect(520, 220, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_method_newtonRaphson.setFont(font)
        self.button_method_newtonRaphson.setObjectName("button_method_newtonRaphson")
        self.button_READ = QtWidgets.QPushButton(self.centralwidget)
        self.button_READ.setGeometry(QtCore.QRect(590, 830, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_READ.setFont(font)
        self.button_READ.setObjectName("button_READ")
        self.label_x_up = QtWidgets.QLabel(self.centralwidget)
        self.label_x_up.setGeometry(QtCore.QRect(150, 330, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_x_up.setFont(font)
        self.label_x_up.setObjectName("label_x_up")
        self.label_x_low = QtWidgets.QLabel(self.centralwidget)
        self.label_x_low.setGeometry(QtCore.QRect(150, 300, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_x_low.setFont(font)
        self.label_x_low.setObjectName("label_x_low")
        self.lineEdit_iterations = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_iterations.setGeometry(QtCore.QRect(620, 340, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_iterations.setFont(font)
        self.lineEdit_iterations.setObjectName("lineEdit_iterations")
        self.lineEdit_tolerance = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tolerance.setGeometry(QtCore.QRect(620, 310, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_tolerance.setFont(font)
        self.lineEdit_tolerance.setObjectName("lineEdit_tolerance")
        self.lineEdit_x_low = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x_low.setGeometry(QtCore.QRect(250, 310, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_x_low.setFont(font)
        self.lineEdit_x_low.setObjectName("lineEdit_x_low")
        self.lineEdit_x_up = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_x_up.setGeometry(QtCore.QRect(250, 340, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_x_up.setFont(font)
        self.lineEdit_x_up.setObjectName("lineEdit_x_up")
        self.label_iteration = QtWidgets.QLabel(self.centralwidget)
        self.label_iteration.setGeometry(QtCore.QRect(520, 330, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_iteration.setFont(font)
        self.label_iteration.setObjectName("label_iteration")
        self.label_tolerance = QtWidgets.QLabel(self.centralwidget)
        self.label_tolerance.setGeometry(QtCore.QRect(520, 300, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_tolerance.setFont(font)
        self.label_tolerance.setObjectName("label_tolerance")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(500, 160, 211, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(130, 160, 211, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(410, 170, 20, 121))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(20, 370, 771, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 830, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.button_EXIT = QtWidgets.QPushButton(self.centralwidget)
        self.button_EXIT.setGeometry(QtCore.QRect(690, 830, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_EXIT.setFont(font)
        self.button_EXIT.setObjectName("button_EXIT")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(40, 400, 741, 401))
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(49)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(28, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(29, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(30, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(31, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(32, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(33, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(34, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(35, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(36, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(37, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(38, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(39, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(40, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(41, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(42, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(43, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(44, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(45, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(46, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(47, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(48, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(160, 830, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.functionField_G = QtWidgets.QLineEdit(self.centralwidget)
        self.functionField_G.setGeometry(QtCore.QRect(190, 110, 431, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.functionField_G.setFont(font)
        self.functionField_G.setObjectName("functionField_G")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 20, 51, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 110, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.button_RESET = QtWidgets.QPushButton(self.centralwidget)
        self.button_RESET.setGeometry(QtCore.QRect(490, 830, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.button_RESET.setFont(font)
        self.button_RESET.setObjectName("button_RESET")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        #button Methods
        self.button_method_bisection.clicked.connect(lambda: self.evaluate("Bisection"))
        self.button_method_fixedPoint.clicked.connect(lambda: self.evaluate("Fixed Point"))
        self.button_method_falsePosition.clicked.connect(lambda: self.evaluate("False"))
        self.button_method_newtonRaphson.clicked.connect(lambda: self.evaluate("Newton Raphson"))
        self.button_method_secant.clicked.connect(lambda: self.evaluate("Secant"))
        
        self.button_method_bisection.clicked.connect(lambda: self.changeLabels(MainWindow, "X(l)", "X(u)", "X(r)", "E"))
        self.button_method_falsePosition.clicked.connect(lambda: self.changeLabels(MainWindow, "X(l)", "X(u)", "X(r)", "E"))
        self.button_method_fixedPoint.clicked.connect(lambda: self.changeLabels(MainWindow, "-", "X(i)", "X(i+1)", "E"))
        self.button_method_newtonRaphson.clicked.connect(lambda: self.changeLabels(MainWindow, "-", "X(i)", "X(i+1)", "E"))
        self.button_method_secant.clicked.connect(lambda: self.changeLabels(MainWindow, "X(i-1)", "X(i)", "X(i+1)", "E"))
        
        self.button_EXIT.clicked.connect(sys.exit)
        self.button_RESET.clicked.connect(self.tableWidget.clear)
        self.button_RESET.clicked.connect(lambda: self.functionField.setText(""))
        self.button_RESET.clicked.connect(lambda: self.functionField_G.setText(""))
        self.button_RESET.clicked.connect(lambda: self.textEdit.setText("0"))
        self.button_READ.clicked.connect(self.read_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Numerical Project"))
        self.button_method_bisection.setText(_translate("MainWindow", "Bisection"))
        self.button_method_fixedPoint.setText(_translate("MainWindow", "Fixed-Point"))
        self.button_method_falsePosition.setText(_translate("MainWindow", "False Position"))
        self.button_method_secant.setText(_translate("MainWindow", "Secant"))
        self.button_method_newtonRaphson.setText(_translate("MainWindow", "Newton-Raphson"))
        self.button_READ.setText(_translate("MainWindow", "Read"))
        self.label_x_up.setText(_translate("MainWindow", "X(u) / X(i-1)"))
        self.label_x_low.setText(_translate("MainWindow", "X(l)  / X(i)"))
        self.lineEdit_iterations.setText(_translate("MainWindow", "50"))
        self.lineEdit_tolerance.setText(_translate("MainWindow", "0.00001"))
        self.lineEdit_x_low.setText(_translate("MainWindow", "0"))
        self.lineEdit_x_up.setText(_translate("MainWindow", "0"))
        self.label_iteration.setText(_translate("MainWindow", "Iterations:"))
        self.label_tolerance.setText(_translate("MainWindow", "Tolerance:"))
        self.label_2.setText(_translate("MainWindow", "X (root) = "))
        self.button_EXIT.setText(_translate("MainWindow", "Exit"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "6"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "7"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "9"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "10"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "11"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "12"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "13"))
        item = self.tableWidget.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "14"))
        item = self.tableWidget.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "15"))
        item = self.tableWidget.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "16"))
        item = self.tableWidget.verticalHeaderItem(16)
        item.setText(_translate("MainWindow", "17"))
        item = self.tableWidget.verticalHeaderItem(17)
        item.setText(_translate("MainWindow", "19"))
        item = self.tableWidget.verticalHeaderItem(18)
        item.setText(_translate("MainWindow", "20"))
        item = self.tableWidget.verticalHeaderItem(19)
        item.setText(_translate("MainWindow", "21"))
        item = self.tableWidget.verticalHeaderItem(20)
        item.setText(_translate("MainWindow", "22"))
        item = self.tableWidget.verticalHeaderItem(21)
        item.setText(_translate("MainWindow", "23"))
        item = self.tableWidget.verticalHeaderItem(22)
        item.setText(_translate("MainWindow", "24"))
        item = self.tableWidget.verticalHeaderItem(23)
        item.setText(_translate("MainWindow", "25"))
        item = self.tableWidget.verticalHeaderItem(24)
        item.setText(_translate("MainWindow", "26"))
        item = self.tableWidget.verticalHeaderItem(25)
        item.setText(_translate("MainWindow", "27"))
        item = self.tableWidget.verticalHeaderItem(26)
        item.setText(_translate("MainWindow", "28"))
        item = self.tableWidget.verticalHeaderItem(27)
        item.setText(_translate("MainWindow", "29"))
        item = self.tableWidget.verticalHeaderItem(28)
        item.setText(_translate("MainWindow", "30"))
        item = self.tableWidget.verticalHeaderItem(29)
        item.setText(_translate("MainWindow", "31"))
        item = self.tableWidget.verticalHeaderItem(30)
        item.setText(_translate("MainWindow", "32"))
        item = self.tableWidget.verticalHeaderItem(31)
        item.setText(_translate("MainWindow", "33"))
        item = self.tableWidget.verticalHeaderItem(32)
        item.setText(_translate("MainWindow", "34"))
        item = self.tableWidget.verticalHeaderItem(33)
        item.setText(_translate("MainWindow", "35"))
        item = self.tableWidget.verticalHeaderItem(34)
        item.setText(_translate("MainWindow", "36"))
        item = self.tableWidget.verticalHeaderItem(35)
        item.setText(_translate("MainWindow", "37"))
        item = self.tableWidget.verticalHeaderItem(36)
        item.setText(_translate("MainWindow", "38"))
        item = self.tableWidget.verticalHeaderItem(37)
        item.setText(_translate("MainWindow", "39"))
        item = self.tableWidget.verticalHeaderItem(38)
        item.setText(_translate("MainWindow", "40"))
        item = self.tableWidget.verticalHeaderItem(39)
        item.setText(_translate("MainWindow", "41"))
        item = self.tableWidget.verticalHeaderItem(40)
        item.setText(_translate("MainWindow", "42"))
        item = self.tableWidget.verticalHeaderItem(41)
        item.setText(_translate("MainWindow", "43"))
        item = self.tableWidget.verticalHeaderItem(42)
        item.setText(_translate("MainWindow", "44"))
        item = self.tableWidget.verticalHeaderItem(43)
        item.setText(_translate("MainWindow", "45"))
        item = self.tableWidget.verticalHeaderItem(44)
        item.setText(_translate("MainWindow", "46"))
        item = self.tableWidget.verticalHeaderItem(45)
        item.setText(_translate("MainWindow", "47"))
        item = self.tableWidget.verticalHeaderItem(46)
        item.setText(_translate("MainWindow", "48"))
        item = self.tableWidget.verticalHeaderItem(47)
        item.setText(_translate("MainWindow", "49"))
        item = self.tableWidget.verticalHeaderItem(48)
        item.setText(_translate("MainWindow", "50"))

        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">0</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "f(x)"))
        self.label_3.setText(_translate("MainWindow", "g(x) "))
        self.button_RESET.setText(_translate("MainWindow", "Reset"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




