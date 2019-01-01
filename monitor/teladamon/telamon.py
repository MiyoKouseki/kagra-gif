import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re
from astropy.time import Time

page = 'https://www-sk.icrr.u-tokyo.ac.jp/~telada/chibutsu.html'
chnum = 14

class TelaMonError(Exception):
    pass


def _get_value(text,num):
    pattern = r'Ch{num}.*:\s+(.*[0-9]+.[0-9]+).*(V)<br>'.format(num=num)
    try:
        return float(re.search(pattern, text).group(1))
    except AttributeError as e:
        return None


def get_values(text):
    return {'ch{0:02d}'.format(num) : _get_value(text,num) for num in range(chnum+1)[1:]} 



def get_datetime(text):
    date = re.search(r'Date.*:\s+([0-9]{4}\/[0-9]{1,2}\/[0-9]{1,2})<br>', text).group(1)
    time = re.search(r'Time.*:\s+([0-9]{2}:[0-9]{2}:[0-9]{2})<br>', text).group(1)
    date = date.replace('/','-')
    dt = Time(date+'T'+time, format='isot') # JST
    return dt
    

class TelaMon():
    def __init__(self):
        text = requests.get(page).text
        self.text = text
        self.datetime = get_datetime(text)
        self.values = get_values(text)
        for k, v in self.values.items():
            setattr(self, k, v)

    def __repr__(self):
        _values = ['{0} : {1}'.format(k,v) for k,v in \
                       sorted(self.values.items(),key=lambda x: x[0])]
        return """DateTime[JST] : {datetime} \n - {values}""".format( \
               datetime=self.datetime,values='\n - '.join(_values))


if __name__=='__main__':
    mon = TelaMon()
    print mon
