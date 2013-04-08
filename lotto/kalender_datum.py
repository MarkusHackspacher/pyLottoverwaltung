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

from gui.dialog_kalender import Ui_Dialog

class ui_kalender(QtGui.QDialog, Ui_Dialog): 
    def __init__(self, year, month, day):
        """open kalender dialog
        Kalender Dialog oeffnen
        @type year: int
        @type month: int
        @type day: int
        """
        QtGui.QDialog.__init__(self) 
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.setupUi(self)
        self.setWindowTitle("Kalender")
        self.calendarWidget.setSelectedDate(QtCore.QDate(year, month, day))  

    def kalender(self):
        """Return the date of the calender
        @return: datum 
        """
        return self.calendarWidget.selectedDate()
