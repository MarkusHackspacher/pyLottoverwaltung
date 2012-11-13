#!/usr/bin/env python
# coding: utf-8

from lxml import html
from PyQt4 import QtGui, QtCore
from datahandler import Datahandler

def data_from_webpage():
    """
    Data from lotto.de
    @return: datum, list of numbers (draw 1-6, Zusatzzahl, Superzahl, Spiel77, Super6)
    """
    QUOTE_URL = 'http://www.lotto.de/de/spielen/landingpage.xhtml'
    try: 
        document = html.parse(QUOTE_URL)
    except:
		return    
    str = '//div[@class="form-row"]//option'
    datum = document.xpath(str)[0].get('value')
    value = []
    for x in xrange(1, 9):
        str = '//div[@class="teaser-left-content"]//li[{}]/text()'.format(x)
        value.append(int(document.xpath(str)[0].strip())) 
    value.append(int(document.xpath('//li[@class="field_spiel77"]/text()')[0].strip()))
    value.append(int(document.xpath('//li[@class="field_super6"]/text()')[0].strip()))    
    return datum, value
 

def data_from_achiv():
    """
    Data from www.lottozahlenonline.de
    @return: datum, list of numbers (draw 1-6), Zusatzzahl
    """
    data_handler = Datahandler('datenbank.sqlite')
    QUOTE_URL = 'http://www.lottozahlenonline.de/statistik/lotto-am-samstag/lottozahlen-archiv.php?j=2008'
    #QUOTE_URL = 'http://www.lottozahlenonline.de/statistik/lotto-am-mittwoch/lottozahlen-archiv.php?j=2012'
    document = html.parse(QUOTE_URL)
    datum = document.xpath('//div[@class="zahlensuche_datum"]/text()')
    lottozahlen = document.xpath('//div[@class="zahlensuche_zahl"]/text()')
    zusatzzahlen = document.xpath('//div[@class="zahlensuche_zz"]/text()')
    block=[]
    for x in range(len(lottozahlen)/6):
		block.append(lottozahlen[(x*6):(x*6)+6])
    
    for x in range(len(datum)):
        print datum[x], block[x],zusatzzahlen[x].strip()
        day = QtCore.QDate.fromString(datum[x],"dd.MM.yyyy").toPyDate()
        ziehung_from_date = data_handler.get_ziehung(None, day)
        if ziehung_from_date != []:
            if ziehung_from_date[0][1] != int(block[x][0]):
                print ('Eintrag fehlt in der DB')
                data_handler.insert_ziehung(day,int(block[x][0]),int(block[x][1]),int(block[x][2]),
                 int(block[x][3]),int(block[x][4]),int(block[x][5]),int(zusatzzahlen[x]),0,0,0)
            else:
                print ('Eintrag vorhanden in der DB')
        else:
            data_handler.insert_ziehung(day,int(block[x][0]),int(block[x][1]),int(block[x][2]),
                 int(block[x][3]),int(block[x][4]),int(block[x][5]),int(zusatzzahlen[x]),0,0,0)

    return datum, block, zusatzzahlen

def test_data_from_webpage():
 	datum, value = data_from_webpage()
	for x in value:
	    print '{} ...Zahl........ {}'.format(datum, x)

 
if __name__ == '__main__':    #main()
    data_from_achiv()
    #test_data_from_webpage()
