#! coding:utf-8

import unittest
from kagraread import (from_nds2_buffer, fetch, read)
from gwpy.timeseries import TimeSeries


class TestKagraRead(unittest.TestCase):
    '''
    '''
    def setUp(self):
        self.start = 1224028818 # UTC 2018-10-20T00:00:00
        self.end = 1224029418 # UTC 2018-10-20T00:10:00
        self.ch = 'K1:PEM-EXV_SEIS_NS_SENSINF_INMON'
        self.source = './K-K1_C-1224029408-32_forTest.gwf'

        
    def test_read_nds2_buffer(self):
        '''Test `kagraread.from_nds2_buffer` constructor
        '''
        expected = TimeSeries
        actual = from_nds2_buffer(self.start,self.end,self.ch)
        self.assertIsInstance(actual,expected)
        
        
    def test_fetch(self):
        '''Test `kagraread.test_fetch` constructor
        '''        
        expected = TimeSeries
        actual = fetch(self.start,self.end,self.ch)
        self.assertIsInstance(actual,expected)
        
        
    def test_read(self):
        '''Test `kagraread.read` constructor
        '''
        expected = TimeSeries
        actual = read(self.source,self.start,self.end,self.ch)
        self.assertIsInstance(actual,expected)

        
if __name__ == '__main__':
    unittest.main()   
