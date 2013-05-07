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

from sets import Set
from os.path import join
from PyQt4 import QtGui, QtCore

from gui.auswertung import Ui_Dialog


class ui_lotto_auswertung(QtGui.QDialog, Ui_Dialog):
    def __init__(self, rowid, data_handler):
        """open analyze dialog
        Datenauswerte Dialog oeffnen
        @type rowid: int
        @type data_handler: datahandler
        @return: give close(0) back
        """
        QtGui.QDialog.__init__(self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.setupUi(self)
        self.setWindowTitle("Auswertung")
        self.edi_daten.appendPlainText('Datensatz: {0}'.
        format(rowid))
        schein = data_handler.get_schein(rowid)[0]
        self.edi_daten.appendPlainText('Datum: {0} Zahlen: {1}'
         .format(schein[1], schein[5]))
        self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
        lottodaten = data_handler.get_id_numbers_of_ziehung(rowid)
        anzahl_lottodaten = len(lottodaten)
        if anzahl_lottodaten == 0:
            self.edi_daten.appendPlainText(
             u'Keine übereinstimmende Ziehungen gefunden')
        else:
            self.edi_daten.appendPlainText(u'Folgende Ziehungen gefunden:')
            zahlen = schein[5].split(',')
            z = []
            uebereinstimmungen = [0,0,0,0,0,0,0,0,0,0,0,0]
            for i in zahlen:
                z.append(int(i))
            set_schein = Set(z)
            for lottodaten_z in lottodaten:
                ziehungsdaten = data_handler.get_ziehung(lottodaten_z)[0]
                zahlen = ziehungsdaten[5].split(',')
                z = []
                for i in zahlen:
                    z.append(int(i))
                set_ziehung = Set(z[0:6])
                set_zusatzzahl = Set([z[6]])

                anzahl_gleiche_zahl = len(set_schein & set_ziehung)
                zusatzzahl_vorhanden = len(set_schein & set_zusatzzahl)
                uebereinstimmungen[anzahl_gleiche_zahl * 2 + zusatzzahl_vorhanden] += 1
                if anzahl_gleiche_zahl > 3:
                    self.edi_daten.appendPlainText(u'Datum: {0} | {1}, {2},'
                     u'{3}, {4}, {5}, {6} ZZ: {7} Übereinstimmungen: {8}'
                    .format(ziehungsdaten[1],
                    z[0], z[1], z[2], z[3], z[4], z[5], z[6],
                    anzahl_gleiche_zahl))
            self.edi_daten.appendPlainText(
             u'nur Übereinstimmend mit der Zusatzzahl: {0}'
            .format(uebereinstimmungen[1]))
            self.edi_daten.appendPlainText(
             u'{0} Übereinstimmungen mit einer Zahlen, plus Zusatzzahl: {1}'
             .format(uebereinstimmungen[2], uebereinstimmungen[3]))
            self.edi_daten.appendPlainText(
             u'{0} Übereinstimmungen mit zwei Zahlen, plus Zusatzzahl: {1}'
             .format(uebereinstimmungen[4], uebereinstimmungen[5]))
            self.edi_daten.appendPlainText(
             u'{0} Übereinstimmungen mit drei Zahlen, plus Zusatzzahl: {1}'
             .format(uebereinstimmungen[6], uebereinstimmungen[7]))
            self.edi_daten.appendPlainText(
             u'{0} Übereinstimmungen mit vier Zahlen, plus Zusatzzahl: {1}'
             .format(uebereinstimmungen[8], uebereinstimmungen[9]))
            self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
