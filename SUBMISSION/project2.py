#!/usr/bin/env python3

import threading
from array import array
import sys
import time
from collections import deque

# max number of entry allowed in the fifo object
maxFifo = int(sys.argv[4])

lock = threading.Lock()
empty = threading.Semaphore(value=maxFifo)
full = threading.Semaphore(value=0)
stopper = threading.Event()

# to store the transaction read from the file by the producer
fifo = deque()

# file to be read by all the consumer
transactionFile = open( sys.argv[ 1 ] )


# counter to set the internalId of each transaction
idCounter = 0

# Transaction object to store the transactionid, producerSleep and consumerSleep
# the sleep time is in 1000s of a second
class Transaction:
     def __init__(self, transactionId, producerSleep, consumerSleep):
        self.transactionId = transactionId
        self.producerSleep = producerSleep
        self.consumerSleep = consumerSleep
        self.internalId    = 0;


# function used by the producer to read the file, and to queue the transaction in the global fifo
def threadProducer(filename):
    global idCounter

    with transactionFile:
        try:
            for line in transactionFile:
                params = line.split(",")
                t = Transaction( params[0], params[1], params[2] )

                empty.acquire()
                lock.acquire()
                
                idCounter += 1
                t.internalId = idCounter
                print('Producer:' + t.transactionId + ' internalId:' + str(t.internalId))

                fifo.append( t )
                lock.release()
                full.release()
                time.sleep( float( t.producerSleep ) / 1000  )
        except ValueError:
            print('Producer reached end of file')
        # print('Producer completed')
    return 

# function used by the consumer to get the transaction from the global fifo
# it stops when the transactioId is 9999
def threadConsumer (stopper):
    while not stopper.is_set():
        full.acquire()
        # print('full sema acquired!')
        lock.acquire()
        # print('lock acquired!')
        t = fifo.popleft()
        print('Consumer:' + t.transactionId + ' internalId:' + str(t.internalId))
        lock.release()
        # print('lock released!')
        empty.release()
        # print('empty sema released!')
        if (int(t.transactionId) == 9999):
            break
        time.sleep( float( t.consumerSleep ) / 1000  )
    return 

threads =  []

## ------------------------------ ##

print('Starting producer:' + sys.argv[2])
for num in range(0, int(sys.argv[2])):
    t = threading.Thread(target=threadProducer, args=(sys.argv[1], ))
    t.start()
    threads.append( t )

print('Starting consumer:' + sys.argv[3])
for num in range(0, int(sys.argv[3])):
    t = threading.Thread(target=threadConsumer, args=( stopper, ))
    t.start()
    time.sleep(10)  # consumer threads will stop after 10 seconds
    stopper.set()
    threads.append( t )

for i in range(0, len(threads)-1 ):
   threads[i].join()

