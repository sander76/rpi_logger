'''
Created on 27 aug. 2013

@author: Teunissen-S
'''

import time
import logging
import threading
from logger.parser import Parser
# import Queue


class Persistence(threading.Thread):
    '''
    This is the class watching the log input queue, emptying it
    and periodically saving it.
    '''
    def __init__(self, filename, logQueue, parser, group=None, target=None,
                 name=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target,
                                  name=name, verbose=verbose)
        self.parser = parser
        self.filename = filename
        self.logQueue = logQueue
        # the amount of lines being written to memory
        # until a write to a file is made.
        self.bufferedlines = 10
        self.writes = self.bufferedlines
        self.output = None
        self.openfile()

    def run(self):
        while True:
            line = self.logQueue.get()
            logging.debug("getting a line from the queue")
            try:
                if line == "close":
                    break
                else:
                    self.save(self.parser.parse(line))
                    self.logQueue.task_done()
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
