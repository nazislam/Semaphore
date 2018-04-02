import threading
import time

c = [11, 22, 33, 44, 55, 66, 77]
r = []
s = []
mutex = threading.Semaphore()
empty = threading.Semaphore(value=len(c))
full = threading.Semaphore(value=0)

class ThreadProducer(threading.Thread):
    def __init__(self, m, e, f):
        threading.Thread.__init__(self)
        self.m = m
        self.e = e
        self.f = f

    def run(self):
        while c:
            print('{0} started'.format(self.name))
            item = c.pop()
            time.sleep(1)
            self.e.acquire()
            print('semaphore empty decreased by one! by {0}'.format(self.name))
            self.m.acquire()
            print('semaphore mutex decreased by one! by {0}'.format(self.name))
            r.append(item)
            print('r from producer:-', r)
            self.m.release()
            print('semaphore mutex increased by one! by {0}'.format(self.name))
            self.f.release()
            print('semaphore full increased by one! by {0}'.format(self.name))

class ThreadConsumer(threading.Thread):
    def __init__(self, m, e, f):
        threading.Thread.__init__(self)
        self.m = m
        self.e = e
        self.f = f

    def run(self):
        while True:
            print('{0} started'.format(self.name))
            self.f.acquire()
            print('semaphore full decreased by one! by {0}'.format(self.name))
            self.m.acquire()
            print('semaphore mutex decreased by one! by {0}'.format(self.name))
            item = r.pop()
            s.append(item)
            print('s from consumer:-', s)
            time.sleep(2)
            self.m.release()
            print('semaphore mutex increased by one! by {0}'.format(self.name))
            self.e.release()
            print('semaphore empty increased by one! by {0}'.format(self.name))
            s.append(r.pop())


p1 = ThreadProducer(mutex, empty, full)
c1 = ThreadConsumer(mutex, empty, full)

p1.start()
c1.start()
p1.join()
c1.join()
