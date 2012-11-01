#!/usr/bin/env python
from lxml import html

QUOTE_URL = 'http://www.lotto.de/de/spielen/landingpage.xhtml'


def main():
    old_value = None
    document = html.parse(QUOTE_URL)
    str = '//div[@class="form-row"]//option'
    datum = document.xpath(str)[0].get('value')
    
    for x in xrange(1, 9):
        str = '//div[@class="teaser-left-content"]//li[{}]/text()'.format(x)
        value = document.xpath(str)[0].strip()
        print '{} ...Zahl {}........ {}'.format(datum, x, value)
 
    value = document.xpath('//li[@class="field_spiel77"]/text()')[0].strip()
    print '{} ...Spiel77....... {}'.format(datum, value)
    value = document.xpath('//li[@class="field_super6"]/text()')[0].strip()
    print '{} ...Super6........ {}'.format(datum, value)
 
if __name__ == '__main__':
    main()
