'''
Created on 27 aug. 2013

@author: Teunissen-S
'''

import time
import logging
import threading
from Queue import Queue
import shutil
import os
import tempfile
from shutil import copyfileobj
# import Queue
lgr = logging.getLogger(__name__)

class Persistence(threading.Thread):
    '''
    This is the class watching the log input queue, emptying it
    and periodically saving it.
    '''
    def __init__(self, filename, group=None, target=None,
                 name=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target,
                                  name=name, verbose=verbose)
        self.filename = filename
        self.full_path = os.path.abspath(self.filename)
        self._logQueue = Queue()
        self.return_queue = Queue()
        # the amount of lines being written to memory
        # until a write to a file is made.
        self.writebuffer = []
        self.maxbuffersize = 10
        self.output = None

    def persist(self, action, data):
        '''
        :param action: what should the persistence do: close, list
        log
        :param data: the actual data in case of logging activity.
        '''
        self._logQueue.put({'action': action, 'data': data})

    def getlog(self):
        self._logQueue.put({'action': 'list', 'data': 0})

    def _returndata(self):
        temp_fl = tempfile.NamedTemporaryFile()
        with open(self.filename, 'r') as fl:
            copyfileobj(fl, temp_fl)
#             for l in fl:
#                 temp_fl.write(l)
        temp_fl.seek(0, 0)
        self.return_queue.put(temp_fl)
        # with open(self.filename,'r') as fl:

    def run(self):
        while True:
            line = self._logQueue.get()
            lgr.debug("persistence queue: {}".format(line))
            try:
                if line['action'] == "close":
                    break
                elif line['action'] == "list":
                    self._returndata()

                else:
                    self.save(line['data'])

            except Exception, err:
                logging.error(err)
            finally:
                self._logQueue.task_done()

    def openfile(self):
        self.output = open(self.filename, 'a')

    def save(self, i):
        # one write less
        self.writes -= 1

        # add the output to the buffer
        self.writebuffer.append('test {}\n'.format(i))

        if len(self.writebuffer) > self.maxbuffersize:
            with open(self.filename, 'a') as fl:
                logging.debug('writing to file.')
                fl.writelines(self.writebuffer)
                self.writebuffer = []


if __name__ == '__main__':
    persistence = Persistence('test.txt')
    i = 1000
    while i:
        persistence.save(i)
        time.sleep(1)
        i -= 1
