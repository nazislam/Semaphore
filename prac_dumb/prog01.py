from threading import Lock, Thread
from time import sleep

lock = Lock()

g = 0

def add_one():
    global g
    #lock.acquire()
    g += 1
    sleep(1)
    #lock.release()

def add_two():
    global g
    #lock.acquire()
    g += 2
    sleep(2)
    #lock.release()

threads = []

for func in [add_one, add_two]:
    threads.append(Thread(target=func))
    threads[-1].start()

for thread in threads:
    thread.join()



print(g)


