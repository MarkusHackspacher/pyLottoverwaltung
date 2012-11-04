#!/usr/bin/env python
from lxml import html
from PyQt4 import QtGui


def data_from_webpage():
    """
    Data from lotto.de
    @return: datum, list of numbers (draw 1-6, Zusatzzahl, Superzahl, Spiel77, Super6)
    """
    QUOTE_URL = 'http://www.lotto.de/de/spielen/landingpage.xhtml'
    document = html.parse(QUOTE_URL)
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
    @return: datum, list of numbers (draw 1-6, Zusatzzahl, Superzahl, Spiel77, Super6)
    """
    QUOTE_URL = 'http://www.lottozahlenonline.de/statistik/lotto-am-samstag/lottozahlen-archiv.php'
    document = html.parse(QUOTE_URL)
    datum = document.xpath('//div[@class="zahlensuche_datum"]/text()')[0].strip()
    value = []
    for x in xrange( 6,12):
        str = '//div[@class="zahlensuche_zahl"]/text()'
        value.append(int(document.xpath(str)[x].strip())) 
    value.append(int(document.xpath('//div[@class="zahlensuche_zz"]/text()')[0].strip()))
    print  datum, value
    return datum, value

def test_data_from_webpage():
 	datum, value = data_from_webpage()
	for x in value:
	    print '{} ...Zahl........ {}'.format(datum, x)

 
if __name__ == '__main__':    #main()
    data_from_achiv()
