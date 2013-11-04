'''
Created on 27 aug. 2013

@author: Teunissen-S
'''

import time
import logging
import threading
from Queue import Queue
# import Queue


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
        self._logQueue = Queue()
        # the amount of lines being written to memory
        # until a write to a file is made.
        self.bufferedlines = 10
        self.writes = self.bufferedlines
        self.output = None
        self.openfile()

    def persist(self, action, data):
        '''
        :param action: what should the persistence do: close, list
        log
        :param data: the actual data in case of logging activity.
        '''
        self._logQueue.put({'action': action, 'data': data})

    def _returndata(self):
        raise NotImplemented

    def run(self):
        while True:
            line = self._logQueue.get()
            logging.debug("getting a line from the queue")
            try:
                if line['action'] == "close":
                    break
                elif line['action'] == "list":
                    self._returndata()
                else:
                    self.save(line['data'])
                    self._logQueue.task_done()
            except Exception, err:
                logging.error(err)

    def openfile(self):
        self.output = open(self.filename, 'a')

    def save(self, i):
        try:
            # one write less
            self.writes -= 1

            # write the output to the file
            self.output.write('test {}\n'.format(i))

            # the amount of writes is zero meaning it is
            # time to write the changes to the file and close it.
            if not self.writes:
                self.writes = self.bufferedlines
                logging.debug('writing to file.')
                self.output.close()
                # and re-open it for further writing.
                self.openfile()
        except:
            self.output.close()


if __name__ == '__main__':
    persistence = Persistence('test.txt')
    i = 1000
    while i:
        persistence.save(i)
        time.sleep(1)
        i -= 1
