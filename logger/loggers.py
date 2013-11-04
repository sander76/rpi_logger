'''
Created on 4 nov. 2013

@author: Teunissen-S
'''
class BaseLogger():
    def __init__(self, incoming_port, output):
        # the port which is receiving data.
        self.port = incoming_port
        self.persistence = output


class IntervalBasedLogger(BaseLogger):
    def __init__(self, incoming_port, output, cron_interval):
        BaseLogger.__init__(self, incoming_port, output)
        self.cron_seconds = cron_interval
