# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lotto_dialog.ui'
#
# Created: Sun Oct 28 20:03:49 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(526, 333)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 411, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(409, 290, 91, 27))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(60, 40, 261, 41))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 110, 311, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.spinBox_superz = QtGui.QSpinBox(Dialog)
        self.spinBox_superz.setGeometry(QtCore.QRect(370, 170, 51, 23))
        self.spinBox_superz.setMaximum(9)
        self.spinBox_superz.setObjectName(_fromUtf8("spinBox_superz"))
        self.spinBox_spiel77 = QtGui.QSpinBox(Dialog)
        self.spinBox_spiel77.setGeometry(QtCore.QRect(140, 194, 101, 23))
        self.spinBox_spiel77.setMaximum(9999999)
        self.spinBox_spiel77.setObjectName(_fromUtf8("spinBox_spiel77"))
        self.spinBox_super6 = QtGui.QSpinBox(Dialog)
        self.spinBox_super6.setGeometry(QtCore.QRect(370, 194, 91, 23))
        self.spinBox_super6.setMaximum(999999)
        self.spinBox_super6.setObjectName(_fromUtf8("spinBox_super6"))
        self.lab_zusatz = QtGui.QLabel(Dialog)
        self.lab_zusatz.setGeometry(QtCore.QRect(20, 170, 101, 21))
        self.lab_zusatz.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_zusatz.setObjectName(_fromUtf8("lab_zusatz"))
        self.lab_spiel77 = QtGui.QLabel(Dialog)
        self.lab_spiel77.setGeometry(QtCore.QRect(20, 194, 101, 21))
        self.lab_spiel77.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_spiel77.setObjectName(_fromUtf8("lab_spiel77"))
        self.lab_superz = QtGui.QLabel(Dialog)
        self.lab_superz.setGeometry(QtCore.QRect(250, 170, 91, 21))
        self.lab_superz.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_superz.setObjectName(_fromUtf8("lab_superz"))
        self.lab_super6 = QtGui.QLabel(Dialog)
        self.lab_super6.setGeometry(QtCore.QRect(250, 194, 91, 21))
        self.lab_super6.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_super6.setObjectName(_fromUtf8("lab_super6"))
        self.btn_save = QtGui.QPushButton(Dialog)
        self.btn_save.setGeometry(QtCore.QRect(190, 290, 95, 31))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Bewertung", None, QtGui.QApplication.UnicodeUTF8))
        self.lab_zusatz.setText(QtGui.QApplication.translate("Dialog", "Zusatzzahl", None, QtGui.QApplication.UnicodeUTF8))
        self.lab_spiel77.setText(QtGui.QApplication.translate("Dialog", "Spiel 77", None, QtGui.QApplication.UnicodeUTF8))
        self.lab_superz.setText(QtGui.QApplication.translate("Dialog", "Superzahl", None, QtGui.QApplication.UnicodeUTF8))
        self.lab_super6.setText(QtGui.QApplication.translate("Dialog", "Super 6:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setText(QtGui.QApplication.translate("Dialog", "Sichern", None, QtGui.QApplication.UnicodeUTF8))

