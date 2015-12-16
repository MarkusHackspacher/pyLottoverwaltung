# -*- coding: utf-8 -*-

# pyLottoverwaltung

# Copyright (C) <2015> Markus Hackspacher

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

import unittest
import pep8


class TestCodeFormat(unittest.TestCase):
    """
    Test Code Format
    """

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['pylotto.pyw',
                                        'test/test_pep8.py',
                                        'test/test_datahandler.py',
                                        'lotto/auswertung.py',
                                        'lotto/datahandler.py',
                                        'lotto/kalender_datum.py',
                                        'lotto/lotto_gui_dateneing.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
