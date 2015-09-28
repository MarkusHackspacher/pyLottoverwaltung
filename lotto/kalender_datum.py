#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyLottoverwaltung

# Copyright (C) <2012-2014> Markus Hackspacher

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

from os.path import join
try:
    from PyQt5 import QtGui, QtCore, QtWidgets, uic
except ImportError:
    from PyQt4 import QtGui as QtWidgets
    from PyQt4 import QtGui, QtCore, uic


class ui_kalender(QtWidgets.QDialog):
    def __init__(self, year, month, day):
        """open kalender dialog
        Kalender Dialog oeffnen
        @type year: int
        @type month: int
        @type day: int
        """
        QtWidgets.QDialog.__init__(self)

        uic.loadUi(join("lotto", "gui", "dialog_kalender.ui"), self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.calendarWidget.setSelectedDate(QtCore.QDate(year, month, day))

    def kalender(self):
        """Return the date of the calender
        @return: datum
        """
        return self.calendarWidget.selectedDate()
