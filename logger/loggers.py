'''
Created on 4 nov. 2013

@author: Teunissen-S
'''

from threading import Thread


class BaseLogger(Thread):
    def __init__(self, incoming_port, output, parser):
        Thread.__init__(self, group=None, target=None,
                                  name=None, verbose=None)
        # the port which is receiving data.
        self.port = incoming_port
        self.persistence = output
        self.parser = parser

    def run(self):
        self.port.connect()


class IntervalBasedLogger(BaseLogger):
    def __init__(self, incoming_port, output, parser, cron_interval):
        BaseLogger.__init__(self, incoming_port, output, parser)
        self.cron_seconds = cron_interval

    def run(self):
        BaseLogger.run(self)
        raise NotImplemented


class EventBasedLogger(BaseLogger):
    def __init__(self, incoming_port, output, parser):
        BaseLogger.__init__(self, incoming_port, output, parser)
        self.do_run = 1
        self.port.timeout = 5

    def run(self):
        BaseLogger.run(self)
        while self.do_run:
            incoming = self.port.readline()
            parsed = self.parser.parse(incoming)
            self.persistence.persist('log', parsed)
