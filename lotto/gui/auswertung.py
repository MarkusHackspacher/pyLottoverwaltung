# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auswertung.ui'
#
# Created: Sat Mar  9 18:11:11 2013
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
        Dialog.resize(457, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.edi_daten = QtGui.QPlainTextEdit(Dialog)
        self.edi_daten.setGeometry(QtCore.QRect(20, 20, 417, 191))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.edi_daten.setFont(font)
        self.edi_daten.setAutoFillBackground(False)
        self.edi_daten.setUndoRedoEnabled(False)
        self.edi_daten.setReadOnly(True)
        self.edi_daten.setObjectName(_fromUtf8("edi_daten"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.edi_daten.setWhatsThis(QtGui.QApplication.translate("Dialog", "Ausgabefeld", None, QtGui.QApplication.UnicodeUTF8))

