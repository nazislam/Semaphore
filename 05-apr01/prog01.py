import threading
import time

lock = threading.Lock()
sema = threading.Semaphore(value=3)

fifo = [11, 22, 33, 44, 55, 66, 77]

class myThreadClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while fifo:
            print('{0} has started!'.format(self.name))
            lock.acquire()
            sema.acquire()
            item = fifo.pop()
            print('item {0} has been processed by {1}'.format(item, self.name))
            print('{0} finished'.format(self.name))
            lock.release()
            sema.release()
            print('fifo:', fifo)


alex = myThreadClass()
lisa = myThreadClass()

alex.start()
lisa.start()
alex.join()
lisa.join()

