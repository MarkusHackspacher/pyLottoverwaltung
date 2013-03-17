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
        """class init
        @type path: string
        
        >>> data_handler = Datahandler(':memory:')
        >>> data_handler.insert_ziehung('2013-03-13',[11,12,13,14,15,16,17],666,777,888)
        >>> data_handler.get_ziehung()
        [(1, u'2013-03-13', 666, 777, 888, u'11,12,13,14,15,16,17')]
        >>> data_handler.insert_ziehung('2013-03-12',[21,22,23,24,25,26,27],222,333,444)
        >>> data_handler.get_ziehung(2)
        [(2, u'2013-03-12', 222, 333, 444, u'21,22,23,24,25,26,27')]
        >>> data_handler.get_ziehung()
        [(2, u'2013-03-12', 222, 333, 444, u'21,22,23,24,25,26,27'), (1, u'2013-03-13', 666, 777, 888, u'11,12,13,14,15,16,17')]

        >>> data_handler.insert_schein('2013-03-13',[11,12,13,14,15,16,17],2,0,888)
        >>> data_handler.get_schein()
        [(1, u'2013-03-13', 666, 777, 888, u'11,12,13,14,15,16,17')]
        >>> data_handler.insert_schein('2013-03-12',[21,22,23,24,25,26],1,1,444)
        >>> data_handler.get_schein(2)
        [(2, u'2013-03-12', 1,1, 444, u'21,22,23,24,25,26,27')]
        >>> data_handler.get_schein()
        [(2, u'2013-03-12', 1,1, 444, u'21,22,23,24,25,26,27'), (1, u'2013-03-13', 2,0, 888, u'11,12,13,14,15,16,17')]


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
        zahl_1, zahl_2 ,zahl_3 ,zahl_4 ,zahl_5, zahl_6: int
        laufzeit, laufzeit_tag, scheinnr: int
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
        c.execute("update lottery_tickets set d=?, zahl_1=?, zahl_2=?, zahl_3=?, zahl_4=?, zahl_5=?, zahl_6=?, "
             "laufzeit=?, laufzeit_tag=?, scheinnr=? where rowid=? ", 
             (date, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, 
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
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number) 
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      WHERE a.id=?
                      GROUP BY a.id 
                      """, (rowid,))
        elif date:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number)
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      GROUP BY a.id 
                      WHERE a.d=?""", (date,))
        else:
            c.execute("""SELECT a.*, GROUP_CONCAT(b.number)
                      FROM lottery_drawing a
                      INNER JOIN lottery_drawing_numbers b ON a.id = b.id_drawing
                      GROUP BY b.id_drawing
                      ORDER BY a.d """)           
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
        data = c.fetchone()  
        selectdata = "select * from lottery_drawing where "
        for z in range(1, 7):
            selectdata = selectdata + ("zahl_{0} in ({1},{2},{3},{4},{5},{6}) or ".
             format(z, data[1], data[2], data[3], data[4], data[5], data[6]))
        c.execute("{6} "
          "zahl_zusatz in ({0},{1},{2},{3},{4},{5}) ORDER BY d". 
         format(data[1], data[2], data[3], data[4], data[5], data[6], selectdata))
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
        data = c.fetchall()
        c.close()
        return data
        
    def delete_ziehung(self, rowid):
        """Daten der Ziehung der Lottozahlen löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("DELETE from lottery_drawing "
                  "where id=?", (rowid, ))
        c.execute("DELETE from lottery_drawing_numbers "
                  "where id_drawing=?", (rowid, ))
        self.connection.commit()
        c.close()

    def delete_schein(self, rowid):
        """Daten eines  Lottoscheines löschen
        @type rowid: int
        """
        c = self.connection.cursor()
        c.execute("DELETE from lottery_tickets, lottery_tickets_numbers where id=?", (rowid, ))
        c.execute("DELETE from lottery_tickets_numbers where id_ticket=?", (rowid, ))
        self.connection.commit()
        c.close()

    def dump(self):
        with open('dump.sql', 'w') as f:
            for line in self.connection.iterdump():
                f.write('%s\n' % line)
        f.close()


    def close(self):
        """close connection of database"""
        self.connection.close()
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()
