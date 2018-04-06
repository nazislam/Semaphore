#!/usr/bin/env python3

## NAME: Naz, Sida, Jake
## CLASS: CSC433
## Project # 02

# -- Test transcript files and test decumentation have been attached -- #

import threading
from array import array
import sys
import time
from collections import deque

# file to be read by all the consumer
transactionFile = open( sys.argv[ 1 ] )

# to store the transaction read from the file by the producer
fifo = deque()

# max number of entry allowed in the fifo object
maxFifo = int(sys.argv[4])

# Lock object to enable one thread process at a time
lock = threading.Lock()

# semaphore that will keep track of the empty slots in fifo
empty = threading.Semaphore(value=maxFifo)

# semaphore that will keep track of the full slots in fifo
full = threading.Semaphore(value=0)

# stopper event object for consumer threads
stopper = threading.Event()

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
            # Once one producer reaches end of file, other producers 
            # will fall back
            return
        print('Producer completed')
    return 

# function used by the consumer to get the transaction from the global fifo
# it stops when the transactioId is 9999
def threadConsumer (event_stop):
    while not event_stop.is_set():
        full.acquire()
        lock.acquire()
        t = fifo.popleft()
        print('Consumer:' + t.transactionId + ' internalId:' + str(t.internalId))
        lock.release()
        empty.release()
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

print('Producer and consumer threads done processing!')

