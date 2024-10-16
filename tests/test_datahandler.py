# -*- coding: utf-8 -*-

# pyLottoverwaltung

# Copyright (C) <2015-2024> Markus Hackspacher

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

import lotto.datahandler


class TestDataHandler(unittest.TestCase):
    """
    Test Datahandler
    """
    def setUp(self):
        """
        load LottoSystemData
        :return:
        """
        self.data_handler = lotto.datahandler.Datahandler(':memory:')

    def test_insert_get_draw(self):
        """insert and get draw
        """
        self.data_handler.insert_ziehung('2013-03-13',
                                         [11, 12, 13, 14, 15, 16, 17],
                                         666, 777, 888)

        self.assertEqual(self.data_handler.get_ziehung(),
                         [(1, u'2013-03-13', 666, 777, 888,
                           u'11,12,13,14,15,16,17')])

        self.data_handler.insert_ziehung('2013-03-12',
                                         [21, 22, 23, 24, 25, 26, 27],
                                         222, 333, 444)
        self.assertEqual(self.data_handler.get_ziehung(2),
                         [(2, u'2013-03-12', 222, 333, 444,
                           u'21,22,23,24,25,26,27')])

        self.assertEqual(self.data_handler.get_ziehung(),
                         [(2, u'2013-03-12', 222, 333, 444,
                           u'21,22,23,24,25,26,27'),
                          (1, u'2013-03-13', 666, 777, 888,
                           u'11,12,13,14,15,16,17')])
        with self.assertRaises(UnboundLocalError):
            self.data_handler.get_id_numbers_of_ziehung(0)
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(1), [])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(2), [])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(3), [])

        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(2, 3),
                         'error')
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(),
                         'error')
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(
                number_list=[12, 27]), [1, 2])
        self.data_handler.dump()
        self.data_handler.delete_ziehung(1)
        self.data_handler.delete_ziehung(2)
        self.assertEqual(self.data_handler.get_ziehung(), [])

    def test_insert_get_bet(self):
        """insert and get bet
        """
        self.data_handler.insert_schein('2013-03-13',
                                        [11, 12, 13, 14, 15, 16, 17],
                                        2, 0, 888)

        self.assertEqual(self.data_handler.get_schein(),
                         [(1, u'2013-03-13', 2, 0, 888,
                           u'11,12,13,14,15,16,17')])

        self.data_handler.insert_schein('2013-03-12',
                                        [21, 22, 23, 24, 25, 28], 1, 1, 444)
        self.assertEqual(self.data_handler.get_schein(2),
                         [(2, u'2013-03-12', 1, 1, 444,
                           u'21,22,23,24,25,28')])

        self.assertEqual(self.data_handler.get_schein(),
                         [(2, u'2013-03-12', 1, 1, 444,
                           u'21,22,23,24,25,28'),
                          (1, u'2013-03-13', 2, 0, 888,
                           u'11,12,13,14,15,16,17')])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(1), [])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(2), [])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(3), [])

        self.data_handler.delete_schein(1)
        self.data_handler.delete_schein(2)
        self.assertEqual(self.data_handler.get_schein(), [])

    def test_get_id_numbers(self):
        """insert and get bet
        """
        self.data_handler.insert_ziehung('2013-03-12',
                                         [21, 22, 23, 24, 25, 26, 27],
                                         222, 333, 444)
        self.data_handler.insert_ziehung('2013-03-13',
                                         [11, 12, 13, 14, 15, 16, 17],
                                         666, 777, 888)
        self.data_handler.insert_schein('2013-03-13',
                                        [11, 12, 13, 14, 15, 16, 17],
                                        2, 0, 888)
        self.data_handler.insert_schein('2013-03-12',
                                        [21, 22, 23, 24, 25, 28], 1, 1, 444)
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(1), [2])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(2), [1])
        self.assertEqual(self.data_handler.get_id_numbers_of_ziehung(3), [])
