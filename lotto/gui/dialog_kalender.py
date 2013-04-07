# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_kalender.ui'
#
# Created: Sun Apr  7 13:46:45 2013
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(419, 248)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 211, 301, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.calendarWidget = QtGui.QCalendarWidget(Dialog)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 10, 381, 191))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setSelectionMode(QtGui.QCalendarWidget.SingleSelection)
        self.calendarWidget.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setObjectName("calendarWidget")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

