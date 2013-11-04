'''
Created on 27 aug. 2013

@author: Teunissen-S
'''

import logging
from logger.serialport import SerialPort
from apscheduler.scheduler import Scheduler
from logger.persistence import Persistence
from Queue import Queue
import time
from logger.parser import Parser


TIMEOUT = 1


class LuxLogger():
    def __init__(self, cron_seconds, output, serialport):
        self.sched = Scheduler()
        self.sched.start()
        self.log_queue = Queue()
        self.incoming = SerialPort(serialport, self.log_queue,
                                   TIMEOUT)
        self.parser = Parser()
        self.saver = Persistence(output, self.log_queue, self.parser)
        self.saver.start()
        self.cron_seconds = cron_seconds

    def go(self):
        try:
            logging.debug("starting the cron based scheduler")
            self.sched.add_cron_job(self.incoming.getData,
                                    second=self.cron_seconds)
        except Exception, err:
            logging.error(err)

