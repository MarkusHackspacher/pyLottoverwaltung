# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auswertung.ui'
#
# Created: Sun Apr  7 13:46:41 2013
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(561, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(200, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.edi_daten = QtGui.QPlainTextEdit(Dialog)
        self.edi_daten.setGeometry(QtCore.QRect(10, 10, 541, 221))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.edi_daten.setFont(font)
        self.edi_daten.setAutoFillBackground(False)
        self.edi_daten.setUndoRedoEnabled(False)
        self.edi_daten.setReadOnly(True)
        self.edi_daten.setObjectName("edi_daten")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.edi_daten.setWhatsThis(QtGui.QApplication.translate("Dialog", "Ausgabefeld", None, QtGui.QApplication.UnicodeUTF8))

