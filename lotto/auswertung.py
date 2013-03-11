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
#import datahandler

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
        self.edi_daten.appendPlainText('Datensatz RowID: {0}'.
        format(rowid))
        schein = data_handler.get_schein(rowid)[0]
        self.edi_daten.appendPlainText('Datum: {0} Zahlen: '
        '{1}, {2}, {3}, {4}, {5}, {6}' 
         .format(schein[0], schein[1], schein[2], schein[3], schein[4], schein[5], schein[6]))
        self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
        lottodaten = data_handler.get_numbers_from_ziehung(rowid)      
        set_schein = Set([schein[1],schein[2],schein[3],schein[4],schein[5],schein[6]])
        
        for i in lottodaten:
            set_ziehung = Set([i[2], i[3], i[4], i[5], i[6], i[7], i[8]])
            anzahl_gleiche_zahl =  len(set_schein & set_ziehung)
            self.edi_daten.appendPlainText(u'Datum: {0} | {1}, {2}, '
            u'{3}, {4}, {5}, {6} ZZ: {7} Übereinstimmungen: {8}' 
             .format(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], anzahl_gleiche_zahl))
        self.edi_daten.moveCursor(self.edi_daten.textCursor().End)
 
      
