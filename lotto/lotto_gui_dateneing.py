#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pyLottoverwaltung

Copyright (C) <2012-2013> Markus Hackspacher

This file is part of pyLottoverwaltung.

pyLottoverwaltung is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyLottoverwaltung is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyLottoverwaltung.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import sqlite3
import functools
from os.path import join
from PyQt4 import QtGui, QtCore

from gui.lotto_dateneing import Ui_MainWindow as Dlg
from datahandler import Datahandler
from gui.lotto_dialog import Ui_Dialog
import webzugriff
import auswertung

class ui_lotto_Dialog(QtGui.QDialog, Ui_Dialog): 
    def __init__(self, typ, data_handler, rowid):
        """open analyze dialog
        Datenauswerte Dialog oeffnen
        @param typ: 0 == Gewinnzahlen, 1 == Lottoschein
        @param rowid: is the rowid number of the database
        @type typ: int
        @type rowid: int
        @return: give close(0) or accept(1) back
        """
        QtGui.QDialog.__init__(self) 
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.setupUi(self)
        infotext = 'Gewinnzahlen'
        if typ == 1:
            infotext = 'Lottoschein'        
            lottodaten = data_handler.get_schein(rowid)
        else:
            lottodaten = data_handler.get_ziehung(rowid)
            
        self.setWindowTitle(infotext)
        self.plainTextEdit.appendPlainText('Datensatz RowID: {0} Datum: {1}'.
        format(rowid, lottodaten[0][0]))

        #set 6 SpinBox and 1 
        self.spinBox_Zahlen = []
        for zahlen in xrange(6):
            self.spinBox_Zahlen.append(QtGui.QSpinBox(self.horizontalLayoutWidget))
        self.spinBox_Zahlen.append(QtGui.QSpinBox(self))
        for zahlen in xrange(7):
            if zahlen != 6:
                self.spinBox_Zahlen[zahlen].setMinimumSize(QtCore.QSize(32, 20))
                self.spinBox_Zahlen[zahlen].setMaximumSize(QtCore.QSize(52, 32))
                self.horizontalLayout.addWidget(self.spinBox_Zahlen[zahlen])
            else:
                #set extra Spinbox
                self.spinBox_Zahlen[zahlen].setGeometry(QtCore.QRect(140, 170, 51, 23))
            self.spinBox_Zahlen[zahlen].setMaximum(49)
            self.spinBox_Zahlen[zahlen].clear()

        self.spinBox_Zahlen[0].setValue(lottodaten[0][1])
        self.spinBox_Zahlen[1].setValue(lottodaten[0][2])
        self.spinBox_Zahlen[2].setValue(lottodaten[0][3])
        self.spinBox_Zahlen[3].setValue(lottodaten[0][4])
        self.spinBox_Zahlen[4].setValue(lottodaten[0][5])
        self.spinBox_Zahlen[5].setValue(lottodaten[0][6])

        if typ == 1:
            self.com_laufzeit.setCurrentIndex(lottodaten[0][7])
            if lottodaten[0][8] == None:
                index = 0
            else:
                index = lottodaten[0][8]           
            self.com_laufzeit_tag.setCurrentIndex(index)
            if lottodaten[0][9] == None:
                index = 0
            else:
                index = lottodaten[0][9]
            self.spinBox_spiel77.setValue(index)

            self.spinBox_Zahlen[6].setVisible(False)
            self.spinBox_superz.setVisible(False)
            self.lab_superz.setVisible(False)
            self.spinBox_spiel77.setVisible(True)
            self.lab_spiel77.setVisible(False)
            self.lab_scheinnr.setVisible(True)
            self.spinBox_super6.setVisible(False)
            self.lab_super6.setVisible(False)
            self.lab_zusatz.setVisible(False)
           
        else:
            self.spinBox_Zahlen[6].setValue(lottodaten[0][7])
            self.spinBox_superz.setValue(lottodaten[0][8])
            self.spinBox_spiel77.setValue(lottodaten[0][9])
            self.spinBox_super6.setValue(lottodaten[0][10])
            self.spinBox_Zahlen[6].setVisible(True)
            self.com_laufzeit.setVisible(False)
            self.com_laufzeit_tag.setVisible(False)
            self.lab_laufzeit.setVisible(False)         
            self.lab_scheinnr.setVisible(False)
            
        self.onbtn_save = functools.partial(self.onbtn_save_index, typ, rowid, lottodaten[0][0])
        self.connect(self.btn_save, QtCore.SIGNAL('clicked()'), self.onbtn_save)
        self.buttonBox.accepted.connect(self.accept)
         
    def onbtn_save_index(self, typ , rowid, date_of):
        """drawing numbers move in database """
        if typ == 0:
            data_handler.update_ziehung(rowid ,date_of, self.spinBox_Zahlen[0].value(), \
             self.spinBox_Zahlen[1].value(), self.spinBox_Zahlen[2].value(), \
             self.spinBox_Zahlen[3].value(), self.spinBox_Zahlen[4].value(), \
             self.spinBox_Zahlen[5].value(), self.spinBox_Zahlen[6].value(), \
             self.spinBox_superz.value(), self.spinBox_spiel77.value(), self.spinBox_super6.value())
        else:
            data_handler.update_schein(rowid ,date_of, self.spinBox_Zahlen[0].value(), \
             self.spinBox_Zahlen[1].value(), self.spinBox_Zahlen[2].value(), \
             self.spinBox_Zahlen[3].value(), self.spinBox_Zahlen[4].value(), \
             self.spinBox_Zahlen[5].value(), self.com_laufzeit.currentIndex(), \
             self.com_laufzeit_tag.currentIndex(), self.spinBox_spiel77.value())
        self.accept()

class MeinDialog(QtGui.QMainWindow, Dlg): 
    def __init__(self):
        """
        inital the main window
        1 to 49 button,
        7 spinbox,
        calender,
        datafield
        """
        QtGui.QDialog.__init__(self) 
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.setupUi(self)
        #array of Button from 1 to 49
        self.Btn_Numerary_1to49 = []
        for button in xrange(49):
            self.Btn_Numerary_1to49.append(QtGui.QPushButton(self.gridLayoutWidget))
        for button in xrange(49):
            self.Btn_Numerary_1to49[button].setMaximumSize(QtCore.QSize(58, 58))
            self.gridLayout.addWidget(self.Btn_Numerary_1to49[button], \
             int(button / 7),  int(button % 7), 1, 1)
            self.Btn_Numerary_1to49[button].setAutoFillBackground(True)
            self.Btn_Numerary_1to49[button].setText(QtGui.QApplication.translate("MainWindow", str(button + 1), 
             None, QtGui.QApplication.UnicodeUTF8))
    
        #set 6 SpinBox and 1 
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
                #set extra Spinbox
                self.spinBox_Zahlen[zahlen].setGeometry(QtCore.QRect(130, 360, 51, 23))
                self.Btn_delete_Number[zahlen].setGeometry(QtCore.QRect(190, 360, 41, 20)) 
            self.spinBox_Zahlen[zahlen].setMaximum(49)
            self.spinBox_Zahlen[zahlen].clear()
            self.Btn_delete_Number[zahlen].setText(QtGui.QApplication.translate( \
             "MainWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
 
 
        self.onmodus()
        self.geaendert()
        self.data_handler = Datahandler('datenbank1.sqlite')
        self.onBtn_gz_laden()
        self.onBtn_ls_laden()        
        
        # slots for datanbase funktion
        self.connect(self.Btn_gz_anzeigen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_anzeigen)
        self.connect(self.Btn_ls_anzeigen,QtCore.SIGNAL("clicked()"), self.onBtn_ls_anzeigen)
        self.connect(self.Btn_gz_loeschen,QtCore.SIGNAL("clicked()"), self.onBtn_gz_loeschen)
        self.Btn_gz_loeschen.setEnabled(False)
        self.connect(self.Btn_ls_loeschen,QtCore.SIGNAL("clicked()"), self.onBtn_ls_loeschen)
        self.Btn_ls_loeschen.setEnabled(False)
        self.connect(self.btn_gz_aendern,QtCore.SIGNAL("clicked()"), self.onBtn_gz_aendern)
        self.btn_gz_aendern.setEnabled(False)
        self.connect(self.btn_ls_aendern,QtCore.SIGNAL("clicked()"), self.onBtn_ls_aendern)
        self.btn_ls_aendern.setEnabled(False)
        self.connect(self.btn_ls_auswerten,QtCore.SIGNAL("clicked()"), self.onBtn_ls_auswerten)
        self.btn_ls_auswerten.setEnabled(False)
        self.connect(self.CBox_gz_kompl_ausgeben,QtCore.SIGNAL("clicked()"), self.onCBox_gz_kompl_ausgeben)
       
        self.connect(self.Btn_set_calender_today,QtCore.SIGNAL("clicked()"), self.onBtn_set_calender_today)

        # fields fill with random numbers and give them to database
        self.connect(self.Btn_Zufall,QtCore.SIGNAL("clicked()"), self.onBtn_Zufall)
        self.connect(self.Btn_hinzu,QtCore.SIGNAL("clicked()"), self.onBtn_hinzu) 

        # fields of draw numbers
        for number in xrange(7):
            self.spinBox_clear = functools.partial(self.spinBox_1to7_clear, number)
            self.connect(self.Btn_delete_Number[0], QtCore.SIGNAL("clicked()"), self.spinBox_clear)
            self.focusSpinBox = functools.partial(self.focusSpinBox_1to7, number)
            self.connect(self.spinBox_Zahlen[0],QtCore.SIGNAL("valueChanged(int)"), self.focusSpinBox)

        self.connect(self.com_modus,QtCore.SIGNAL("currentIndexChanged(int)"), self.onmodus)

        # fields of 1 to 49 numbers
        for button in xrange(49):
            self.onEingabefeld = functools.partial(self.onEingabefeld_1to49, button + 1)
            self.connect(self.Btn_Numerary_1to49[button], QtCore.SIGNAL("clicked()"), self.onEingabefeld)
        
        self.statusBar().showMessage('Bereit')

        self.connect(self.actionBeenden, 
         QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(self.actionInfo, 
         QtCore.SIGNAL('triggered()'), self.onInfo)
        self.connect(self.actionDaten_von_lotto_de,
         QtCore.SIGNAL('triggered()'), self.onData_lottode)
        self.onData_lottozahlenonlinede_2000 = functools.partial \
         (self.onData_lottozahlenonlinede, 2000, 2004)
        self.connect(self.actionDaten_von_lottozahlenonline_de_2000_2004,
         QtCore.SIGNAL('triggered()'), self.onData_lottozahlenonlinede_2000)
        self.onData_lottozahlenonlinede_2005 = functools.partial \
         (self.onData_lottozahlenonlinede, 2005, 2009)
        self.connect(self.actionDaten_von_lottozahlenonline_de_2005_2009,
         QtCore.SIGNAL('triggered()'), self.onData_lottozahlenonlinede_2005)
        self.onData_lottozahlenonlinede_2010 = functools.partial \
         (self.onData_lottozahlenonlinede, 2010, 2013)
        self.connect(self.actionDaten_von_lottozahlenonline_de_2010_2013,
         QtCore.SIGNAL('triggered()'), self.onData_lottozahlenonlinede_2010)
        self.connect(self.edi_daten_gewinnz, 
         QtCore.SIGNAL('cursorPositionChanged()'), self.ondaten_gewinnz)
        self.connect(self.edi_daten_lottoschein, 
         QtCore.SIGNAL('cursorPositionChanged()'), self.ondaten_lottoschein)
 
    def ondaten_gewinnz(self):
       """
       Anzeigen der Gewinnzahlen an den Auswahlfeld
       Auslesen der Zeilennumer
       Den Text der Zeile in der Beschriftung ausgeben
       """
       block=self.edi_daten_gewinnz.textCursor().blockNumber()
       text = self.edi_daten_gewinnz.document().findBlockByNumber(block).text()
       self.lab_daten_gewinnz.setText(text)
       self.Btn_gz_loeschen.setEnabled(True)
       self.btn_gz_aendern.setEnabled(True)
        
    def ondaten_lottoschein(self):
       """
       Anzeigen der Daten des Lottoscheins an den Auswahlfeld
       Auslesen der Zeilennumer
       Den Text der Zeile in der Beschriftung ausgeben
       """
       block=self.edi_daten_lottoschein.textCursor().blockNumber()               
       text = self.edi_daten_lottoschein.document().findBlockByNumber(block).text()
       self.lab_daten_lottoschein.setText(text)       
       self.Btn_ls_loeschen.setEnabled(True)
       self.btn_ls_auswerten.setEnabled(True)
       self.btn_ls_aendern.setEnabled(True)

 
    def onInfo(self):
        """ Programm Info
        """
        text ='Eingabe der Gewinnzahlen von einer Ziehung\noder des Lottoscheins\n\n'
        text = text + 'Lizenz: GNU GPLv3\n'
        text = text + 'http://www.gnu.org/licenses/'
        a = QtGui.QMessageBox()
        a.setWindowTitle('Info')
        a.setText(text)
        a.setInformativeText('Von Markus Hackspacher')
        a.exec_()
        
    def closeEvent(self, event):
        """ the program exit """
        self.data_handler.close()
    
    def onData_lottode(self):
        """Load the actual draw from lotto.de"""        
        try: 
            datum, value = webzugriff.data_from_webpage()
        except:
            a = QtGui.QMessageBox()
            a.setWindowTitle('Info')
            a.setText('Daten konnten nicht geladen werden')
            a.exec_()
            return
            
        self.calendarWidget.setSelectedDate(QtCore.QDate.fromString(datum,"dd.MM.yyyy"))       
        self.spinBox_Zahlen[0].setValue(value[0])
        self.spinBox_Zahlen[1].setValue(value[1])
        self.spinBox_Zahlen[2].setValue(value[2])
        self.spinBox_Zahlen[3].setValue(value[3])
        self.spinBox_Zahlen[4].setValue(value[4])
        self.spinBox_Zahlen[5].setValue(value[5])
        self.spinBox_Zahlen[6].setValue(value[6])
        self.spinBox_superz.setValue(value[7])
        self.spinBox_spiel77.setValue(value[8])
        self.spinBox_super6.setValue(value[9])
        self.com_modus.setCurrentIndex(0)
        self.geaendert()
        
    def onData_lottozahlenonlinede(self, first_year, last_year):
        """Load the draw from lottozahlenonline.de"""
        a = QtGui.QProgressDialog("Daten Einlesen", "Abbruch",
         first_year, last_year, self, QtCore.Qt.Dialog|QtCore.Qt.WindowTitleHint)
        a.setWindowModality(QtCore.Qt.WindowModal)
        a.setValue(first_year)
        for z in range(first_year, last_year+1):
            url = 'http://www.lottozahlenonline.de/statistik/beide-spieltage/lottozahlen-archiv.php?j={0}'.format(z)
            webzugriff.data_from_achiv(self.data_handler, url)
            a.setValue(z)      
        a.close()
        self.onBtn_gz_laden()

    def spinBox_1to7_clear(self, number):
        """Die SpinBoxen 1 bis 6 und Zusatzzahl löschen"""
        self.spinBox_Zahlen[number].setValue(0)
        self.spinBox_Zahlen[number].clear()

    def onEingabefeld_1to49(self,zahl):
        """Ein Zahlenfelder 1 bis 49 wurde angeklickt"""
        self.zahl = zahl
        self.geaendert_btn()
            
    def focusSpinBox_1to7(self, number):
        """Ein Auswahlfelder der 7 Gewinnzahlen oder Lottoscheins hat sich geaendert"""
        self.geaendert()
     
    def onBtn_hinzu(self):
        """drawing numbers move in database """
        datum = self.calendarWidget.selectedDate()
        day = datum.toPyDate()       
        if self.com_modus.currentIndex()==0:
            self.data_handler.insert_ziehung(day, self.draw_numbers(),
             self.spinBox_superz.value(), self.spinBox_spiel77.value(), self.spinBox_super6.value())
            self.Btn_gz_loeschen.setEnabled(False)
            self.onBtn_gz_laden()
        else:
            self.data_handler.insert_schein(day, self.spinBox_Zahlen[0].value(),
             self.spinBox_Zahlen[1].value(), self.spinBox_Zahlen[2].value(),
             self.spinBox_Zahlen[3].value(), self.spinBox_Zahlen[4].value(),
             self.spinBox_Zahlen[5].value(), self.com_laufzeit.currentIndex(),
             self.com_laufzeit_tag.currentIndex(), self.spinBox_spiel77.value())
            self.Btn_ls_loeschen.setEnabled(False)
            self.onBtn_ls_laden()
            

    def onBtn_gz_aendern(self):
        """Gewinnzahlen anzeigen und änderen
        """
        anzahl_datensaetze = len(self.data_handler.get_ziehung())
        if not self.CBox_gz_kompl_ausgeben.isChecked() \
         and anzahl_datensaetze > 10:
            anzahl_datensaetze =- 10
        else:
            anzahl_datensaetze = 0
        rowid = self.data_handler.get_ziehung()[ 
         self.edi_daten_gewinnz.textCursor().blockNumber() + anzahl_datensaetze][0]
        dlg = ui_lotto_Dialog(0, self.data_handler, rowid)
        dlg.exec_()
        self.onBtn_gz_laden()

    def onBtn_ls_aendern(self):
        """Lottoschein anzeigen und änderen
        """      
        dlg = ui_lotto_Dialog(1, self.data_handler, self.data_handler.get_schein()[
         self.edi_daten_lottoschein.textCursor().blockNumber()][0])
        dlg.exec_()
        self.onBtn_ls_laden()
                
    def onBtn_ls_auswerten(self):
        """den Lottoschein auswerten"""
        dlg = auswertung.ui_lotto_auswertung(self.data_handler.get_schein()[
         self.edi_daten_lottoschein.textCursor().blockNumber()][0], self.data_handler)
        dlg.exec_()

    def onBtn_gz_anzeigen(self):
        """
        show drawing numbers
        Gewinnzahlen im großen Feld anzeigen
        """
        block=self.edi_daten_gewinnz.textCursor().blockNumber()
        lottodaten = self.data_handler.get_ziehung()
        if not self.CBox_gz_kompl_ausgeben.isChecked():
            lottodaten = lottodaten[-10:]
        self.calendarWidget.setSelectedDate(QtCore.QDate.fromString(lottodaten[block][1],"yyyy-MM-dd"))       
        self.spinBox_Zahlen[0].setValue(lottodaten[block][2])
        self.spinBox_Zahlen[1].setValue(lottodaten[block][3])
        self.spinBox_Zahlen[2].setValue(lottodaten[block][4])
        self.spinBox_Zahlen[3].setValue(lottodaten[block][5])
        self.spinBox_Zahlen[4].setValue(lottodaten[block][6])
        self.spinBox_Zahlen[5].setValue(lottodaten[block][7])
        self.spinBox_Zahlen[6].setValue(lottodaten[block][8])
        self.spinBox_superz.setValue(lottodaten[block][9])
        self.spinBox_spiel77.setValue(lottodaten[block][10])
        self.spinBox_super6.setValue(lottodaten[block][11])
        self.com_modus.setCurrentIndex(0)
        self.geaendert()

    def onBtn_ls_anzeigen(self):
        """
        show tip numbers
        Lottoschein im großen Feld anzeigen,
        """
        block=self.edi_daten_lottoschein.textCursor().blockNumber()
        lottodaten = self.data_handler.get_schein()
        if len(lottodaten[block]) < 10:
            self.data_handler.add_columns()
            lottodaten = self.data_handler.get_schein()
        self.calendarWidget.setSelectedDate(QtCore.QDate.fromString(lottodaten[block][1],"yyyy-MM-dd"))       
        self.spinBox_Zahlen[0].setValue(lottodaten[block][2])
        self.spinBox_Zahlen[1].setValue(lottodaten[block][3])
        self.spinBox_Zahlen[2].setValue(lottodaten[block][4])
        self.spinBox_Zahlen[3].setValue(lottodaten[block][5])
        self.spinBox_Zahlen[4].setValue(lottodaten[block][6])
        self.spinBox_Zahlen[5].setValue(lottodaten[block][7])
        self.com_laufzeit.setCurrentIndex(lottodaten[block][8])
        if lottodaten[block][9] == None:
            index = 0
        else:
            index = lottodaten[block][9]
        self.com_laufzeit_tag.setCurrentIndex(index)
        if lottodaten[block][10] == None:
            index = 0
        else:
            index = lottodaten[block][10]
        self.spinBox_spiel77.setValue(index)
        self.com_modus.setCurrentIndex(1)
        #self.onmodus()
        self.geaendert()
        
    def onBtn_gz_loeschen(self):
        """ 
        delete drawing numbers from the database
        Gewinnzahlen einer Ziehung aus der Datenbank loeschen
        """           
        anzahl_datensaetze = len(self.data_handler.get_ziehung())
        if not self.CBox_gz_kompl_ausgeben.isChecked():
            anzahl_datensaetze =- 10
        else:
            anzahl_datensaetze = 0
        self.data_handler.delete_ziehung(self.data_handler.get_ziehung() 
         [self.edi_daten_gewinnz.textCursor().blockNumber() + anzahl_datensaetze][0])
        self.onBtn_gz_laden()

    def onBtn_ls_loeschen(self):
        """
        delete tip numbers from the database
        Lottoschein aus der Datenbank loeschen
        """        
        self.data_handler.delete_schein(self.data_handler.get_schein()
         [self.edi_daten_lottoschein.textCursor().blockNumber()][0])
        self.onBtn_ls_laden()

    def onBtn_ls_laden(self):
        """Read the Lottoschein from the Database
        loading into the QPlainTextEdit
        """
        PlainText = QtGui.QPlainTextEdit()
        lottodaten = self.data_handler.get_schein()
        for schein in lottodaten:
            PlainText.appendPlainText('Datum: {0} Zahlen: {1}, {2}, {3}, {4}, {5}, {6}'
             .format(schein[1], schein[2], schein[3], schein[4], schein[5], schein[6], schein[7]))
        self.edi_daten_lottoschein.setPlainText(PlainText.document().toPlainText())
        self.edi_daten_lottoschein.moveCursor(self.edi_daten_lottoschein.textCursor().End)

    def onBtn_gz_laden(self):
        """Read the Gewinnzahlen from the Database
        loading into the QPlainTextEdit
        """
        PlainText = QtGui.QPlainTextEdit()
        lottodaten = self.data_handler.get_ziehung()
        if not self.CBox_gz_kompl_ausgeben.isChecked():
            lottodaten = lottodaten[-10:]
        for i in lottodaten:
           PlainText.appendPlainText('Datum: {0} | {1}'
            .format(i[1], i[5]))
        self.edi_daten_gewinnz.setPlainText(PlainText.document().toPlainText())
        self.edi_daten_gewinnz.moveCursor(self.edi_daten_gewinnz.textCursor().End)
            
    def onCBox_gz_kompl_ausgeben(self):
        """
        CheckBox: Show the complete database in TextEdit
        """
        self.onBtn_gz_laden()
   
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
        
    def onBtn_set_calender_today(self):
        """set calender today"""
        self.calendarWidget.setSelectedDate(QtCore.QDate.currentDate())       

    def onmodus(self):
        """ Wenn der Eingabe-Modus wechselt werden Schaltflächen an oder ab geschaltet
        """
        if self.com_modus.currentIndex()==1:
            self.Btn_Zufall.setVisible(True)
            self.com_laufzeit.setVisible(True)
            self.com_laufzeit_tag.setVisible(True)
            self.lab_laufzeit.setVisible(True)         
            self.spinBox_superz.setVisible(False)
            self.lab_superz.setVisible(False)
            self.spinBox_spiel77.setVisible(True)
            self.lab_spiel77.setVisible(False)
            self.lab_scheinnr.setVisible(True)
            self.spinBox_super6.setVisible(False)
            self.lab_super6.setVisible(False)
            self.lab_zusatz.setVisible(False)
            self.spinBox_Zahlen[6].setVisible(False)
            self.Btn_delete_Number[6].setVisible(False)
            self.spinBox_1to7_clear(6)
            self.geaendert()

        else:
            self.Btn_Zufall.setVisible(False)
            self.com_laufzeit.setVisible(False)
            self.com_laufzeit_tag.setVisible(False)
            self.lab_laufzeit.setVisible(False)
            self.spinBox_superz.setVisible(True)
            self.lab_superz.setVisible(True)
            self.spinBox_spiel77.setVisible(True)
            self.lab_spiel77.setVisible(True)
            self.lab_scheinnr.setVisible(False)
            self.spinBox_super6.setVisible(True)
            self.lab_super6.setVisible(True)
            self.lab_zusatz.setVisible(True)
            self.spinBox_Zahlen[6].setVisible(True)
            self.Btn_delete_Number[6].setVisible(True)
            self.geaendert()

    def geaendert(self):
        """Überprüfen der SpinBoxen damit nicht zwei den gleichen Wert haben
        """
        a = self.draw_numbers()        
        #Setzen der Botton je nach Wert der Spinbox
        for button in xrange(49):
            if button + 1 in a:
                self.Btn_Numerary_1to49[button].setFlat(False)               
                self.Btn_Numerary_1to49[button].setStyleSheet("color: red;")
                if button + 1 == self.spinBox_Zahlen[6].value():
                    self.Btn_Numerary_1to49[button].setStyleSheet("color: blue;")                
            else:
                self.Btn_Numerary_1to49[button].setFlat(True)
                self.Btn_Numerary_1to49[button].setStyleSheet("color: black;")
                
    def geaendert_btn(self):
        """in den SpinBoxen die Nummern der Zahlen 1 bis 49 anzeigen
        wenn die Zahl abgewaehlt wird, wird auch der Wert der entsprechende Spinbox geloescht
        """
        a = self.draw_numbers()        

        for number in xrange(6):
            if self.spinBox_Zahlen[number].value()==0 and not (self.zahl in a):
                self.spinBox_Zahlen[number].setValue(self.zahl)
                break
            elif self.zahl == self.spinBox_Zahlen[number].value():
                self.spinBox_1to7_clear(number)
                self.zahl = 0
                
        a = self.draw_numbers()          
        if self.spinBox_Zahlen[6].value()==0 and self.com_modus.currentIndex()==0 and not (self.zahl in a):
            self.spinBox_Zahlen[6].setValue(self.zahl)
        elif self.zahl == self.spinBox_Zahlen[6].value() or self.com_modus.currentIndex()==1:
            self.spinBox_1to7_clear(6)
        self.geaendert()

    def draw_numbers(self):
        """
        this numbers are in the draw
        """
        a=[]
        a.append(self.spinBox_Zahlen[0].value())        
        a.append(self.spinBox_Zahlen[1].value())
        a.append(self.spinBox_Zahlen[2].value())
        a.append(self.spinBox_Zahlen[3].value())
        a.append(self.spinBox_Zahlen[4].value())
        a.append(self.spinBox_Zahlen[5].value())
        a.append(self.spinBox_Zahlen[6].value())
        return a

def gui():
    app = QtGui.QApplication(sys.argv) 
    dialog = MeinDialog() 
    dialog.show() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    gui()
