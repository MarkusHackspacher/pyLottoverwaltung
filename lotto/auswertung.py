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


try:
    from sets import Set
except ImportError:
    Set = set

import sys
from os.path import join

try:
    from PyQt5 import QtGui, QtWidgets, uic
except ImportError:
    from PyQt4 import QtGui as QtWidgets
    from PyQt4 import QtGui, QtCore, uic

if sys.version_info < (3, 0):
    str = unicode


class UiLottoEvaluation(QtWidgets.QDialog):
    """
    analyze dialog
    """
    def __init__(self, rowid, data_handler, parent=None):
        """open analyze dialog
        Datenauswerte Dialog oeffnen
        @type rowid: int
        @type data_handler: datahandler
        @return: give close(0) back
        """
        super(UiLottoEvaluation, self).__init__(parent)
        uic.loadUi(join("lotto", "gui", "auswertung.ui"), self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        text = self.tr('record: {0}')
        self.edi_daten.appendPlainText(str(text).format(rowid))
        schein = data_handler.get_schein(rowid)[0]
        text = self.tr('Date: {0} Numbers: {1}')
        self.edi_daten.appendPlainText(str(text).format(schein[1], schein[5]))
        self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
        lottodaten = data_handler.get_id_numbers_of_ziehung(rowid)
        anzahl_lottodaten = len(lottodaten)
        if anzahl_lottodaten == 0:
            self.edi_daten.appendPlainText(
                self.tr('No matching draws found'))
        else:
            self.edi_daten.appendPlainText(
                self.tr('The following drawings found:'))
            zahlen = schein[5].split(',')
            z = []
            uebereinstimmungen = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
                anzahl_gleiche_zahl = len(set_schein & set_ziehung)

                if len(z) >= 7:
                    set_zusatzzahl = Set([z[6]])
                    zusatzzahl_vorhanden = len(set_schein & set_zusatzzahl)
                else:
                    zusatzzahl_vorhanden = 0

                uebereinstimmungen[
                    anzahl_gleiche_zahl * 2 + zusatzzahl_vorhanden] += 1
                if anzahl_gleiche_zahl > 3:
                    if len(z) >= 7:
                        text_zz = 'ZZ: {0}'.format(z[6])
                    else:
                        text_zz = ''
                    text = self.tr('Date: {0} | {1}, {2}, {3}, {4}, {5}, {6}'
                                   ' {7} matches: {8}')
                    text = str(text).format(ziehungsdaten[1], z[0], z[1],
                                            z[2], z[3], z[4], z[5], text_zz,
                                            anzahl_gleiche_zahl)
                    self.edi_daten.appendPlainText(text)
            text = self.tr('only match with the additional number: {0}')
            self.edi_daten.appendPlainText(
                    str(text).format(uebereinstimmungen[1]))
            text_zahl = (self.tr('a number'), self.tr('two numbers'),
                         self.tr('three numbers'), self.tr('four numbers'))
            text = self.tr('{} Matches with {}, plus additional number: {}')
            c = 0
            while c < 4:
                self.edi_daten.appendPlainText(str(text).format(
                        uebereinstimmungen[c + 1 * 2],
                        str(text_zahl[c]),
                        uebereinstimmungen[c + 2 * 2]))
                c += 1
            self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
