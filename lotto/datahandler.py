# coding: utf-8

"""
the data handler
for insert, get and delete data in the database

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

import sqlite3, os
import doctest

class Datahandler(object):
    def __init__(self, path):
        """class init
        @type path: string
        
        >>> data_handler = Datahandler(':memory:')
        >>> data_handler.insert_ziehung('2013-03-13', [11, 12, 13, 14, 15, 16, 17],666, 777, 888)
        >>> data_handler.get_ziehung()
        [(1, u'2013-03-13', 666, 777, 888, u'11,12,13,14,15,16,17')]
        >>> data_handler.insert_ziehung('2013-03-12', [21 ,22, 23, 24, 25, 26, 27], 222, 333, 444)
        >>> data_handler.get_ziehung(2)
        [(2, u'2013-03-12', 222, 333, 444, u'21,22,23,24,25,26,27')]
        >>> data_handler.get_ziehung()
        [(2, u'2013-03-12', 222, 333, 444, u'21,22,23,24,25,26,27'), (1, u'2013-03-13', 666, 777, 888, u'11,12,13,14,15,16,17')]

        >>> data_handler.insert_schein('2013-03-13', [11, 12, 13, 14, 15, 16, 17], 2 ,0 ,888)
        >>> data_handler.get_schein()
        [(1, u'2013-03-13', 2, 0, 888, u'11,12,13,14,15,16,17')]
        >>> data_handler.insert_schein('2013-03-12', [21, 22, 23, 24, 25, 28], 1, 1, 444)
        >>> data_handler.get_schein(2)
        [(2, u'2013-03-12', 1, 1, 444, u'21,22,23,24,25,28')]
        >>> data_handler.get_schein()
        [(2, u'2013-03-12', 1, 1, 444, u'21,22,23,24,25,28'), (1, u'2013-03-13', 2, 0, 888, u'11,12,13,14,15,16,17')]
        >>> data_handler.get_id_numbers_of_ziehung(2)
        [2]
        >>> data_handler.get_id_numbers_of_ziehung(2, 3)
        'error'
        >>> data_handler.get_id_numbers_of_ziehung()
        'error'
        >>> data_handler.get_id_numbers_of_ziehung(number_list=[12, 27])
        [1, 2]
        >>> data_handler.dump()
        >>> data_handler.delete_ziehung(1)
        >>> data_handler.delete_ziehung(2)
        >>> data_handler.get_ziehung()
        []
        >>> data_handler.delete_schein(1)
        >>> data_handler.delete_schein(2)
        >>> data_handler.get_schein()
        []
       """
        self.connection = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self):
        """Tabellen erstellen mit id"""
        c = self.connection.cursor()
        c.execute("""create table if not exists lottery_drawing (
                  id INTEGER PRIMARY KEY ASC, 
                  d DATE, 
                  zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)""")
        c.execute("""create table if not exists lottery_drawing_numbers (
                  id_drawing INTEGER, 
                  number INTEGER, 
                  position INTEGER,
                  FOREIGN KEY(id_drawing) REFERENCES lottery_drawing(id))""")                  
        c.execute("""create table if not exists lottery_tickets (
                  id INTEGER PRIMARY KEY ASC, 
                  d DATE, 
                  laufzeit INTEGER, laufzeit_tag INTEGER, scheinnr INTEGER)""")        
        c.execute("""create table if not exists lottery_tickets_numbers (
                  id_ticket INTEGER,
                  number INTEGER, 
                  position INTEGER,
                  FOREIGN KEY(id_ticket) REFERENCES lottery_tickets(id))""")
        self.connection.commit()
        c.close()	

    def insert_ziehung(self, date, zahlen, zahl_super, zahl_spiel77, zahl_spielsuper6):
        """Save the number of the draw in database
        Lottozahlen in der Datenbank speichern
        @type date: date
        @type zahlen: list
        @type zahl_super : int
        @type zahl_spiel77: int
        @type zahl_spielsuper6: int
        """
        c = self.connection.cursor()
        c.execute("insert into lottery_drawing(d, zahl_super , zahl_spiel77, zahl_spielsuper6) "
                  "values (?, ?, ?, ?)", 
                 (date,zahl_super, zahl_spiel77, zahl_spielsuper6))
        self.connection.commit()
        c.execute("SELECT last_insert_rowid()")
        last_insert_rowid = c.fetchone()
        position = 0
        for z in zahlen:
            position = position + 1         
            c.execute("insert into lottery_drawing_numbers (id_drawing, number , position) values (?, ?, ?)", 
             (last_insert_rowid[0], z, position))
        self.connection.commit()
        c.close()

    def insert_schein(self, date, zahlen, laufzeit, laufzeit_tag, scheinnr):
        """Save the number of the tip in database
        Daten des Lottoscheines in der Datenbank speichern
        @type date: date
        @type zahlen: list of int
        @type laufzeit: int
        @type laufzeit_tag: int
        @type scheinnr: int
        """
        c = self.connection.cursor()
        c.execute("insert into lottery_tickets(d, "
                  "laufzeit, laufzeit_tag, scheinnr) values (?, ?, ?, ?)", 
                 (date, laufzeit, laufzeit_tag, scheinnr))
        self.connection.commit()
        c.execute("SELECT last_insert_rowid()")
        last_insert_rowid = c.fetchone()
        position = 0
        for z in zahlen:
            position = position + 1         
            c.execute("insert into lottery_tickets_numbers (id_ticket, number , position) values (?, ?, ?)", 
             (last_insert_rowid[0], z, position))
        self.connection.commit()
        c.close()

    def get_ziehung(self, rowid=None, date=None):    
        """Daten der Ziehung der Lottozahlen auslesen
        @type rowid: int
        @type date: date
        @return: data
        """
        c = self.connection.cursor()
        if rowid:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number) 
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      WHERE a.id=? GROUP BY a.id 
                      """, (rowid,))
        elif date:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number)
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      WHERE a.d=? GROUP BY a.id""", (date,))
        else:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number)
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      GROUP BY b.id_drawing
                      ORDER BY a.d """)           
        data = c.fetchall()
        c.close()
        return data

    def get_id_numbers_of_ziehung(self, id_lottoschein=None, number_list=None):    
        """Get id numbers of ziehung, with the id of lotteryticket
        Finde die ID Nummer der Ziehungsdaten, durch den Lottoschein
        @type id_lottoschein: int
        @type number_list: list of int
        @return: data all the draw with the number of lotteryticket
        """
        if not ((id_lottoschein==None) ^ (number_list==None)):
            return "error"
        c = self.connection.cursor()
        if id_lottoschein:
            c.execute("SELECT * FROM lottery_tickets_numbers where id_ticket=?", (id_lottoschein,))
            data = c.fetchall()                      
            selectdata = ""
            for z in data:
                selectdata = selectdata + (" {0},".format(z[1]))
        if number_list:
            selectdata = "".join(map(" {0},".format, number_list))
        selectdata = ("SELECT * FROM lottery_drawing_numbers where number in ( {0} ) ORDER BY id_drawing".
         format(selectdata.rstrip(',')))
        c.execute (selectdata)
        data = c.fetchall()
        id_numbers = []
        for z in data:
            if z[0] not in id_numbers:
                id_numbers.append(z[0])
        return id_numbers
        
    def get_schein(self, rowid=None):    
        """Get data from Lottoscheines
        Daten des Lottoscheines auslesen
        @type rowid: int
        @return: data
        """
        c = self.connection.cursor()
        if rowid:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number) 
                      FROM lottery_tickets a
                      INNER JOIN lottery_tickets_numbers b ON a.id = b.id_ticket
                      WHERE a.id=?
                      GROUP BY a.id 
                      """, (rowid,))
        else:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number)
                      FROM lottery_tickets a
                      INNER JOIN lottery_tickets_numbers b ON a.id = b.id_ticket
                      GROUP BY b.id_ticket
                      ORDER BY a.d """)           
        data = c.fetchall()
        c.close()
        return data
        
    def delete_ziehung(self, rowid):
        """Daten der Ziehung der Lottozahlen löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("DELETE from lottery_drawing "
                  "WHERE id=?", (rowid, ))
        c.execute("DELETE from lottery_drawing_numbers "
                  "WHERE id_drawing=?", (rowid, ))
        self.connection.commit()
        c.close()

    def delete_schein(self, rowid):
        """Daten eines  Lottoscheines löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("DELETE from lottery_tickets "
                  "WHERE id=?", (rowid, ))
        c.execute("DELETE from lottery_tickets_numbers "
                  "WHERE id_ticket=?", (rowid, ))
        self.connection.commit()
        c.close()

    def dump(self):
        """write dump file"""
        with open('dump.sql', 'w') as f:
            for line in self.connection.iterdump():
                f.write('%s\n' % line)
        f.close()

    def __del__(self):
        """close connection of database"""
        self.connection.close()
        print ('database connection close')
        
if __name__ == "__main__":
    doctest.testmod()
