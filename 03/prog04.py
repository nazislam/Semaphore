#!/usr/bin/env python3

# so far improved than others

import threading
import time

global_array = [111, 222, 333, 444, 555, 666, 777, 888, 999]
producer_array = [] # main buffer
consumer_array = []

lock = threading.Lock()
full = threading.Semaphore(value=0)
empty = threading.Semaphore(value=3)

f = 0
e = 3

class myProducerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global f, e
        while global_array:
            print('{0} started!'.format(self.name))
            item = global_array.pop()
            empty.acquire()
            e -= 1
            print('empty sema acquired by {0} -> e:{1}'.format(self.name, e))
            lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            producer_array.append(item)
            print('processed item {0} by {1}'.format(item, self.name))
            print('producer_array: ', producer_array)
            print('global_array: ', global_array)
            lock.release()
            print('lock released by {0}'.format(self.name))
            time.sleep(1)
            full.release()
            f += 1
            print('full sema released by {0} -> f:{1}'.format(self.name, f))

class myConsumerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global f, e
        while producer_array:
            print('{0} started!'.format(self.name))
            full.acquire()
            f -= 1
            print('full sema acquired by {0} -> f:{1}'.format(self.name, f))
            lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            i2 = producer_array.pop()
            consumer_array.append(i2)
            print('processed item {0} by {1}'.format(i2, self.name))
            print('consumer_array: ', consumer_array)
            lock.release()
            print('lock released by {0}'.format(self.name))
            time.sleep(2)
            empty.release()
            e += 1
            print('empty sema released by {0} -> e:{1}'.format(self.name, e))


alex = myProducerThread()
mark = myConsumerThread()

alex.start()
mark.start()
alex.join()
mark.join()

print('All Done!')
