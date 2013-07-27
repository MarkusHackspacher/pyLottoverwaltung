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
from PyQt4 import QtGui, QtCore, uic

from datahandler import Datahandler
import webzugriff
import auswertung
import kalender_datum


class MeinDialog(QtGui.QMainWindow):
    def __init__(self):
        """
        inital the main window
        1 to 49 button,
        7 spinbox,
        calender,
        datafield
        """
        QtGui.QDialog.__init__(self)
        self.ui = uic.loadUi(join("lotto/gui", "lotto_dateneing.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))

        #array of Button from 1 to 49
        self.ui.Btn_Numerary_1to49 = []
        for button in xrange(49):
            self.ui.Btn_Numerary_1to49.append(QtGui.QPushButton(
             self.ui.gridLayoutWidget))
            self.ui.Btn_Numerary_1to49[button].setMaximumSize(
             QtCore.QSize(58, 58))
            self.ui.gridLayout.addWidget(self.ui.Btn_Numerary_1to49[button],
             int(button / 7), int(button % 7), 1, 1)
            self.ui.Btn_Numerary_1to49[button].setAutoFillBackground(True)
            self.ui.Btn_Numerary_1to49[button].setText(str(button + 1))

        #set 6 SpinBox and 1
        self.ui.spinBox_Zahlen = []
        self.ui.Btn_delete_Number = []
        for zahlen in xrange(7):
            if zahlen != 6:
                self.ui.spinBox_Zahlen.append(QtGui.QSpinBox(
                 self.ui.horizontalLayoutWidget))
                self.ui.Btn_delete_Number.append(QtGui.QPushButton(
                 self.ui.horizontalLayoutWidget_2))
                self.ui.spinBox_Zahlen[zahlen].setMinimumSize(
                 QtCore.QSize(32, 20))
                self.ui.spinBox_Zahlen[zahlen].setMaximumSize(
                 QtCore.QSize(52, 32))
                self.ui.Btn_delete_Number[zahlen].setMinimumSize(
                 QtCore.QSize(32, 20))
                self.ui.Btn_delete_Number[zahlen].setMaximumSize(
                 QtCore.QSize(52, 20))
                self.ui.horizontalLayout.addWidget(
                 self.ui.spinBox_Zahlen[zahlen])
                self.ui.horizontalLayout_2.addWidget(
                 self.ui.Btn_delete_Number[zahlen])
            else:
                #set extra Spinbox
                self.ui.spinBox_Zahlen.append(QtGui.QSpinBox(self.ui.Lottozahlen))
                self.ui.spinBox_Zahlen[zahlen].setGeometry(QtCore.QRect(
                 130, 360, 51, 23))
                self.ui.Btn_delete_Number.append(QtGui.QPushButton(self.ui.Lottozahlen))
                self.ui.Btn_delete_Number[zahlen].setGeometry(QtCore.QRect(
                 190, 360, 41, 20))
            self.ui.spinBox_Zahlen[zahlen].setMaximum(49)
            self.ui.spinBox_Zahlen[zahlen].clear()
            self.ui.Btn_delete_Number[zahlen].setText("X")

        self.onmodus()
        self.geaendert()
        self.data_handler = Datahandler('datenbank1.sqlite')
        self.onBtn_gz_laden()
        self.onBtn_ls_laden()

        # slots for datanbase funktion
        self.ui.Btn_gz_anzeigen.clicked.connect(self.onBtn_gz_anzeigen)
        self.ui.Btn_ls_anzeigen.clicked.connect(self.onBtn_ls_anzeigen)
        self.ui.Btn_gz_loeschen.clicked.connect(self.onBtn_gz_loeschen)
        self.ui.Btn_gz_loeschen.setEnabled(False)
        self.ui.Btn_ls_loeschen.clicked.connect(self.onBtn_ls_loeschen)
        self.ui.Btn_ls_loeschen.setEnabled(False)
        self.ui.btn_ls_auswerten.clicked.connect(self.onBtn_ls_auswerten)
        self.ui.btn_ls_auswerten.setEnabled(False)
        self.ui.CBox_gz_kompl_ausgeben.clicked.connect(
         self.onCBox_gz_kompl_ausgeben)
        self.ui.btn_set_calender_today.clicked.connect(
         self.onbtn_set_calender_today)
        self.ui.btn_kalender.clicked.connect(self.onbtn_kalender)

        # fields fill with random numbers and give them to database
        self.ui.btn_zufall.clicked.connect(self.onbtn_zufall)
        self.ui.btn_hinzu.clicked.connect(self.onbtn_hinzu)
       # fields of draw numbers
        for number in xrange(7):
            self.spinBox_clear = functools.partial(
             self.spinBox_1to7_clear, number)
            self.ui.Btn_delete_Number[number].clicked.connect(self.spinBox_clear)
            self.focusSpinBox = functools.partial(
             self.focusSpinBox_1to7, number)
            self.ui.spinBox_Zahlen[number].valueChanged.connect(self.focusSpinBox)

        self.ui.com_modus.currentIndexChanged.connect(self.onmodus)

        # fields of 1 to 49 numbers
        for button in xrange(49):
            self.onEingabefeld = functools.partial(
             self.onEingabefeld_1to49, button + 1)
            self.ui.Btn_Numerary_1to49[button].clicked.connect(self.onEingabefeld)

        self.statusBar().showMessage('Bereit')

        self.ui.actionBeenden.triggered.connect(self.onClose)
        self.ui.actionInfo.triggered.connect(self.onInfo)
        self.ui.actionDaten_von_lotto_de.triggered.connect(self.onData_lottode)
        self.onData_lottozahlenonlinede_2000 = functools.partial(
         self.onData_lottozahlenonlinede, 2000, 2004)
        self.ui.actionDaten_von_lottozahlenonline_de_2000_2004.triggered.connect(
         self.onData_lottozahlenonlinede_2000)
        self.onData_lottozahlenonlinede_2005 = functools.partial(
         self.onData_lottozahlenonlinede, 2005, 2009)
        self.ui.actionDaten_von_lottozahlenonline_de_2005_2009.triggered.connect(
         self.onData_lottozahlenonlinede_2005)
        self.onData_lottozahlenonlinede_2010 = functools.partial(
         self.onData_lottozahlenonlinede, 2010, 2013)
        self.ui.actionDaten_von_lottozahlenonline_de_2010_2013.triggered.connect(
         self.onData_lottozahlenonlinede_2010)
        self.ui.edi_daten_gewinnz.cursorPositionChanged.connect(
         self.ondaten_gewinnz)
        self.ui.edi_daten_lottoschein.cursorPositionChanged.connect(
         self.ondaten_lottoschein)
        self.onbtn_set_calender_today()

        self.ui.show()

    def onbtn_kalender(self):
        """Kalender Dialog öffen"""
        dlg = kalender_datum.ui_kalender(
         self.ui.spinBox_jahr.value(),
         self.ui.spinBox_monat.value(),
         self.ui.spinbox_tag.value())
        if dlg.exec_() == 1:
            self.ui.spinbox_tag.setValue(dlg.kalender().day())
            self.ui.spinBox_monat.setValue(dlg.kalender().month())
            self.ui.spinBox_jahr.setValue(dlg.kalender().year())

    def ondaten_gewinnz(self):
        """
        Anzeigen der Gewinnzahlen an den Auswahlfeld
        Auslesen der Zeilennumer
        Den Text der Zeile in der Beschriftung ausgeben
        """
        block = self.ui.edi_daten_gewinnz.textCursor().blockNumber()
        text = self.ui.edi_daten_gewinnz.document(). \
         findBlockByNumber(block).text()
        self.ui.lab_daten_gewinnz.setText(text)
        self.ui.Btn_gz_loeschen.setEnabled(True)

    def ondaten_lottoschein(self):
        """
        Anzeigen der Daten des Lottoscheins an den Auswahlfeld
        Auslesen der Zeilennumer
        Den Text der Zeile in der Beschriftung ausgeben
        """
        block = self.ui.edi_daten_lottoschein.textCursor().blockNumber()
        text = self.ui.edi_daten_lottoschein.document(). \
         findBlockByNumber(block).text()
        self.ui.lab_daten_lottoschein.setText(text)
        self.ui.Btn_ls_loeschen.setEnabled(True)
        self.ui.btn_ls_auswerten.setEnabled(True)

    def onInfo(self):
        """ Programm Info
        """
        text = """Eingabe der Gewinnzahlen von einer Ziehung
        oder des Lottoscheins
        \n"""
        text = text + 'Lizenz: GNU GPLv3\n'
        text = text + 'http://www.gnu.org/licenses/'
        a = QtGui.QMessageBox()
        a.setWindowTitle('Info')
        a.setText(text)
        a.setInformativeText('Von Markus Hackspacher')
        a.exec_()

    def closeEvent(self, event):
        """ the program exit """
        return

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
        self.ui.spinbox_tag.setValue(int(datum[:2]))
        self.ui.spinBox_monat.setValue(int(datum[3:5]))
        self.ui.spinBox_jahr.setValue(int(datum[6:]))
        self.ui.spinBox_Zahlen[0].setValue(value[0])
        self.ui.spinBox_Zahlen[1].setValue(value[1])
        self.ui.spinBox_Zahlen[2].setValue(value[2])
        self.ui.spinBox_Zahlen[3].setValue(value[3])
        self.ui.spinBox_Zahlen[4].setValue(value[4])
        self.ui.spinBox_Zahlen[5].setValue(value[5])
        #self.spinBox_Zahlen[6].setValue(value[6])
        #04.05.2013 rules change, no Zusatzzahl
        self.ui.spinBox_superz.setValue(value[6])
        self.ui.spinBox_spiel77.setValue(value[7])
        self.ui.spinBox_super6.setValue(value[8])
        self.ui.com_modus.setCurrentIndex(0)
        self.geaendert()

    def onData_lottozahlenonlinede(self, first_year, last_year):
        """Load the draw from lottozahlenonline.de"""
        a = QtGui.QProgressDialog("Daten Einlesen", "Abbruch",
         first_year, last_year, self,
         QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        a.setWindowModality(QtCore.Qt.WindowModal)
        a.setValue(first_year)
        for z in range(first_year, last_year + 1):
            print z
            url = 'http://www.lottozahlenonline.de/statistik/beide-spieltage/lottozahlen-archiv.php?j={0}'.format(z)
            webzugriff.data_from_achiv(self.data_handler, url)
            a.setValue(z)
        a.close()
        self.onBtn_gz_laden()

    def spinBox_1to7_clear(self, number):
        """Die SpinBoxen 1 bis 6 und Zusatzzahl löschen"""
        self.ui.spinBox_Zahlen[number].setValue(0)
        self.ui.spinBox_Zahlen[number].clear()

    def onEingabefeld_1to49(self, zahl):
        """Ein Zahlenfelder 1 bis 49 wurde angeklickt"""
        self.zahl = zahl
        self.geaendert_btn()

    def focusSpinBox_1to7(self, number):
        """Ein Auswahlfelder der 7 Gewinnzahlen oder
        Lottoscheins hat sich geaendert"""
        self.geaendert()

    def onbtn_hinzu(self):
        """drawing numbers move in database """
        day = '{0:4}-{1:02}-{2:02}'.format(self.ui.spinBox_jahr.value(),
         self.ui.spinBox_monat.value(), self.ui.spinbox_tag.value())
        if self.ui.com_modus.currentIndex() == 0:
            self.data_handler.insert_ziehung(day, self.draw_numbers(),
             self.ui.spinBox_superz.value(), self.ui.spinBox_spiel77.value(),
             self.ui.spinBox_super6.value())
            self.ui.Btn_gz_loeschen.setEnabled(False)
            self.onBtn_gz_laden()
        else:
            self.data_handler.insert_schein(day, self.draw_numbers()[:-1],
             self.ui.com_laufzeit.currentIndex(),
             self.ui.com_laufzeit_tag.currentIndex(),
             self.ui.spinBox_spiel77.value())
            self.ui.Btn_ls_loeschen.setEnabled(False)
            self.onBtn_ls_laden()

    def onBtn_ls_auswerten(self):
        """den Lottoschein auswerten"""
        dlg = auswertung.ui_lotto_auswertung(self.data_handler.get_schein()[
         self.ui.edi_daten_lottoschein.textCursor().blockNumber()][0],
         self.data_handler)
        dlg.exec_()

    def onBtn_gz_anzeigen(self):
        """
        show drawing numbers
        Gewinnzahlen im großen Feld anzeigen
        """
        block = self.ui.edi_daten_gewinnz.textCursor().blockNumber()
        lottodaten = self.data_handler.get_ziehung()
        if lottodaten == []:
            return
        if not self.ui.CBox_gz_kompl_ausgeben.isChecked():
            lottodaten = lottodaten[-10:]
        self.ui.spinbox_tag.setValue(int(lottodaten[block][1][8:]))
        self.ui.spinBox_monat.setValue(int(lottodaten[block][1][5:7]))
        self.ui.spinBox_jahr.setValue(int(lottodaten[block][1][:4]))
        zahlen = lottodaten[block][5].split(',')
        self.ui.spinBox_Zahlen[0].setValue(int(zahlen[0]))
        self.ui.spinBox_Zahlen[1].setValue(int(zahlen[1]))
        self.ui.spinBox_Zahlen[2].setValue(int(zahlen[2]))
        self.ui.spinBox_Zahlen[3].setValue(int(zahlen[3]))
        self.ui.spinBox_Zahlen[4].setValue(int(zahlen[4]))
        self.ui.spinBox_Zahlen[5].setValue(int(zahlen[5]))
        if len(zahlen) > 6:
            self.ui.spinBox_Zahlen[6].setValue(int(zahlen[6]))
        self.ui.spinBox_superz.setValue(lottodaten[block][2])
        self.ui.spinBox_spiel77.setValue(lottodaten[block][3])
        self.ui.spinBox_super6.setValue(lottodaten[block][4])
        self.ui.com_modus.setCurrentIndex(0)
        self.geaendert()

    def onBtn_ls_anzeigen(self):
        """
        show tip numbers
        Lottoschein im großen Feld anzeigen,
        """
        block = self.ui.edi_daten_lottoschein.textCursor().blockNumber()
        lottodaten = self.data_handler.get_schein()
        if lottodaten == []:
            return
        self.ui.spinbox_tag.setValue(int(lottodaten[block][1][8:]))
        self.ui.spinBox_monat.setValue(int(lottodaten[block][1][5:7]))
        self.ui.spinBox_jahr.setValue(int(lottodaten[block][1][:4]))
        zahlen = lottodaten[block][5].split(',')
        self.ui.spinBox_Zahlen[0].setValue(int(zahlen[0]))
        self.ui.spinBox_Zahlen[1].setValue(int(zahlen[1]))
        self.ui.spinBox_Zahlen[2].setValue(int(zahlen[2]))
        self.ui.spinBox_Zahlen[3].setValue(int(zahlen[3]))
        self.ui.spinBox_Zahlen[4].setValue(int(zahlen[4]))
        self.ui.spinBox_Zahlen[5].setValue(int(zahlen[5]))

        self.ui.com_laufzeit.setCurrentIndex(lottodaten[block][2])
        self.ui.com_laufzeit_tag.setCurrentIndex(lottodaten[block][3])
        self.ui.spinBox_spiel77.setValue(lottodaten[block][4])
        self.ui.com_modus.setCurrentIndex(1)
        self.geaendert()

    def onBtn_gz_loeschen(self):
        """
        delete drawing numbers from the database
        Gewinnzahlen einer Ziehung aus der Datenbank loeschen
        """
        lottodaten = self.data_handler.get_ziehung()
        if lottodaten == []:
            return
        anzahl_datensaetze = len(lottodaten)
        if not self.ui.CBox_gz_kompl_ausgeben.isChecked() \
         and anzahl_datensaetze > 10:
            anzahl_datensaetze =- 10
        else:
            anzahl_datensaetze = 0
        self.data_handler.delete_ziehung(lottodaten
         [self.ui.edi_daten_gewinnz.textCursor().blockNumber()
         + anzahl_datensaetze][0])
        self.onBtn_gz_laden()

    def onBtn_ls_loeschen(self):
        """
        delete tip numbers from the database
        Lottoschein aus der Datenbank loeschen
        """
        lottodaten = self.data_handler.get_schein()
        if lottodaten == []:
            return
        self.data_handler.delete_schein(lottodaten
         [self.ui.edi_daten_lottoschein.textCursor().blockNumber()][0])
        self.onBtn_ls_laden()

    def onBtn_ls_laden(self):
        """Read the Lottoschein from the Database
        loading into the QPlainTextEdit
        """
        PlainText = QtGui.QPlainTextEdit()
        lottodaten = self.data_handler.get_schein()
        for schein in lottodaten:
            PlainText.appendPlainText('Datum: {0} Zahlen: {1}'
             .format(schein[1], schein[5]))
        self.ui.edi_daten_lottoschein.setPlainText(
         PlainText.document().toPlainText())
        self.ui.edi_daten_lottoschein.moveCursor(
         self.ui.edi_daten_lottoschein.textCursor().End)

    def onBtn_gz_laden(self):
        """Read the Gewinnzahlen from the Database
        loading into the QPlainTextEdit
        """
        PlainText = QtGui.QPlainTextEdit()
        lottodaten = self.data_handler.get_ziehung()
        if not self.ui.CBox_gz_kompl_ausgeben.isChecked():
            lottodaten = lottodaten[-10:]
        for i in lottodaten:
            PlainText.appendPlainText('Datum: {0} Zahlen: {1}'
             .format(i[1], i[5]))
        self.ui.edi_daten_gewinnz.setPlainText(PlainText.document().toPlainText())
        self.ui.edi_daten_gewinnz.moveCursor(
         self.ui.edi_daten_gewinnz.textCursor().End)

    def onCBox_gz_kompl_ausgeben(self):
        """
        CheckBox: Show the complete database in TextEdit
        """
        self.onBtn_gz_laden()

    def onbtn_zufall(self):
        """ Die Zufallszahen generieren
        """
        from zufallszahl import zufallszahlen
        i_anzahl = 6
        i_hochste = 49
        zufallszahl = zufallszahlen(i_anzahl, i_hochste)
        for zahlen in xrange(6):
            self.ui.spinBox_Zahlen[zahlen].setValue(zufallszahl[zahlen])
        self.zahl = 0
        self.geaendert_btn()

    def onbtn_set_calender_today(self):
        """set calender today"""
        self.ui.spinbox_tag.setValue(QtCore.QDate.currentDate().day())
        self.ui.spinBox_monat.setValue(QtCore.QDate.currentDate().month())
        self.ui.spinBox_jahr.setValue(QtCore.QDate.currentDate().year())

    def onmodus(self):
        """ Wenn der Eingabe-Modus wechselt werden
        Schaltflächen an oder ab geschaltet
        """
        if self.ui.com_modus.currentIndex() == 1:
            self.ui.btn_zufall.setVisible(True)
            self.ui.com_laufzeit.setVisible(True)
            self.ui.com_laufzeit_tag.setVisible(True)
            self.ui.lab_laufzeit.setVisible(True)
            self.ui.spinBox_superz.setVisible(False)
            self.ui.lab_superz.setVisible(False)
            self.ui.spinBox_spiel77.setVisible(True)
            self.ui.lab_spiel77.setVisible(False)
            self.ui.lab_scheinnr.setVisible(True)
            self.ui.spinBox_super6.setVisible(False)
            self.ui.lab_super6.setVisible(False)
            self.ui.lab_zusatz.setVisible(False)
            self.ui.spinBox_Zahlen[6].setVisible(False)
            self.ui.Btn_delete_Number[6].setVisible(False)
            self.spinBox_1to7_clear(6)
            self.geaendert()

        else:
            self.ui.btn_zufall.setVisible(False)
            self.ui.com_laufzeit.setVisible(False)
            self.ui.com_laufzeit_tag.setVisible(False)
            self.ui.lab_laufzeit.setVisible(False)
            self.ui.spinBox_superz.setVisible(True)
            self.ui.lab_superz.setVisible(True)
            self.ui.spinBox_spiel77.setVisible(True)
            self.ui.lab_spiel77.setVisible(True)
            self.ui.lab_scheinnr.setVisible(False)
            self.ui.spinBox_super6.setVisible(True)
            self.ui.lab_super6.setVisible(True)
            self.ui.lab_zusatz.setVisible(True)
            self.ui.spinBox_Zahlen[6].setVisible(True)
            self.ui.Btn_delete_Number[6].setVisible(True)
            self.geaendert()

    def geaendert(self):
        """Überprüfen der SpinBoxen damit nicht zwei den gleichen Wert haben
        """
        a = self.draw_numbers()
        #Setzen der Botton je nach Wert der Spinbox
        for button in xrange(49):
            if button + 1 in a:
                self.ui.Btn_Numerary_1to49[button].setFlat(False)
                self.ui.Btn_Numerary_1to49[button].setStyleSheet("color: red;")
                if button + 1 == self.ui.spinBox_Zahlen[6].value():
                    self.ui.Btn_Numerary_1to49[button].setStyleSheet(
                     "color: blue;")
            else:
                self.ui.Btn_Numerary_1to49[button].setFlat(True)
                self.ui.Btn_Numerary_1to49[button].setStyleSheet("color: black;")

    def geaendert_btn(self):
        """in den SpinBoxen die Nummern der Zahlen 1 bis 49 anzeigen
        wenn die Zahl abgewaehlt wird, wird auch der
        Wert der entsprechende Spinbox geloescht
        """
        a = self.draw_numbers()

        for number in xrange(6):
            if self.ui.spinBox_Zahlen[number].value() == 0 \
             and not (self.zahl in a):
                self.ui.spinBox_Zahlen[number].setValue(self.zahl)
                break
            elif self.zahl == self.ui.spinBox_Zahlen[number].value():
                self.spinBox_1to7_clear(number)
                self.zahl = 0

        a = self.draw_numbers()
        if self.ui.spinBox_Zahlen[6].value() == 0 \
         and self.ui.com_modus.currentIndex() == 0 \
         and not (self.zahl in a):
            self.ui.spinBox_Zahlen[6].setValue(self.zahl)
        elif self.zahl == self.ui.spinBox_Zahlen[6].value() \
         or self.ui.com_modus.currentIndex() == 1:
            self.spinBox_1to7_clear(6)
        self.geaendert()

    def draw_numbers(self):
        """
        this numbers are in the draw
        """
        a = []
        a.append(self.ui.spinBox_Zahlen[0].value())
        a.append(self.ui.spinBox_Zahlen[1].value())
        a.append(self.ui.spinBox_Zahlen[2].value())
        a.append(self.ui.spinBox_Zahlen[3].value())
        a.append(self.ui.spinBox_Zahlen[4].value())
        a.append(self.ui.spinBox_Zahlen[5].value())
        a.append(self.ui.spinBox_Zahlen[6].value())
        return a

    def onClose(self):
        self.ui.close()


def gui():
    app = QtGui.QApplication(sys.argv)
    dialog = MeinDialog()
    sys.exit(app.exec_())

if __name__ == "__main__":
    gui()
