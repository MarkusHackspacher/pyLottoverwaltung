pyLottoverwaltung
=================

[![Build Status](https://app.travis-ci.com/MarkusHackspacher/pyLottoverwaltung.svg?branch=master)](https://app.travis-ci.com/github/MarkusHackspacher/pyLottoverwaltung)

a program for the german lottery "pick 6 out of 49" system.
A goal is manage the own numbers and the numbers of the drawing.


current:
--------

input of the own numbers and draw numbers with date and save in a database (sqlite).
load a numbers from the database

ToDo:
-----

change and remove data sets. compare the own numbers with the draw numbers.

install:
--------

The program requires [Python 3.x](http://www.python.org/download/) 
and [Qt5 for Python](http://www.riverbankcomputing.com/software/pyqt/download5).

Start with:
```./start.pyw```

The layout (lotto_dateneing.ui) can be manipulated using the Qt designer.

Make the documentation as .pdf file:
```epydoc pylotto.pyw lotto --pdf```

To translate the program or make a translation in your language,
insert in the complete.pro your language code.
```
cd lotto
pylupdate5 complete.pro
```
translate your language file: pylv_xx.ts, and produce the .ts translation files with
```
lrelease complete.pro
```

Installieren:
-------------

Das Programm benötigt [Python 3.x](http://www.python.org/download/) 
und [Qt5 für Python](http://www.riverbankcomputing.com/software/pyqt/download5) dazu.

Start mit: 
```python lotto.pyw```

Das Layout (lotto_dateneing.ui) kann mit den Qt-Designer bearbeitet werden.

Dokumentation als as .pdf Datei erstellen lassen:
```epydoc pylotto.pyw lotto --pdf```


License
-------

GNU GPL V3
