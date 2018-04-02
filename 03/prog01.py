#!/usr/bin/env python3

# the profucer will pick one item and put it an array,
# the cosumer will process the items from the array

import threading
import time

c = [111, 222, 333, 444, 555, 666, 777, 888, 999]
u = []

lock = threading.Lock()
sema = threading.Semaphore(value=3)

class myProducerThread(threading.Thread):

    def __init__(self, l, lock, sm):
        threading.Thread.__init__(self)
        self.l = l
        self.lock = lock
        self.sm = sm

    def run(self):
        while self.l:
            self.sm.acquire()
            self.lock.acquire()
            item = self.l.pop()
            # print('{0} is processing'.format(self.name))
            print('{0} started!'.format(self.name))
            u.append(item)
            time.sleep(1)
            print('processed item {0} by {1}'.format(item, self.name))
            print('c array: ', c)
            self.lock.release()

class myConsumerThread(threading.Thread):
    def __init__(self, lock, sm):
        threading.Thread.__init__(self)
        self.lock = lock
        self.sm = sm

    def run(self):
        while u:
            print('{0} started!'.format(self.name))
            self.lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            i2 = u.pop()
            print('{0} has been processed'.format(i2))
            self.lock.release()
            print('lock released by {0}'.format(self.name))
            self.sm.release()

#a = [1, 2, 3, 4]
#b = [11, 22, 33, 44]

alex = myProducerThread(c, lock, sema)
mark = myConsumerThread(lock, sema)
#lisa = myProducerThread(c, lock)

alex.start()
mark.start()
alex.join()
mark.join()
