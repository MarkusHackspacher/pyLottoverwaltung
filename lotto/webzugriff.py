#!/usr/bin/env python
# coding: utf-8

"""
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

try:
    from lxml import html
except ImportError, e:
    print "FAIL!!! import lxml:", e
from PyQt4 import QtGui, QtCore


def data_from_webpage():
    """
    Data from lotto.de
    @return: datum, list of numbers
    (draw 1-6, Zusatzzahl, Superzahl, Spiel77, Super6)
    """
    quote_url = 'http://www.lotto.de/de/spielen/landingpage.xhtml'
    try:
        document = html.parse(quote_url)
    except Exception, e:
        print "Error:", e
        return
    str = '//div[@class="form-row"]//option'
    datum = document.xpath(str)[0].get('value')
    value = []
    for x in xrange(1, 8):
        str = '//div[@class="teaser-left-content"]//li[{0}]/text()'.format(x)
        value.append(int(document.xpath(str)[0].strip()))
    value.append(int(document.xpath(
     '//li[@class="field_spiel77"]/text()')[0].strip()))
    value.append(int(document.xpath(
     '//li[@class="field_super6"]/text()')[0].strip()))
    return datum, value


def data_from_achiv(data_handler, quote_url=None):
    """
    Data from www.lottozahlenonline.de
    """
    if not quote_url:
        quote_url = 'http://www.lottozahlenonline.de/statistik/lotto-am-samstag/lottozahlen-archiv.php?j=2008'
    try:
        document = html.parse(quote_url)
    except Exception, e:
        print "Error:", e
        return
    datum = document.xpath('//div[@class="zahlensuche_datum"]/text()')
    lottozahlen = document.xpath('//div[@class="zahlensuche_zahl"]/text()')
    zusatzzahlen = document.xpath('//div[@class="zahlensuche_zz"]/text()')
    
    block = []
    for x in range(len(lottozahlen) / 6):
        block.append(lottozahlen[(x * 6):(x * 6) + 6])

    ziehung_from_date = data_handler.get_ziehung()
    ziehung_date = [ziehung_date_satz[1] for
     ziehung_date_satz in ziehung_from_date]
    for x in range(len(datum)):
        datensatz = block[x]
        #print datensatz
        day = u'{0}'.format(QtCore.QDate.fromString(datum[x],
         "dd.MM.yyyy").toPyDate())
        if not day in ziehung_date:
            data_handler.insert_ziehung(day, datensatz,
             zusatzzahlen[x].strip(), 0, 0)
    return


def test_data_from_webpage():
    datum, value = data_from_webpage()
    for x in value:
        print '{} ...Zahl........ {}'.format(datum, x)

if __name__ == '__main__':
    """main"""
    print data_from_webpage()
    #test_data_from_webpage()
