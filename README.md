=================
pyLottoverwaltung
=================

a programm for the german lottery "pick 6 out of 49" system.
A goal is manage the own numbers and the numbers of the drawing.


current:
--------

input of the own numbers and draw numbers with date and save in a database (sqlite).
load a numbers from the database

ToDo:
-----

change and remove data sets. compare the own numbers with the draw numbers.
make the code easier to read.

install:
--------

The program requires [Python 2.7 or 3.x](http://www.python.org/download/) 
and [Qt4 for Python](http://www.riverbankcomputing.com/software/pyqt/download)
or [Qt5 for Python](http://www.riverbankcomputing.com/software/pyqt/download5).

Start with:
```python pylotto.pyw```

The layout (lotto_dateneing.ui) can be manipulated using the Qt4 designer.

Make the documentation as .pdf file:
```epydoc pylotto.pyw lotto --pdf```

To translate the programm or make a translation in your language,
insert in the complete.pro your language code.
```
cd lotto
pylupdate4 complete.pro
```
translate your language file: pylv_xx.ts, and produce the .ts translation files with
```
lrelease complete.pro
```

Installieren:
-------------

Das Programm benötigt [Python  2.7 oder 3.x](http://www.python.org/download/) 
und [Qt4 für Python](http://www.riverbankcomputing.com/software/pyqt/download) 
oder [Qt5 für Python](http://www.riverbankcomputing.com/software/pyqt/download5) dazu.

Start mit: 
```python lotto.pyw```

Das Layout (lotto_dateneing.ui) kann mit den Qt4-Designer bearbeitet werden.

Dokumentation als as .pdf Datei erstellen lassen:
```epydoc pylotto.pyw lotto --pdf```

Copyright (C) <2012-2014> Markus Hackspacher

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

