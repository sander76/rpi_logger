'''
Created on 4 nov. 2013

@author: Teunissen-S
'''
from logger.parser import BaseParser


class Em304Parser(BaseParser):
    def __init__(self):
        BaseParser.__init__(self)

    def parse(self, raw_data):
        BaseParser.parse(self, raw_data)
        self.parsed['data'] = self.raw
        return self.parsed
