'''
Created on 27 aug. 2013

@author: Teunissen-S
'''
import serial
from time import gmtime, strftime, time
import logging


class SerialPort():
    def __init__(self, port, logqueue, timeout):
        self.ser = serial.Serial(port, timeout=timeout)
        self.logQueue = logqueue

    def getData(self):
        try:
            self.ser.flushInput()
            proceed = 1
            while proceed:
                output = {
                          'tm': time(),
                          'time': strftime("%a, %d %b %Y %H:%M:%S +0000",
                                           gmtime()),
                          'status': '',
                          'data': ''
                          }
                char = ord(self.ser.read())
                if char == 2:
                    logging.debug("found the starting point\
                     of the serial string")
                    output['status'] = 'ok'
                    output['data'] = self.ser.read(14)
                    logging.debug(output)
                    proceed = 0
            if self.checkoutput(output, ord(self.ser.read())):
                logging.info("putting it in the log output queue")
                self.logQueue.put(output)
            else:
                raise Exception('Parsing not correct')
        except serial.SerialException:
            raise Exception("something wrong with the serial port.")
        except:
            output['status'] = 'error'
            output['data'] = 'reading serial data'
            self.logQueue.put(output)

    def checkoutput(self, output, enchar):
        if enchar == 13:
            return 1
        else:
            return 0
