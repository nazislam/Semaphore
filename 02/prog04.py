import threading
import time


class myThreadClass(threading.Thread):
    
    def __init__(self, sp):
        threading.Thread.__init__(self)
        self.sp = sp

    def run(self):
        self.sp.acquire()
        print('semaphore is acuired by {0}'.format(self.name))
        time.sleep(3)
        self.sp.release()
        print('semaphore is released by {0}'.format(self.name))


def main():
    sema = threading.Semaphore(value=2)

    alex = myThreadClass(sema)
    lisa = myThreadClass(sema)
    bob = myThreadClass(sema)
    naz = myThreadClass(sema)
    mark = myThreadClass(sema)

    alex.start()
    lisa.start()
    bob.start()
    naz.start()
    mark.start()
    alex.join()
    lisa.join()
    bob.join()
    naz.join()
    mark.join()

if __name__ == '__main__':
    main()
