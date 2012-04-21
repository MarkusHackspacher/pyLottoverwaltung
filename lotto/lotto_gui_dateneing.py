#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Das Hauptprogramm
"""

import sys
import sqlite3
from PyQt4 import QtGui, QtCore

from lotto_dateneing import Ui_MainWindow as Dlg


class MeinDialog(QtGui.QMainWindow, Dlg): 
    def __init__(self):
        """Fenster oeffnen und Werte zuweisen"""
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)
        self.Btn_Numerary_1to49 = []
        for button in xrange(49):
            self.Btn_Numerary_1to49.append(QtGui.QPushButton(self.gridLayoutWidget))
        for button in xrange(49):
            self.Btn_Numerary_1to49[button].setMaximumSize(QtCore.QSize(58, 58))
            self.gridLayout.addWidget(self.Btn_Numerary_1to49[button], int(button / 7),  int(button % 7), 1, 1)
            self.Btn_Numerary_1to49[button].setAutoFillBackground(True)
            self.Btn_Numerary_1to49[button].setText(QtGui.QApplication.translate("MainWindow", str(button + 1), 
             None, QtGui.QApplication.UnicodeUTF8))
                     
        self.spinBox_Zahlen = []
        self.Btn_delete_Number = []
        for zahlen in xrange(6):
            self.spinBox_Zahlen.append(QtGui.QSpinBox(self.horizontalLayoutWidget))
            self.Btn_delete_Number.append(QtGui.QPushButton(self.horizontalLayoutWidget_2))
        self.spinBox_Zahlen.append(QtGui.QSpinBox(self.Lottozahlen))
        self.Btn_delete_Number.append(QtGui.QPushButton(self.Lottozahlen))
        for zahlen in xrange(7):
            if zahlen != 6:
                self.spinBox_Zahlen[zahlen].setMinimumSize(QtCore.QSize(32, 20))
                self.spinBox_Zahlen[zahlen].setMaximumSize(QtCore.QSize(52, 32))
                self.Btn_delete_Number[zahlen].setMinimumSize(QtCore.QSize(32, 20))
                self.Btn_delete_Number[zahlen].setMaximumSize(QtCore.QSize(52, 20))
                self.horizontalLayout.addWidget(self.spinBox_Zahlen[zahlen])
                self.horizontalLayout_2.addWidget(self.Btn_delete_Number[zahlen])
            else:
                self.spinBox_Zahlen[zahlen].setGeometry(QtCore.QRect(130, 360, 51, 23))
                self.Btn_delete_Number[zahlen].setGeometry(QtCore.QRect(190, 360, 41, 20)) 
            self.spinBox_Zahlen[zahlen].setMaximum(49)
            self.spinBox_Zahlen[zahlen].clear()
            self.Btn_delete_Number[zahlen].setText(QtGui.QApplication.translate("MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
 
 
        self.onmodus()
        self.geaendert()
        self.conn = sqlite3.connect('datenbank.sqlite')
        self.c = self.conn.cursor()
        self.onBtn_gz_laden()
        self.onBtn_ls_laden()        
        
        # Slots einrichten 
        #Datenbank Funktionen
        self.connect(self.Btn_gz_anzeigen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_anzeigen)
        self.connect(self.Btn_ls_anzeigen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_anzeigen)
        self.connect(self.Btn_gz_loeschen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_loeschen)
        self.connect(self.Btn_ls_loeschen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_loeschen)
        self.connect(self.Btn_gz_auswerten,QtCore.SIGNAL("clicked()"), self.onBtn_gz_auswerten)
        self.connect(self.Btn_ls_auswerten,QtCore.SIGNAL("clicked()"), self.onBtn_ls_auswerten)

        #Felder mit Zufallszahen ausfüllen und der jeweiligen Datenbank hinzufügen
        self.connect(self.Btn_Zufall,QtCore.SIGNAL("clicked()"), self.onBtn_Zufall)
        self.connect(self.Btn_hinzu,QtCore.SIGNAL("clicked()"), self.onBtn_hinzu) 

        #Zahlenfelder
        self.connect(self.Btn_delete_Number[0], QtCore.SIGNAL("clicked()"), self.spinBox_1clear)
        self.connect(self.Btn_delete_Number[1], QtCore.SIGNAL("clicked()"), self.spinBox_2clear)
        self.connect(self.Btn_delete_Number[2], QtCore.SIGNAL("clicked()"), self.spinBox_3clear)
        self.connect(self.Btn_delete_Number[3], QtCore.SIGNAL("clicked()"), self.spinBox_4clear)
        self.connect(self.Btn_delete_Number[4], QtCore.SIGNAL("clicked()"), self.spinBox_5clear)
        self.connect(self.Btn_delete_Number[5], QtCore.SIGNAL("clicked()"), self.spinBox_6clear)
        self.connect(self.Btn_delete_Number[6], QtCore.SIGNAL("clicked()"), self.spinBox_7clear)
        self.connect(self.spinBox_Zahlen[0],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_1)
        self.connect(self.spinBox_Zahlen[1],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_2)
        self.connect(self.spinBox_Zahlen[2],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_3)
        self.connect(self.spinBox_Zahlen[3],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_4)
        self.connect(self.spinBox_Zahlen[4],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_5)
        self.connect(self.spinBox_Zahlen[5],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_6)
        self.connect(self.spinBox_Zahlen[6],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox_7)

        self.connect(self.com_modus,QtCore.SIGNAL("currentIndexChanged(int)"), self.onmodus)
        self.connect(self.com_laufzeit,QtCore.SIGNAL("currentIndexChanged(int)"), self.onlaufzeit)

        self.connect(self.calendarWidget,QtCore.SIGNAL("selectionChanged()"), self.oncalendarWidget)

        # 1 bis 49 Felder
        self.connect(self.Btn_Numerary_1to49[0],QtCore.SIGNAL("clicked()"),self.onEingabefeld_1)
        self.connect(self.Btn_Numerary_1to49[1],QtCore.SIGNAL("clicked()"),self.onEingabefeld_2)        
        self.connect(self.Btn_Numerary_1to49[2],QtCore.SIGNAL("clicked()"),self.onEingabefeld_3)
        self.connect(self.Btn_Numerary_1to49[3],QtCore.SIGNAL("clicked()"),self.onEingabefeld_4)
        self.connect(self.Btn_Numerary_1to49[4],QtCore.SIGNAL("clicked()"),self.onEingabefeld_5)
        self.connect(self.Btn_Numerary_1to49[5],QtCore.SIGNAL("clicked()"),self.onEingabefeld_6)
        self.connect(self.Btn_Numerary_1to49[6],QtCore.SIGNAL("clicked()"),self.onEingabefeld_7)
        self.connect(self.Btn_Numerary_1to49[7],QtCore.SIGNAL("clicked()"),self.onEingabefeld_8)
        self.connect(self.Btn_Numerary_1to49[8],QtCore.SIGNAL("clicked()"),self.onEingabefeld_9)
        self.connect(self.Btn_Numerary_1to49[9],QtCore.SIGNAL("clicked()"),self.onEingabefeld_10)
        self.connect(self.Btn_Numerary_1to49[10],QtCore.SIGNAL("clicked()"),self.onEingabefeld_11)
        self.connect(self.Btn_Numerary_1to49[11],QtCore.SIGNAL("clicked()"),self.onEingabefeld_12)
        self.connect(self.Btn_Numerary_1to49[12],QtCore.SIGNAL("clicked()"),self.onEingabefeld_13)
        self.connect(self.Btn_Numerary_1to49[13],QtCore.SIGNAL("clicked()"),self.onEingabefeld_14)
        self.connect(self.Btn_Numerary_1to49[14],QtCore.SIGNAL("clicked()"),self.onEingabefeld_15)
        self.connect(self.Btn_Numerary_1to49[15],QtCore.SIGNAL("clicked()"),self.onEingabefeld_16)
        self.connect(self.Btn_Numerary_1to49[16],QtCore.SIGNAL("clicked()"),self.onEingabefeld_17)
        self.connect(self.Btn_Numerary_1to49[17],QtCore.SIGNAL("clicked()"),self.onEingabefeld_18)
        self.connect(self.Btn_Numerary_1to49[18],QtCore.SIGNAL("clicked()"),self.onEingabefeld_19)
        self.connect(self.Btn_Numerary_1to49[19],QtCore.SIGNAL("clicked()"),self.onEingabefeld_20)
        self.connect(self.Btn_Numerary_1to49[20],QtCore.SIGNAL("clicked()"),self.onEingabefeld_21)
        self.connect(self.Btn_Numerary_1to49[21],QtCore.SIGNAL("clicked()"),self.onEingabefeld_22)
        self.connect(self.Btn_Numerary_1to49[22],QtCore.SIGNAL("clicked()"),self.onEingabefeld_23)
        self.connect(self.Btn_Numerary_1to49[23],QtCore.SIGNAL("clicked()"),self.onEingabefeld_24)
        self.connect(self.Btn_Numerary_1to49[24],QtCore.SIGNAL("clicked()"),self.onEingabefeld_25)
        self.connect(self.Btn_Numerary_1to49[25],QtCore.SIGNAL("clicked()"),self.onEingabefeld_26)
        self.connect(self.Btn_Numerary_1to49[26],QtCore.SIGNAL("clicked()"),self.onEingabefeld_27)
        self.connect(self.Btn_Numerary_1to49[27],QtCore.SIGNAL("clicked()"),self.onEingabefeld_28)
        self.connect(self.Btn_Numerary_1to49[28],QtCore.SIGNAL("clicked()"),self.onEingabefeld_29)
        self.connect(self.Btn_Numerary_1to49[29],QtCore.SIGNAL("clicked()"),self.onEingabefeld_30)
        self.connect(self.Btn_Numerary_1to49[30],QtCore.SIGNAL("clicked()"),self.onEingabefeld_31)
        self.connect(self.Btn_Numerary_1to49[31],QtCore.SIGNAL("clicked()"),self.onEingabefeld_32)
        self.connect(self.Btn_Numerary_1to49[32],QtCore.SIGNAL("clicked()"),self.onEingabefeld_33)
        self.connect(self.Btn_Numerary_1to49[33],QtCore.SIGNAL("clicked()"),self.onEingabefeld_34)
        self.connect(self.Btn_Numerary_1to49[34],QtCore.SIGNAL("clicked()"),self.onEingabefeld_35)
        self.connect(self.Btn_Numerary_1to49[35],QtCore.SIGNAL("clicked()"),self.onEingabefeld_36)
        self.connect(self.Btn_Numerary_1to49[36],QtCore.SIGNAL("clicked()"),self.onEingabefeld_37)
        self.connect(self.Btn_Numerary_1to49[37],QtCore.SIGNAL("clicked()"),self.onEingabefeld_38)
        self.connect(self.Btn_Numerary_1to49[38],QtCore.SIGNAL("clicked()"),self.onEingabefeld_39)
        self.connect(self.Btn_Numerary_1to49[39],QtCore.SIGNAL("clicked()"),self.onEingabefeld_40)
        self.connect(self.Btn_Numerary_1to49[40],QtCore.SIGNAL("clicked()"),self.onEingabefeld_41)
        self.connect(self.Btn_Numerary_1to49[41],QtCore.SIGNAL("clicked()"),self.onEingabefeld_42)
        self.connect(self.Btn_Numerary_1to49[42],QtCore.SIGNAL("clicked()"),self.onEingabefeld_43)
        self.connect(self.Btn_Numerary_1to49[43],QtCore.SIGNAL("clicked()"),self.onEingabefeld_44)
        self.connect(self.Btn_Numerary_1to49[44],QtCore.SIGNAL("clicked()"),self.onEingabefeld_45)
        self.connect(self.Btn_Numerary_1to49[45],QtCore.SIGNAL("clicked()"),self.onEingabefeld_46)
        self.connect(self.Btn_Numerary_1to49[46],QtCore.SIGNAL("clicked()"),self.onEingabefeld_47)
        self.connect(self.Btn_Numerary_1to49[47],QtCore.SIGNAL("clicked()"),self.onEingabefeld_48)
        self.connect(self.Btn_Numerary_1to49[48],QtCore.SIGNAL("clicked()"),self.onEingabefeld_49)
        
        self.statusBar().showMessage('Bereit')

        self.connect(self.actionBeenden, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(self.actionInfo, QtCore.SIGNAL('triggered()'), self.onInfo)
        self.connect(self.actionHilfe, QtCore.SIGNAL('triggered()'), self.onHilfe)
        self.connect(self.edi_daten_gewinnz, QtCore.SIGNAL('cursorPositionChanged()'), self.ondaten_gewinnz)
        self.connect(self.edi_daten_lottoschein, QtCore.SIGNAL('cursorPositionChanged()'), self.ondaten_lottoschein)
 
    def ondaten_gewinnz(self):
       if not self.gz_laden_aktiv:
           block=self.edi_daten_gewinnz.textCursor().blockNumber()
           try:
               self.c.execute('select * from ziehung')
           except:
               self.c.execute("create table ziehung (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, zahl_zusatz INTEGER, \
                zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)")
               self.c.execute("select * from ziehung")
           lottodaten = self.c.fetchall()
           text =('Datum: {0} Zahlen: {1} {2} {3} {4} {5} {6}' \
            .format(lottodaten[block][0], lottodaten[block][1], lottodaten[block][2], lottodaten[block][3], 
             lottodaten[block][4], lottodaten[block][5], lottodaten[block][6]))
           self.lab_daten_gewinnz.setText(text)
        
    def ondaten_lottoschein(self):
       if not self.ls_laden_aktiv:
           block=self.edi_daten_lottoschein.textCursor().blockNumber()
           try:
               self.c.execute('select * from schein')
           except:
               self.c.execute("create table schein (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, laufzeit INTEGER)")
               self.c.execute("select * from schein")
           lottodaten = self.c.fetchall()
           text =('Datum: {0} Zahlen: {1} {2} {3} {4} {5} {6}' \
            .format(lottodaten[block][0], lottodaten[block][1], lottodaten[block][2], lottodaten[block][3],
             lottodaten[block][4], lottodaten[block][5], lottodaten[block][6]))
           self.lab_daten_lottoschein.setText(text)
        
 
    def onHilfe(self):
        """ Öffnen der Hilfe Datei im Browser
        """
        import webbrowser
        webbrowser.open_new('hilfe.html')

    def onInfo(self):
        """ Programm Info
        """
        text ='Eingabe der Gewinnzahlen von einer Ziehung\noder des Lottoscheins\n\n'
        text = text + 'Lizenz: Creative Commons by-sa\n'
        text = text + 'http://creativecommons.org/licenses/by-sa/3.0/deed.de'
        a = QtGui.QMessageBox()
        a.setWindowTitle('Info')
        a.setText(text)
        a.setInformativeText('Von Markus Hackspacher')
        a.exec_()
        
    def closeEvent(self, event):
        self.c.close()
        return
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Wirklich Beenden?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def spinBox_1clear(self):
        self.spinBox_Zahlen[0].setValue(0)
        self.spinBox_Zahlen[0].clear()
    def spinBox_2clear(self):
        self.spinBox_Zahlen[1].setValue(0)
        self.spinBox_Zahlen[1].clear()
    def spinBox_3clear(self):
        self.spinBox_Zahlen[2].setValue(0)
        self.spinBox_Zahlen[2].clear()
    def spinBox_4clear(self):
        self.spinBox_Zahlen[3].setValue(0)
        self.spinBox_Zahlen[3].clear()
    def spinBox_5clear(self):
        self.spinBox_Zahlen[4].setValue(0)
        self.spinBox_Zahlen[4].clear()
    def spinBox_6clear(self):
        self.spinBox_Zahlen[5].setValue(0)
        self.spinBox_Zahlen[5].clear()
    def spinBox_7clear(self):
        self.spinBox_Zahlen[6].setValue(0)
        self.spinBox_Zahlen[6].clear()

    def onEingabefeld_1(self):
        self.zahl = 1
        self.geaendert_btn()
    def onEingabefeld_2(self):
        self.zahl = 2
        self.geaendert_btn()
    def onEingabefeld_3(self):
        self.zahl = 3
        self.geaendert_btn()
    def onEingabefeld_4(self):
        self.zahl = 4
        self.geaendert_btn()
    def onEingabefeld_5(self):
        self.zahl = 5
        self.geaendert_btn()
    def onEingabefeld_6(self):
        self.zahl = 6
        self.geaendert_btn()
    def onEingabefeld_7(self):
        self.zahl = 7
        self.geaendert_btn()
    def onEingabefeld_8(self):
        self.zahl = 8
        self.geaendert_btn()
    def onEingabefeld_9(self):
        self.zahl = 9
        self.geaendert_btn()
    def onEingabefeld_10(self):
        self.zahl = 10
        self.geaendert_btn()
    def onEingabefeld_11(self):
        self.zahl = 11
        self.geaendert_btn()
    def onEingabefeld_12(self):
        self.zahl = 12
        self.geaendert_btn()
    def onEingabefeld_13(self):
        self.zahl = 13
        self.geaendert_btn()
    def onEingabefeld_14(self):
        self.zahl = 14
        self.geaendert_btn()
    def onEingabefeld_15(self):
        self.zahl = 15
        self.geaendert_btn()
    def onEingabefeld_16(self):
        self.zahl = 16
        self.geaendert_btn()
    def onEingabefeld_17(self):
        self.zahl = 17
        self.geaendert_btn()
    def onEingabefeld_18(self):
        self.zahl = 18
        self.geaendert_btn()
    def onEingabefeld_19(self):
        self.zahl = 19
        self.geaendert_btn()
    def onEingabefeld_20(self):
        self.zahl = 20
        self.geaendert_btn()
    def onEingabefeld_21(self):
        self.zahl = 21
        self.geaendert_btn()
    def onEingabefeld_22(self):
        self.zahl = 22
        self.geaendert_btn()
    def onEingabefeld_23(self):
        self.zahl = 23
        self.geaendert_btn()
    def onEingabefeld_24(self):
        self.zahl = 24
        self.geaendert_btn()
    def onEingabefeld_25(self):
        self.zahl = 25
        self.geaendert_btn()
    def onEingabefeld_26(self):
        self.zahl = 26
        self.geaendert_btn()
    def onEingabefeld_27(self):
        self.zahl = 27
        self.geaendert_btn()
    def onEingabefeld_28(self):
        self.zahl = 28
        self.geaendert_btn()
    def onEingabefeld_29(self):
        self.zahl = 29
        self.geaendert_btn()
    def onEingabefeld_30(self):
        self.zahl = 30
        self.geaendert_btn()
    def onEingabefeld_31(self):
        self.zahl = 31
        self.geaendert_btn()
    def onEingabefeld_32(self):
        self.zahl = 32
        self.geaendert_btn()
    def onEingabefeld_33(self):
        self.zahl = 33
        self.geaendert_btn()
    def onEingabefeld_34(self):
        self.zahl = 34
        self.geaendert_btn()
    def onEingabefeld_35(self):
        self.zahl = 35
        self.geaendert_btn()
    def onEingabefeld_36(self):
        self.zahl = 36
        self.geaendert_btn()
    def onEingabefeld_37(self):
        self.zahl = 37
        self.geaendert_btn()
    def onEingabefeld_38(self):
        self.zahl = 38
        self.geaendert_btn()
    def onEingabefeld_39(self):
        self.zahl = 39
        self.geaendert_btn()
    def onEingabefeld_40(self):
        self.zahl = 40
        self.geaendert_btn()
    def onEingabefeld_41(self):
        self.zahl = 41
        self.geaendert_btn()
    def onEingabefeld_42(self):
        self.zahl = 42
        self.geaendert_btn()
    def onEingabefeld_43(self):
        self.zahl = 43
        self.geaendert_btn()
    def onEingabefeld_44(self):
        self.zahl = 44
        self.geaendert_btn()
    def onEingabefeld_45(self):
        self.zahl = 45
        self.geaendert_btn()
    def onEingabefeld_46(self):
        self.zahl = 46
        self.geaendert_btn()
    def onEingabefeld_47(self):
        self.zahl = 47
        self.geaendert_btn()
    def onEingabefeld_48(self):
        self.zahl = 48
        self.geaendert_btn()
    def onEingabefeld_49(self):
        self.zahl = 49
        self.geaendert_btn()
    
    def focusSpinBox_1(self):
        self.geaendert()
    def focusSpinBox_2(self):
        self.geaendert()
    def focusSpinBox_3(self):
        self.geaendert()
    def focusSpinBox_4(self):
        self.geaendert()
    def focusSpinBox_5(self):
        self.geaendert()
    def focusSpinBox_6(self):
        self.geaendert()
    def focusSpinBox_7(self):
        self.geaendert()
    def oncalendarWidget(self):
        print 'oncalendarWidget'
        print self.calendarWidget.selectedDate()
     
    def onBtn_hinzu(self):
        """Datensatz hinzufügen"""
        datum = self.calendarWidget.selectedDate()
        day = datum.toPyDate()
        text = 'Daten hinzugefügt '+str(datum.day())+ '.' + str(datum.month())+ '.' + str(datum.year())
        
        if self.com_modus.currentIndex()==0:
            try:
               self.c.execute('select * from ziehung')
            except:
               self.c.execute("create table ziehung (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                 zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, zahl_zusatz INTEGER, \
                 zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)")
            self.c.execute("insert into ziehung(d, zahl_1, zahl_2,zahl_3,zahl_4,zahl_5,zahl_6, \
             zahl_zusatz,zahl_super , zahl_spiel77,zahl_spielsuper6) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, self.spinBox_1.value(), self.spinBox_2.value(), self.spinBox_3.value(), \
             self.spinBox_4.value(), self.spinBox_5.value(), self.spinBox_6.value(), self.spinBox_7.value(), \
             self.spinBox_superz.value(), self.spinBox_spiel77.value(), self.spinBox_super6.value()))
            self.edi_daten_gewinnz.appendPlainText(text)


        else:
            self.spinBox_1.value()
            try:
                self.c.execute('select * from schein')
            except:
                self.c.execute("create table schein (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                 zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, laufzeit INTEGER)")
            self.c.execute("insert into schein(d, zahl_1, zahl_2,zahl_3,zahl_4,zahl_5,zahl_6, \
             laufzeit) values (?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, self.spinBox_1.value(), self.spinBox_2.value(), self.spinBox_3.value(), \
             self.spinBox_4.value(), self.spinBox_5.value(), self.spinBox_6.value(), self.com_laufzeit.currentIndex()))
            self.edi_daten_lottoschein.appendPlainText(text)
        self.conn.commit()

    def onBtn_gz_auswerten(self):
        print 'onBtn_gz_auswerten', self.edi_daten_gewinnz.textCursor().blockNumber()

    def onBtn_ls_auswerten(self):
        print 'onBtn_ls_auswerten', self.edi_daten_gewinnz.textCursor().blockNumber()


    def onBtn_gz_anzeigen(self):
        print 'onBtn_gz_anzeigen', self.edi_daten_gewinnz.textCursor().blockNumber()

    def onBtn_ls_anzeigen(self):
        print 'onBtn_ls_anzeigen', self.edi_daten_gewinnz.textCursor().blockNumber()
        
    def onBtn_gz_loeschen(self):
        #self.c.rowcount = self.edi_daten_gewinnz.textCursor().blockNumber()
        #self.c.execute('DELETE FROM table')
        #self.conn.commit()
        self.onBtn_gz_laden()

    def onBtn_ls_loeschen(self):
        print 'onBtn_loesch', self.edi_daten_gewinnz.textCursor().blockNumber()

    def onBtn_ls_laden(self):
       """Read the Lottoschein from the Database
       loading into the QPlainTextEdit
       """
       self.ls_laden_aktiv = True
       self.edi_daten_lottoschein.setPlainText("")
       try:
            self.c.execute('select * from schein')
       except:
            self.c.execute("create table schein (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
             zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, laufzeit INTEGER)")
            self.c.execute("select * from schein")
       lottodaten = self.c.fetchone()
       while lottodaten!=None:
            self.edi_daten_lottoschein.appendPlainText('Datum: {0} Zahlen: {1} {2} {3} {4} {5} {6}' \
             .format(lottodaten[0], lottodaten[1], lottodaten[2], lottodaten[3], lottodaten[4], lottodaten[5], lottodaten[6]))
            lottodaten = self.c.fetchone()
       self.ls_laden_aktiv = False

    def onBtn_gz_laden(self):
       """Read the Gewinnzahlen from the Database
       loading into the QPlainTextEdit
       """
       self.gz_laden_aktiv = True
       self.edi_daten_gewinnz.setPlainText("")
       try:
           self.c.execute('select * from ziehung')
       except:
           self.c.execute("create table ziehung (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
             zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, zahl_zusatz INTEGER, \
             zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)")
           self.c.execute("select * from ziehung")
       lottodaten = self.c.fetchone()
       while lottodaten!=None:
           self.edi_daten_gewinnz.appendPlainText('Datum: {0} Zahlen: {1} {2} {3} {4} {5} {6}' \
             .format(lottodaten[0], lottodaten[1], lottodaten[2],lottodaten[3],lottodaten[4],lottodaten[5],lottodaten[6]))
           lottodaten = self.c.fetchone()
       self.gz_laden_aktiv = False
            
    def onBtn_Zufall(self):
        """ Die Zufallszahen generieren
        """
        from zufallszahl import zufallszahlen
        i_anzahl=6
        i_hochste=49
        zufallszahl=zufallszahlen(i_anzahl,i_hochste)
        for zahlen in xrange(6):
            self.spinBox_Zahlen[zahlen].setValue(zufallszahl[zahlen])
        self.zahl=0
        self.geaendert_btn()
        
    def onmodus(self):
        """ Wenn der Eingabe-Modus wechselt werden Schaltflächen an oder ab geschaltet
        """
        if self.com_modus.currentIndex()==1:
           self.Btn_Zufall.setVisible(True)
           self.com_laufzeit.setVisible(True)
           self.lab_laufzeit.setVisible(True)         
           self.spinBox_superz.setVisible(False)
           self.lab_superz.setVisible(False)
           self.spinBox_spiel77.setVisible(False)
           self.lab_spiel77.setVisible(False)
           self.spinBox_super6.setVisible(False)
           self.lab_super6.setVisible(False)
           self.lab_zusatz.setVisible(False)
           self.pinBox_Zahlen[6].setVisible(False)
           self.Btn_delete_Number[6].setVisible(False)
           self.spinBox_7clear()
           self.geaendert()

        else:
           self.Btn_Zufall.setVisible(False)
           self.com_laufzeit.setVisible(False)
           self.lab_laufzeit.setVisible(False)
           self.spinBox_superz.setVisible(True)
           self.lab_superz.setVisible(True)
           self.spinBox_spiel77.setVisible(True)
           self.lab_spiel77.setVisible(True)
           self.spinBox_super6.setVisible(True)
           self.lab_super6.setVisible(True)
           self.lab_zusatz.setVisible(True)
           self.spinBox_Zahlen[6].setVisible(True)
           self.Btn_delete_Number[6].setVisible(True)

    def onlaufzeit(self):
        print 'onlaufzeit',self.com_laufzeit.currentIndex()        

    def geaendert(self):
        """Überprüfen der SpinBoxen damit nicht zwei den gleichen Wert haben
        """
        a=[]
        a.append(self.spinBox_Zahlen[0].value())        
        a.append(self.spinBox_Zahlen[1].value())
        a.append(self.spinBox_Zahlen[2].value())
        a.append(self.spinBox_Zahlen[3].value())
        a.append(self.spinBox_Zahlen[4].value())
        a.append(self.spinBox_Zahlen[5].value())
        a.append(self.spinBox_Zahlen[6].value())
    
        #Setzen der Botton je nach Wert der Spinbox
        for button in xrange(49):
            if button + 1 in a:
                self.Btn_Numerary_1to49[button].setFlat(False)
            else:
                self.Btn_Numerary_1to49[button].setFlat(True)
                
    def geaendert_btn(self):
        if self.spinBox_Zahlen[0].value()==0:
            self.spinBox_Zahlen[0].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[0].value():
            self.spinBox_1clear()
        elif self.spinBox_Zahlen[1].value()==0:
            self.spinBox_Zahlen[1].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[1].value():
            self.spinBox_2clear()
        elif self.spinBox_Zahlen[2].value()==0:
            self.spinBox_Zahlen[2].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[2].value():
            self.spinBox_3clear()
        elif self.spinBox_Zahlen[3].value()==0:
            self.spinBox_Zahlen[3].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[3].value():
            self.spinBox_4clear()
        elif self.spinBox_Zahlen[4].value()==0:
            self.spinBox_Zahlen[4].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[4].value():
            self.spinBox_5clear()
        elif self.spinBox_Zahlen[5].value()==0:
            self.spinBox_Zahlen[5].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[5].value():
            self.spinBox_6clear()
        elif self.spinBox_Zahlen[6].value()==0 and self.com_modus.currentIndex()==0:
            self.spinBox_Zahlen[6].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[6].value() or self.com_modus.currentIndex()==1:
            self.spinBox_7clear()
        self.geaendert()

def gui():
    app = QtGui.QApplication(sys.argv) 
    dialog = MeinDialog() 
    dialog.show() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    gui()