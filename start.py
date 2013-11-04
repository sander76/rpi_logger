'''
Created on 28 aug. 2013

@author: Teunissen-S
'''
import os
import sys
from logger.luxlogger import LuxLogger
pth = os.path.dirname(__file__)
os.chdir(pth)
import json
import logging


if __name__ == "__main__":
    try:

        logging.basicConfig(filename='error.log', level=logging.ERROR)
        # open the config file.
        with open('config.json') as conf:
            conf = json.load(conf)
        luxLogger = LuxLogger(**conf)
        luxLogger.go()
    except Exception, k:
        logging.error(k)
        go_on = 0
