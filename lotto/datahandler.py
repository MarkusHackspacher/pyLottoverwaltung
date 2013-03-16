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

class Datahandler(object):
    def __init__(self, path):
        """class init"""
        self.connection = sqlite3.connect(path)
        #self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Tabellen erstellen mit id"""
        c = self.connection.cursor()
        c.execute("""create table if not exists lottery_drawing (
                  id INTEGER PRIMARY KEY ASC, 
                  d DATE, 
                  zahl_super INTEGER, zahl_spiel77 INTEGER, zahl_spielsuper6 INTEGER)""")
        c.execute("""create table if not exists lottery_drawing_numbers (
                  id INTEGER PRIMARY KEY, 
                  number INTEGER, 
                  position INTEGER,
                  FOREIGN KEY(id) REFERENCES lottery_drawing(id))""")
                  
        c.execute("""create table if not exists lottery_tickets (
                  id INTEGER PRIMARY KEY ASC, 
                  d DATE, 
                  laufzeit INTEGER, laufzeit_tag INTEGER, scheinnr INTEGER)""")        
        c.execute("""create table if not exists lottery_tickets_numbers (
                  id INTEGER PRIMARY KEY, 
                  nummer INTEGER, 
                  position INTEGER,
                  FOREIGN KEY(id) REFERENCES lottery_tickets(id))""")
        self.connection.commit()
        c.close()	

    def insert_ziehung(self, date, zahlen, zahl_super, zahl_spiel77, zahl_spielsuper6):
        """Save the number of the draw in database
        Lottozahlen in der Datenbank speichern
        @type date: date
        @type zahlen: list
        @type zahl_zusatz, zahl_super, zahl_spiel77, zahl_spielsuper6: int
        """
        c = self.connection.cursor()
        c.execute("insert into lottery_drawing(d, zahl_super , zahl_spiel77, zahl_spielsuper6) "
                  "values (?, ?, ?, ?)", 
                 (date,zahl_super, zahl_spiel77, zahl_spielsuper6))
        self.connection.commit()
        c.execute("SELECT last_insert_rowid()")
        self.connection.commit()
        last_insert_rowid = c.fetchone()
        print last_insert_rowid[0]
        position = 0
        for z in zahlen:
            position = position + 1         
            c.execute("insert into lottery_drawing_numbers (number , position) values (?, ?)", 
             (z, position))
        c.close()

    def insert_schein(self, date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
     laufzeit, laufzeit_tag, scheinnr):
        """Save the number of the tip in database
        Daten des Lottoscheines in der Datenbank speichern
        @type date: date
        zahl_1, zahl_2 ,zahl_3 ,zahl_4 ,zahl_5, zahl_6: int
        laufzeit, laufzeit_tag, scheinnr: int
        """
        c = self.connection.cursor()
        try:
            c.execute("insert into lottery_tickets(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             laufzeit, laufzeit_tag, scheinnr) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit, laufzeit_tag, scheinnr))
        except:
            self.add_columns()
            c.execute("insert into lottery_tickets(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             laufzeit, laufzeit_tag, scheinnr) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
             (date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit, laufzeit_tag, scheinnr))
        self.connection.commit()
        c.close()

    def update_ziehung(self, row_id, date, zahl_1, zahl_2,zahl_3, zahl_4, zahl_5, zahl_6, \
     zahl_zusatz, zahl_super, zahl_spiel77, zahl_spielsuper6):
        """Update the number of the draw 
        Lottozahlen in der Datenbank aktualisieren
        @type row_id: int
        @type date: date
        zahl_1, zahl_2 ,zahl_3 ,zahl_4 ,zahl_5, zahl_6: int
        zahl_zusatz, zahl_super, zahl_spiel77, zahl_spielsuper6: int
        """
        c = self.connection.cursor()
        c.execute("update lottery_drawing set d=?, zahl_1=?, zahl_2=?, zahl_3=?, zahl_4=?, zahl_5=?, zahl_6=?, \
             zahl_zusatz=? ,zahl_super=? , zahl_spiel77=?, zahl_spielsuper6=? \
             where rowid=? ", \
             (date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
              zahl_zusatz, zahl_super, zahl_spiel77, zahl_spielsuper6, row_id))
        self.connection.commit()
        c.close()

    def update_schein(self, row_id, date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6,\
     laufzeit, laufzeit_tag, scheinnr):
        """Update the number of the tip 
        Daten des Lottoscheines in der Datenbank aktualisieren
        @type row_id: int
        @type date: date
        zahl_1, zahl_2 ,zahl_3 ,zahl_4 ,zahl_5, zahl_6: int
        laufzeit, laufzeit_tag, scheinnr: int
        """
        c = self.connection.cursor()
        c.execute("update lottery_tickets set d=?, zahl_1=?, zahl_2=?, zahl_3=?, zahl_4=?, zahl_5=?, zahl_6=?, \
             laufzeit=?, laufzeit_tag=?, scheinnr=? where rowid=? ", \
             (date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
              laufzeit, laufzeit_tag, scheinnr, row_id))
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
            c.execute("select * from lottery_drawing where id=?", (rowid,))
        elif date:
            c.execute("select * from lottery_drawing where d=?", (date,))
        else:
            c.execute("select * from lottery_drawing ORDER BY d")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data

    def get_numbers_from_ziehung(self, rowid_lottoschein):    
        """Get numbers from ziehung
        Finde von Nummer in den Ziehungsdaten
        @type rowid_lottoschein: int
        @return: data all the draw with a number from the tip
        """
        c = self.connection.cursor()
        if rowid_lottoschein:
            c.execute("select * from lottery_drawing where rowid=?", (rowid_lottoschein,))
        self.connection.commit()
        data = c.fetchone()  
        selectdata = "select * from lottery_drawing where "
        for z in range(1, 7):
            selectdata = selectdata + ("zahl_{0} in ({1},{2},{3},{4},{5},{6}) or ".
             format(z, data[1], data[2], data[3], data[4], data[5], data[6]))
        c.execute("{6} "
          "zahl_zusatz in ({0},{1},{2},{3},{4},{5}) ORDER BY d". 
         format(data[1], data[2], data[3], data[4], data[5], data[6], selectdata))
        self.connection.commit()
        data = c.fetchall()
        return data
        
    def get_schein(self, rowid=None):    
        """Get data from Lottoscheines
        Daten des Lottoscheines auslesen
        @type rowid: int
        @return: data
        """
        c = self.connection.cursor()
        if rowid:
            c.execute("select * from lottery_tickets where rowid=?", (rowid,))
        else:
            c.execute("select rowid,* from lottery_tickets")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data
        
    def delete_ziehung(self, rowid):
        """Daten der Ziehung der Lottozahlen löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("delete from ziehung where rowid=?", (rowid,))
        self.connection.commit()
        c.close()

    def delete_schein(self, rowid):
        """Daten eines  Lottoscheines löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("delete from lottery_tickets where rowid=?", (rowid,))
        self.connection.commit()
        c.close()

    def dump(self):
        c = self.connection.cursor()
        with open('dump.sql', 'w') as f:
            for line in c.iterdump():
                f.write('%s\n' % line)
        f.close()


    def close(self):
        """close connection of database"""
        self.connection.close()
