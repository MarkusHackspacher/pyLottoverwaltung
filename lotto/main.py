# -*- coding: utf-8 -*-

"""
pyLottoverwaltung

Copyright (C) <2018-2024> Markus Hackspacher

This file is part of Archerank2.

pyLottoverwaltung is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyLottoverwaltung is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with Archerank2.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os
import sys

try:
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtCore import (PYQT_VERSION_STR, QDir, QLocale, Qt,
                              QTranslator)
    from PyQt6.QtWidgets import (QFileDialog, QMessageBox,
                                 )
    LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
    RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea
except ImportError as err:
    from PyQt5 import QtGui, QtWidgets
    from PyQt5.Qt import PYQT_VERSION_STR
    from PyQt5.QtCore import QDir, QLocale, Qt, QTranslator
    from PyQt5.QtWidgets import (QFileDialog, QMessageBox,
                                 )
    LeftDockWidgetArea, RightDockWidgetArea = Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea
    print(f"main.py: ImportError {err=}, {type(err)=}")
except Exception as err:
    print(f"main.py: Unexpected {err=}, {type(err)=}")
    raise

from lotto import VERSION_STR
from lotto.lotto_gui_dateneing import MainDialog


class Main(QtWidgets.QApplication):
    """Open the GUI of the pyLottoverwaltung.
    """

    def __init__(self, arguments):
        """Initial user interface and slots

        :returns: none
        """
        super(Main, self).__init__(sys.argv)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=arguments.log * 10)
        logging.info(f'Python Version: {sys.version_info.major}.{sys.version_info.minor}')
        logging.info(f'PyQt Version: {PYQT_VERSION_STR}')
        logging.info(f'pyLottoverwaltung Version: {VERSION_STR}')
        if arguments.language:
            locale = arguments.language
        else:
            locale = str(QLocale.system().name())
        translator = QTranslator(self)
        if not translator.load(f'pylv_{locale}', directory='lotto'):
            logging.info('no Translation file load, use default')
        logging.info(f'locale: {locale}, QTranslator: {translator.language()}')
        self.installTranslator(translator)
        self.initDataBase(arguments.database)
        self.dialog = MainDialog(self)

    def initDataBase(self, filename=None):
        while not filename:
            filename = self.fileDlg(self.tr('You want load a file or create a new file'))
            print(filename)
        if 'exit' == filename:
            sys.exit(1)
        # Create an engine and create all the tables we need
        logging.info(f'database: {filename}')

    def fileDlg(self, text):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        try:
            msg_box.setWindowIcon(
                QtGui.QIcon(os.path.join(
                    "misc", "pyLottoverwaltung.svg")))
        except FileNotFoundError:
            msg_box.setWindowIcon(
                QtGui.QIcon(os.path.abspath(os.path.join(
                    os.path.dirname(sys.argv[0]), "misc", "pyLottoverwaltung.svg"))))
        msg_box.setText(self.tr("Question"))
        msg_box.setInformativeText(text)
        open_button = msg_box.addButton(self.tr('Open'), QMessageBox.ButtonRole.AcceptRole)
        new_button = msg_box.addButton(self.tr('New'), QMessageBox.ButtonRole.AcceptRole)
        msg_box.addButton(self.tr('Exit'), QMessageBox.ButtonRole.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() == open_button:
            fileName, _ = QFileDialog.getOpenFileName(
                msg_box, self.tr('Open Database File *.sqlite'), "",
                "pyLottoverwaltung Files (*.sqlite)")
            return fileName
        elif msg_box.clickedButton() == new_button:
            filedialog = QFileDialog(msg_box)
            filedialog.setFilter(filedialog.filter() | QDir.Filter.Hidden)
            filedialog.setFileMode(QFileDialog.FileMode.AnyFile)
            filedialog.setDefaultSuffix('sqlite')
            filedialog.setNameFilters(["pyLottoverwaltung Files (*.sqlite)"])
            if filedialog.exec():
                return filedialog.selectedFiles()[0]
            return
        else:
            return "exit"

    def main_loop(self):
        """application start

        :return:
        """
        self.exec()
