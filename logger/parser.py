'''
Created on 27 aug. 2013

@author: Teunissen-S
'''
from datetime import datetime
import time


class BaseParser():
    '''
    Class which is used to interpret incoming raw data and outputs it as a dict.
    '''
    def __init__(self):
        self.parsed = {}
        self.raw = None

    def parse(self, raw):
        self.parsed['tick'] = time.time()
        self.time = time.asctime(time.localtime(self.parsed['tick']))
        self.raw = raw.strip()
