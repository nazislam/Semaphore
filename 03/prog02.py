#!/usr/bin/env python3

# the profucer will pick one item and put it an array,
# the cosumer will process the items from the array

import threading
import time

global_array = [111, 222, 333, 444, 555, 666, 777, 888, 999]
producer_array = []
consumer_array = []

lock = threading.Lock()
sema = threading.Semaphore(value=3)

class myProducerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while global_array:
            print('{0} started!'.format(self.name))
            lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            sema.acquire()
            print('semaphore acquired by {0}'.format(self.name))
            item = global_array.pop()
            producer_array.append(item)
            time.sleep(1)
            print('processed item {0} by {1}'.format(item, self.name))
            print('producer_array: ', producer_array)
            print('global_array: ', global_array)
            lock.release()
            print('lock released by {0}'.format(self.name))

class myConsumerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while producer_array:
            print('{0} started!'.format(self.name))
            lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            i2 = producer_array.pop()
            consumer_array.append(i2)
            print('processed item {0} by {1}'.format(i2, self.name))
            print('consumer_array: ', consumer_array)
            lock.release()
            print('lock released by {0}'.format(self.name))
            sema.release()
            print('semaphore released by {0}'.format(self.name))


alex = myProducerThread()
mark = myConsumerThread()

alex.start()
mark.start()
alex.join()
mark.join()
