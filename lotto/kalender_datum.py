#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyLottoverwaltung

# Copyright (C) <2012-2024> Markus Hackspacher

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
    from PyQt6 import QtCore, QtGui, QtWidgets, uic
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets, uic


class CalendarUi(QtWidgets.QDialog):
    """
    set Calendar UI
    """
    def __init__(self, year, month, day, parent=None):
        """open Calendar UI

        @type year: int
        @type month: int
        @type day: int
        """
        super(CalendarUi, self).__init__(parent)
        uic.loadUi(join("lotto", "gui", "dialog_kalender.ui"), self)
        self.setWindowIcon(QtGui.QIcon(join("misc", "pyLottoverwaltung.svg")))
        self.calendarWidget.setSelectedDate(QtCore.QDate(year, month, day))

    def kalender(self):
        """Return the date of the calender
        @return: date
        """
        return self.calendarWidget.selectedDate()
