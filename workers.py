'''
Created on 26 Feb 2015

@author: Piers
'''
from multiprocessing import Manager, Process
import os
from time import sleep

class DummyWorker(object):
    def __init__(self):
        print 'Initialising...'
    def process(self, thing):
        print '[%s] processing %s...' % (os.getpid(),thing)
        
def worker_function(work_queue,worker_class):
    print 'worker function...'
    print 'process id:', os.getpid()
    worker = worker_class()
    while True:
        thing = work_queue.get()
        worker.process(thing)
        
class WorkerPool(object):
    def __init__(self,poolsize,worker_class):
        self.mgr = Manager()
        self.work_queue = self.mgr.Queue()
        self.process = []
        for _ in range(poolsize):
            self.process.append(Process(target=worker_function, args=(self.work_queue,worker_class)))
            self.process[-1].start()
            
    def terminate(self):
        while not self.work_queue.empty():
            sleep(0.1)
        for p in self.process:
            p.terminate()
        
def main():
    pool = WorkerPool(2,DummyWorker)
    for i in range(10):
        pool.work_queue.put(i)
    pool.terminate()
    print 'finished'
    
if __name__ == '__main__':
    main()
    