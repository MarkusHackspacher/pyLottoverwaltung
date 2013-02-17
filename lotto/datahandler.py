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

import sqlite3

class Datahandler(object):
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Tabellen erstellen"""
        c = self.connection.cursor()
        c.execute("create table if not exists ziehung (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, zahl_zusatz INTEGER, \
                zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)")
        c.execute("create table if not exists schein (d date, zahl_1 INTEGER, zahl_2 INTEGER, zahl_3 INTEGER, \
                zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, laufzeit INTEGER, laufzeit_tag INTEGER, scheinnr INTEGER)")        
        self.connection.commit()
        c.close()

    def add_columns(self):
        """Add columns"""		
        lottodaten = self.get_schein()
        if len(lottodaten[0]) == 9:
            print ('Neue Spalten: laufzeit_tag und scheinnr')
            c = self.connection.cursor()
            c.execute("alter table schein add laufzeit_tag INTEGER")        
            c.execute("alter table schein add scheinnr INTEGER")        
            self.connection.commit()
            c.close()
		

    def insert_ziehung(self, day, zahl_1, zahl_2,zahl_3,zahl_4,zahl_5,zahl_6, zahl_zusatz,zahl_super, zahl_spiel77, zahl_spielsuper6):
        """Daten der Ziehung der Lottozahlen in der Datenbank speichern"""
        c = self.connection.cursor()
        c.execute("insert into ziehung(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             zahl_zusatz,zahl_super , zahl_spiel77, zahl_spielsuper6) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, zahl_1, zahl_2,zahl_3,zahl_4,zahl_5,zahl_6, zahl_zusatz,zahl_super, zahl_spiel77, zahl_spielsuper6))
        self.connection.commit()
        c.close()

    def insert_schein(self, day, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit, laufzeit_tag, scheinnr):
        """Daten des Lottoscheines in der Datenbank speichern"""
        c = self.connection.cursor()
        try:
            c.execute("insert into schein(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             laufzeit, laufzeit_tag, scheinnr) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit, laufzeit_tag, scheinnr))
        except:
            self.add_columns()
            c.execute("insert into schein(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             laufzeit, laufzeit_tag, scheinnr) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit, laufzeit_tag, scheinnr))
        self.connection.commit()
        c.close()

    def get_ziehung(self, id=None, date=None):    
        """Daten der Ziehung der Lottozahlen auslesen"""
        c = self.connection.cursor()
        if id:
            c.execute("select * from ziehung where rowid=?", (id,))
        elif date:
            c.execute("select * from ziehung where d=?", (date,))
        else:
            c.execute("select rowid,* from ziehung ORDER BY d")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data
        
    def get_schein(self, id=None):    
        """Daten des Lottoscheines auslesen"""
        c = self.connection.cursor()
        if id:
            c.execute("select * from schein where rowid=?", (id,))
        else:
            c.execute("select rowid,* from schein")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data
        
    def delete_ziehung(self, id):
        """Daten der Ziehung der Lottozahlen löschen"""
        c = self.connection.cursor()
        c.execute("delete from ziehung where rowid=?", (id,))
        self.connection.commit()
        c.close()

    def delete_schein(self, id):
        """Daten eines  Lottoscheines löschen"""
        c = self.connection.cursor()
        c.execute("delete from schein where rowid=?", (id,))
        self.connection.commit()
        c.close()

    def find_rowid(self, typ, blocknumber):
        """ Return the RowID from the BlockNumber of dataset
        @param typ: 0 == Gewinnzahlen, 1 == Lottoschein
        @param blocknumber: BlockNumber of dataset
        @type typ: int
        @type blocknumber: int
        @return: Return the RowID
        """
        if typ == 1:
            return self.get_schein()[blocknumber][0]
        else:
            return self.get_ziehung()[blocknumber][0]

    def close(self):
        self.connection.close()
