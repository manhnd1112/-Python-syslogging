from queue import Queue
from threading import Thread
from multiprocessing import Process
from time import sleep
from syslogging.syslogging import *
import sys
from time import sleep

f = open('default.log', "a+")

def write_to_file(message):
    f.write(message+"\n")
    f.close()

def send_mail(q):
    try:
        sleep(2)
        #while True:
        message = q.get()
        write_to_file(message)
        return 0        
    except Exception as e:
        raise e
def main():
    try:
        _queue = Queue()
        log_record = LogRecord('data type error', LogLevel.INFO, 'This is an info log messsage')

        p = Process(target=send_mail, args=(_queue,))
        p.start()

        _queue.put("Message 1")    
        _queue.put("Message 2")    
        #block until all item in queue are done
        
        #unblock check_queue
        # _queue.put(None)
        print("done main")
    except Exception as e:
        print(str(e))

main()