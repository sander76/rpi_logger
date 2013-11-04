'''
Created on 27 aug. 2013

@author: Teunissen-S
'''
import serial
from time import gmtime, strftime, time, sleep
import logging
lgr = logging.getLogger(__name__)


class SerialPort(serial.Serial):
    def __init__(self, port, timeout=5):
        serial.Serial.__init__(self)
        self.baudrate = 9600
        self.timeout = timeout
        self.port = port
        self.retries = 10

    def connect(self):
        while self.retries:
            try:
                lgr.info('retry {} of 10'.format(self.retries))
                self.open()
                break
            except:
                lgr.error('cannot open serial port. '
                          'waiting for 10 seconds to try again.')
                sleep(10)
                self.retries += -1
        if self.isOpen():
            pass
        else:
            lgr.error('Unable to open serial port.')
