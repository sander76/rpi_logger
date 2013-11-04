'''
Created on 28 aug. 2013

@author: Teunissen-S
'''
import os
import sys
from logger.persistence import Persistence
from logger.serialport import SerialPort
from arduino.em304parser import Em304Parser
from logger.loggers import EventBasedLogger
pth = os.path.dirname(__file__)
os.chdir(pth)
import json
import logging
lgr = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        #logging.basicConfig(filename='error.log', level=logging.ERROR)
        
        #persistence = Persistence("/media/logger/output.txt")
        persistence = Persistence("output.txt")
        persistence.start()
        # create a serial port logger.
        serialport = SerialPort("COM16", 5)
        em341parser = Em304Parser()
        em341logger = EventBasedLogger(serialport, persistence, em341parser)
        em341logger.start()

    except Exception, k:
        lgr.error(k)
        #go_on = 0
