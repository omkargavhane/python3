import threading as th
import time
import random
import sys

SIZE=30#Size of shared Resource
items=[]#shared data.
mutex=th.Lock()#semaphore for shared data items.
item=['bread','butter','eggs','juice','cheese','oats','banana','apple','grapes','sprouts']

def producer(number):
    '''Thread producer is for producing item and
    store it in <items>.producer acquires 
    lock over <items> for storing item in it.
    here storing means appending item in <items>
    '''
    global items#shared resource
    global mutex#shared lock
    while True:
        #Random numbe rof items to be produced
        rand_no=random.randint(SIZE-10,SIZE)
        '''if we found that random number exceeeds the size of shared
        resource<items> after producng items equal to random number, 
        then produce number of items equal to
        SIZE-length(items) else produce items equal to random number
        NOTE : Here produce means selecting random item from item list with help
        of random.choice(sequence) method.'''
        if len(items)+rand_no>SIZE:
            rand_no=SIZE-len(items)
            '''if SIZE-len(items) found as 0 means shared resource is at its
            maxsize and print as produce ris waiting for resource to get
            empty'''
            if rand_no==0:
                print('[Producer Thread->{}] Waiting for Consumer...Items_In_SharedResource: [{}]'.format(number,len(items))) 
        else:
            with mutex:
                items.extend([random.choice(item) for i in range(rand_no)])
            print('[Producer Thread->{}] {} new items produced.Items_In_SharedResource: [{}]'.format(number,rand_no,len(items)))
        time.sleep(5)

def consumer(number):
    '''Thread consumer for consuming item
    from <items>.acquires lock over <items>
    before consuming item.here consuming means 
    removing item from <items>
    '''
    global items
    global mutex
    while True:
        '''Consumes Random number of items from shared resource
        <items>. 
        if we found random number greater than no of items present in 
        shared resource<list> then we would simply remove all item 
        present in shared resource<items>
        if there were no items for consumer then it simply prints waiting for 
        producer
        NOTE : Here Consumed means poping 1ts item from shared resource<list>''' 
        rand_no=random.randint(0,SIZE//2)
        if rand_no>len(items):
            rand_no=len(items)
        if len(items)==0:
            print('[Consumer Thread->{}] Waiting for Producer...Items_In_SharedReosurce[{}]'.format(number,len(items)))
        else:
            consumed=[]
            with mutex:
                for i in range(rand_no):
                    consumed.append(items.pop(0))
            print('[Consumer Thread->{}] {} items consumed.Items_In_SharedResource[{}]'.format(number,rand_no,len(items)))
        time.sleep(4)

try:
    SIZE,num_pth,num_cth=tuple(map(int,sys.argv[1:]))
except ValueError:
    print('Command Line Argumnets Required!!!\n python <filename> BUFFER_SIZE NUMBEROF_PRODUCER_THREAD NUMBEROF_CONSUER_THREADS')
    sys.exit(0)
print('*'*10+'PRODUCER-CONSUMER PROBLEM FROM OPERATING SYSTEM********'+'*'*10+'\n'+'='*75)        
for i in range(num_pth):
    obj=th.Thread(target=producer,args=(i,))
    obj.start()
for i in range(num_cth):
    obj=th.Thread(target=consumer,args=(i,))
    obj.start()
