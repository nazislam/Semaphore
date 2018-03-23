#!/usr/bin/env python3

#
#add you names !!!!  
#

import threading

from array import array

import sys

import time

from collections import deque

#to store the transaction read from the file by the producer
fifo = deque()

#file to be read by all the consumer
transactionFile = open( sys.argv[ 1 ] )

#max number of entry allowed in the fifo object
maxFifo = sys.argv[4]

#counter to set the internalId of each transaction
idCounter = 0

#Transaction object to store the transactionid, producerSleep and consumerSleep
#the sleep time is in 1000s of a second
class Transaction:
     def __init__(self, transactionId, producerSleep, consumerSleep):
        self.transactionId = transactionId
        self.producerSleep = producerSleep
        self.consumerSleep = consumerSleep
        self.internalId    = 0;


#function used by the producer to read the file, and to queue the transaction in the global fifo
def threadProducer(filename):
    global idCounter

    with transactionFile:
        for line in transactionFile:
            params = line.split(",")
            t = Transaction( params[0], params[1], params[2] )

            idCounter += 1
            t.internalId = idCounter
            print('Producer:' + t.transactionId + ' internalId:' + str(t.internalId))

            fifo.append( t )
            time.sleep( float( t.producerSleep ) / 1000  )
        print('Producer completed')
    return 

#function used by the consumer to get the transaction from the global fifo
#it stops when the transactioId is 9999
def threadConsumer ():

    while True :
        t = fifo.popleft()
        if int(t.transactionId) == 9999:
           break
        print('Consumer:' + t.transactionId + ' internalId:' + str(t.internalId))
        time.sleep( float( t.consumerSleep ) / 1000  )
    return 

# it receives as input the name of the transactionFile, 
# the number of producer, the number of consumer as parameters
# and the maximum number of transaction which are allowed at once in the fifo
# python3 project2.py transaction.txt 1 1 5
threads =  []

print('Starting producer:' + sys.argv[2])
for num in range(0,int(sys.argv[2])):
    t = threading.Thread(target=threadProducer, args=(sys.argv[1], ))
    t.start()
    threads.append( t )

print('Starting consumer:' + sys.argv[3])
for num in range(0,int(sys.argv[3])):
    t = threading.Thread(target=threadConsumer, args=( ))
    t.start()
    threads.append( t )

for i in range(0, len(threads)-1 ):
   threads[i].join()

