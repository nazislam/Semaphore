import threading
import time

class myThreadingClass(threading.Thread):
    def __init__(self, aList, output, lock):
        threading.Thread.__init__(self)
        self.aList = aList
        self.output = output
        self.lock = lock

    def run(self):
        while self.aList:
            time.sleep(3)
            item = self.aList.pop()
            self.lock.acquire()
            print('lock acquired by {0}'.format(self.name))
            self.output.write(str(item))
            self.output.write('\n')
            print('{0} processed {1}'.format(self.name, item))
            self.lock.release()
            print('lock relesed by {0}'.format(self.name))

def main():
    myList01 = [1, 2, 3, 4]
    myList02 = [11, 22, 33, 44]

    f = open('output03.txt', 'w')
    lock = threading.Lock()

    alex = myThreadingClass(myList01, f, lock)
    lisa = myThreadingClass(myList02, f, lock)

    alex.start()
    lisa.start()
    alex.join()
    lisa.join()

if __name__ == "__main__":
    main()
