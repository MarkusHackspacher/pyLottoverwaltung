#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyLottoverwaltung

# Copyright (C) <2012-2017> Markus Hackspacher

# This file is part of pyLottoverwaltung.

# pyLottoverwaltung is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pyLottoverwaltung is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pyLottoverwaltung.  If not, see <http://www.gnu.org/licenses/>.


import functools
import random
import sys
import webbrowser
from os.path import join

import lotto.auswertung as auswertung
import lotto.kalender_datum as kalender_datum

from .datahandler import Datahandler

try:
    from PyQt5 import QtCore, QtGui, QtWidgets, uic
    print("pyQt5")
except ImportError:
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    from PyQt4 import QtGui as QtWidgets
    from PyQt4 import uic
    print("pyQt4")


class MainDialog(QtWidgets.QMainWindow):
    """
    initial the main window
    """
    def __init__(self, parent=None):
        """
        initial the main window
        1 to 49 button,
        7 spinbox,
        calender,
        datafield
        """
        super(MainDialog, self).__init__(parent)
        self.ui = uic.loadUi(join("lotto", "gui", "lotto_dateneing.ui"))
        self.ui.setWindowIcon(QtGui.QIcon(
            join("misc", "pyLottoverwaltung.svg")))

        # array of Button from 1 to 49
        highest_number = 49
        range_highest_number = range(highest_number)
        self.range_6 = range(6)
        range_7 = range(7)
        self.ui.Btn_Numerals_1to49 = [QtWidgets.QPushButton(
            self.ui.gridLayoutWidget)
            for n in range_highest_number]
        for button_number, button in enumerate(self.ui.Btn_Numerals_1to49):
            button.setMaximumSize(QtCore.QSize(58, 58))
            self.ui.gridLayout.addWidget(
                button, int(button_number / 7), int(button_number % 7), 1, 1)
            button.setAutoFillBackground(True)
            button.setText(str(button_number + 1))

        # set 6 SpinBox and 1
        self.ui.spinBox_Zahlen = [QtWidgets.QSpinBox(
            self.ui.horizontalLayoutWidget) for n in self.range_6]
        self.ui.Btn_delete_Number = [QtWidgets.QPushButton(
            self.ui.horizontalLayoutWidget_2) for n in self.range_6]
        for zahlen in range_7:
            if zahlen != 6:
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
                # set extra Spinbox
                self.ui.spinBox_Zahlen.append(QtWidgets.QSpinBox(
                    self.ui.Lottozahlen))
                self.ui.spinBox_Zahlen[zahlen].setGeometry(QtCore.QRect(
                    130, 360, 51, 23))
                self.ui.Btn_delete_Number.append(QtWidgets.QPushButton(
                    self.ui.Lottozahlen))
                self.ui.Btn_delete_Number[zahlen].setGeometry(
                    QtCore.QRect(190, 360, 41, 20))
            self.ui.spinBox_Zahlen[zahlen].setMaximum(49)
            self.ui.spinBox_Zahlen[zahlen].clear()
            self.ui.Btn_delete_Number[zahlen].setText("X")

        self.onmodus()
        self.buttonchange()
        self.data_handler = Datahandler('datenbank1.sqlite')
        self.onbtn_gz_laden()
        self.onbtn_ls_laden()

        # slots for database functions
        self.ui.Btn_gz_anzeigen.clicked.connect(self.onbtn_gz_anzeigen)
        self.ui.Btn_ls_anzeigen.clicked.connect(self.onbtn_ls_anzeigen)
        self.ui.Btn_gz_loeschen.clicked.connect(self.onbtn_gz_loeschen)
        self.ui.Btn_gz_loeschen.setEnabled(False)
        self.ui.Btn_ls_loeschen.clicked.connect(self.onbtn_ls_loeschen)
        self.ui.Btn_ls_loeschen.setEnabled(False)
        self.ui.btn_ls_auswerten.clicked.connect(self.onbtn_ls_auswerten)
        self.ui.btn_ls_auswerten.setEnabled(False)
        self.ui.CBox_gz_kompl_ausgeben.clicked.connect(
            self.on_checkbox_draw_numbers_show)
        self.ui.btn_set_calender_today.clicked.connect(
            self.onbtn_set_calender_today)
        self.ui.btn_kalender.clicked.connect(self.onbtn_kalender)

        # fields fill with random numbers and give them to database
        self.ui.btn_zufall.clicked.connect(self.onbtn_zufall)
        self.ui.btn_hinzu.clicked.connect(self.onbtn_hinzu)
        # fields of draw numbers
        for number in range_7:
            self.spinBox_clear = functools.partial(
                self.spinbox_1to7_clear, number)
            self.ui.Btn_delete_Number[number].clicked.connect(
                self.spinBox_clear)
            self.focusSpinBox = functools.partial(
                self.focus_spinbox_1to7)
            self.ui.spinBox_Zahlen[number].valueChanged.connect(
                self.focusSpinBox)

        self.ui.com_modus.currentIndexChanged.connect(self.onmodus)

        # fields of 1 to highest number
        for button in range_highest_number:
            self.onEingabefeld = functools.partial(
                self.onclick_number_box_1to49, button + 1)
            self.ui.Btn_Numerals_1to49[button].clicked.connect(
                self.onEingabefeld)

        self.statusBar().showMessage(self.tr('ready'))

        self.ui.actionBeenden.triggered.connect(self.onclose)
        self.ui.actionInfo.triggered.connect(self.on_info)
        self.ui.actionGo_to_the_website.triggered.connect(self.onwebsite)
        self.ui.edi_daten_gewinnz.cursorPositionChanged.connect(
            self.ondaten_gewinnz)
        self.ui.edi_daten_lottoschein.cursorPositionChanged.connect(
            self.ondaten_lottoschein)
        self.onbtn_set_calender_today()

        self.ui.show()

    def init(self):
        """initial variable"""
        self.zahl = 0

    def onbtn_kalender(self):
        """open calender dialog"""
        dlg = kalender_datum.CalendarUi(
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

    def on_info(self):
        """ Program info
        """
        text = self.tr('Eingabe der Gewinnzahlen von einer Ziehung'
                       'oder des Lottoscheins\n Lizenz: GNU GPLv3\n'
                       'http://www.gnu.org/licenses/')
        a = QtWidgets.QMessageBox()
        a.setWindowTitle(self.tr('Info'))
        a.setText(text)
        a.setInformativeText(self.tr('Von Markus Hackspacher'))
        a.exec_()

    def spinbox_1to7_clear(self, number=None, numbers=None):
        """Die SpinBoxen 1 bis 6 und Zusatzzahl löschen"""
        if number is not None:
            self.ui.spinBox_Zahlen[number].setValue(0)
            self.ui.spinBox_Zahlen[number].clear()
        elif numbers is not None:
            for spinBox_number in self.ui.spinBox_Zahlen:
                if spinBox_number.value() == numbers:
                    spinBox_number.setValue(0)
                    spinBox_number.clear()

    def onclick_number_box_1to49(self, zahl):
        """Ein Zahlenfelder 1 bis 49 wurde angeklickt"""
        self.zahl = zahl
        self.geaendert_btn()

    def focus_spinbox_1to7(self):
        """Ein Auswahlfelder der 7 Gewinnzahlen oder
        Lottoscheins hat sich geaendert"""
        """
        for spinBox_Zahlen in self.ui.spinBox_Zahlen:
            if (self.ui.spinBox_Zahlen[number].value() ==
             spinBox_Zahlen.value() and not
             self.ui.spinBox_Zahlen[number] == spinBox_Zahlen
             and not self.ui.spinBox_Zahlen[number].value() == 0):
                 self.ui.spinBox_Zahlen[number].setValue(
                  spinBox_Zahlen.value() + 1)
        """
        self.buttonchange()

    def onbtn_hinzu(self):
        """drawing numbers move in database """
        day = '{0:4}-{1:02}-{2:02}'.format(
            self.ui.spinBox_jahr.value(),
            self.ui.spinBox_monat.value(),
            self.ui.spinbox_tag.value())
        if self.ui.com_modus.currentIndex() == 0:
            self.data_handler.insert_ziehung(
                day, self.draw_numbers(),
                self.ui.spinBox_superz.value(),
                self.ui.spinBox_spiel77.value(),
                self.ui.spinBox_super6.value())
            self.ui.Btn_gz_loeschen.setEnabled(False)
            self.onbtn_gz_laden()
        else:
            self.data_handler.insert_schein(
                day, self.draw_numbers()[:-1],
                self.ui.com_laufzeit.currentIndex(),
                self.ui.com_laufzeit_tag.currentIndex(),
                self.ui.spinBox_spiel77.value())
            self.ui.Btn_ls_loeschen.setEnabled(False)
            self.onbtn_ls_laden()

    def onbtn_ls_auswerten(self):
        """den Lottoschein auswerten"""
        dlg = auswertung.UiLottoEvaluation(self.data_handler.get_schein()[
            self.ui.edi_daten_lottoschein.textCursor().blockNumber()][0],
            self.data_handler)
        dlg.exec_()

    def onbtn_gz_anzeigen(self):
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
        i = 0
        for num in lottodaten[block][5].split(','):
            self.ui.spinBox_Zahlen[i].setValue(int(num))
            i += 1
        self.ui.spinBox_superz.setValue(lottodaten[block][2])
        self.ui.spinBox_spiel77.setValue(lottodaten[block][3])
        self.ui.spinBox_super6.setValue(lottodaten[block][4])
        self.ui.com_modus.setCurrentIndex(0)
        self.buttonchange()

    def onbtn_ls_anzeigen(self):
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
        i = 0
        for num in lottodaten[block][5].split(','):
            self.ui.spinBox_Zahlen[i].setValue(int(num))
            i += 1
        self.ui.com_laufzeit.setCurrentIndex(lottodaten[block][2])
        self.ui.com_laufzeit_tag.setCurrentIndex(lottodaten[block][3])
        self.ui.spinBox_spiel77.setValue(lottodaten[block][4])
        self.ui.com_modus.setCurrentIndex(1)
        self.buttonchange()

    def onbtn_gz_loeschen(self):
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
            anzahl_datensaetze -= 10
        else:
            anzahl_datensaetze = 0
        self.data_handler.delete_ziehung(
            lottodaten
            [self.ui.edi_daten_gewinnz.textCursor().blockNumber() +
                anzahl_datensaetze][0])
        self.onbtn_gz_laden()

    def onbtn_ls_loeschen(self):
        """
        delete tip numbers from the database
        Lottoschein aus der Datenbank loeschen
        """
        lottodaten = self.data_handler.get_schein()
        if lottodaten == []:
            return
        self.data_handler.delete_schein(
            lottodaten
            [self.ui.edi_daten_lottoschein.textCursor().blockNumber()][0])
        self.onbtn_ls_laden()

    def onbtn_ls_laden(self):
        """Read the Lottoschein from the Database
        loading into the QPlainTextEdit
        """
        plain_text = QtWidgets.QPlainTextEdit()
        lottodaten = self.data_handler.get_schein()
        for schein in lottodaten:
            plain_text.appendPlainText('Datum: {0} Zahlen: {1}'
                                       .format(schein[1], schein[5]))
        self.ui.edi_daten_lottoschein.setPlainText(
            plain_text.document().toPlainText())
        self.ui.edi_daten_lottoschein.moveCursor(
            self.ui.edi_daten_lottoschein.textCursor().End)

    def onbtn_gz_laden(self):
        """Read the Gewinnzahlen from the Database
        loading into the QPlainTextEdit
        """
        plain_text = QtWidgets.QPlainTextEdit()
        lottodaten = self.data_handler.get_ziehung()
        if not self.ui.CBox_gz_kompl_ausgeben.isChecked():
            lottodaten = lottodaten[-10:]
        for i in lottodaten:
            plain_text.appendPlainText('Datum: {0} Zahlen: {1}'
                                       .format(i[1], i[5]))
        self.ui.edi_daten_gewinnz.setPlainText(
            plain_text.document().toPlainText())
        self.ui.edi_daten_gewinnz.moveCursor(
            self.ui.edi_daten_gewinnz.textCursor().End)

    def on_checkbox_draw_numbers_show(self):
        """
        CheckBox: Show the complete database in TextEdit
        """
        self.onbtn_gz_laden()

    def onbtn_zufall(self):
        """random numbers

        @return:
        """
        drawn_numbers = 6
        highest = 49
        zufallszahl = random.sample(range(1, highest + 1), drawn_numbers)
        for zahlen in self.range_6:
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
            self.spinbox_1to7_clear(6)
            self.buttonchange()

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
            self.buttonchange()

    def buttonchange(self):
        """Button colour in dependence of the valve of the Spinbox
        """
        a = self.draw_numbers()
        for button in self.ui.Btn_Numerals_1to49:
            if int(button.text()) in a:
                button.setFlat(False)
                button.setStyleSheet("color: red;")
                if int(button.text()) == self.ui.spinBox_Zahlen[6].value():
                    button.setStyleSheet("color: blue;")
            else:
                button.setFlat(True)
                button.setStyleSheet("color: black;")

    def geaendert_btn(self):
        """Show the SpinBoxes of the numbers 1 to 49
        if the number is deactivated, also the
        deleted value of the corresponding spin box
        """
        a = self.draw_numbers()

        for number in self.ui.spinBox_Zahlen:
            if number.value() == 0 and not (self.zahl in a):
                number.setValue(self.zahl)
                break
            elif self.zahl == number.value():
                self.spinbox_1to7_clear(numbers=number.value())
                self.zahl = 0

        a = self.draw_numbers()

        if self.ui.spinBox_Zahlen[6].value() == 0 \
                and self.ui.com_modus.currentIndex() == 0 \
                and not (self.zahl in a):
            self.ui.spinBox_Zahlen[6].setValue(self.zahl)
        elif self.zahl == self.ui.spinBox_Zahlen[6].value() \
                or self.ui.com_modus.currentIndex() == 1:
            self.spinbox_1to7_clear(6)
        self.buttonchange()

    def draw_numbers(self):
        """numbers are in the draw
        """
        return [num_draw.value() for num_draw in self.ui.spinBox_Zahlen]

    @staticmethod
    def onwebsite():
        """open website
        """
        webbrowser.open_new_tab(
            "http://ratgeber---forum.de/wbb3/"
            "index.php?page=Thread&threadID=4855")

    def onclose(self):
        """menu button close

        @return:
        """
        self.ui.close()


def gui(arguments):
    """open the GUI

    @param arguments: language (en, de)
    @type arguments: string
    @return: none
    """
    if len(arguments) > 1:
        locale = arguments[1]
    else:
        locale = str(QtCore.QLocale.system().name())
        print("locale: {}".format(locale))
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    translator.load(join("lotto", "pylv_" + locale))
    app.installTranslator(translator)
    dialog = MainDialog()
    sys.exit(app.exec_())


if __name__ == "__main__":
    gui()
