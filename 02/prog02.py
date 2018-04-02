import threading

# myList = [1, 2, 3, 4]

class myThreadClass(threading.Thread):
    def __init__(self, listToPrint, lock):
        threading.Thread.__init__(self)
        self.listToPrint = listToPrint
        self.lock = lock

    def run(self):
        self.lock.acquire()
        print('Lock acquired by {0}'.format(self.name))
        while self.listToPrint:
            item = self.listToPrint.pop()
            print('{0} --> {1}'.format(self.name, item))
        self.lock.release()
        print('Lock released by {0}'.format(self.name))
        print('{0} has terminated'.format(self.name))



myList1 = [4, 8, 10, 11]
myList2 = [7, 3, 1, 13]

lock = threading.Lock()
t1 = myThreadClass(myList1, lock)
t2 = myThreadClass(myList2, lock)
t1.start()
t2.start()
t1.join()
t2.join()


