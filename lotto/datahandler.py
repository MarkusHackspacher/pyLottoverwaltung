# coding: utf-8

"""
the data handler
for insert, get and delete data in the database
"""
import sqlite3
import datetime

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
                zahl_4 INTEGER, zahl_5 INTEGER, zahl_6 INTEGER, laufzeit INTEGER)")        
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

    def insert_schein(self, day, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit):
        """Daten des Lottoscheines in der Datenbank speichern"""
        c = self.connection.cursor()
        c.execute("insert into schein(d, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, \
             laufzeit) values (?, ?, ?, ?, ?, ?, ?, ?)", \
             (day, zahl_1, zahl_2, zahl_3, zahl_4, zahl_5, zahl_6, laufzeit))
        self.connection.commit()
        c.close()

    def get_ziehung(self, id=None):    
        """Daten der Ziehung der Lottozahlen auslesen"""
        c = self.connection.cursor()
        if id:
            c.execute("select * from ziehung where id=?", (id,))
        else:
            c.execute("select rowid,* from ziehung")
        self.connection.commit()
        data = c.fetchall()
        c.close()
        return data
        
    def get_schein(self, id=None):    
        """Daten des Lottoscheines auslesen"""
        c = self.connection.cursor()
        if id:
            c.execute("select * from schein where id=?", (id,))
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

    def close(self):
        self.connection.close()