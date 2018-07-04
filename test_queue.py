from threading import Thread
from multiprocessing import Process, Queue
from time import sleep
from syslogging.syslogging import *
import sys


def check_queue(msg):
    f = open('default.log', "a+")
    print(msg)
    f.write("{}\n".format(msg))
    f.close()

def send_mail(q):
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("manhnddev11@gmail.com", "Gmail_1112")
    while True:
        message = q.get()
        msg = MIMEText(message)
        if msg.as_string == 'Done':
            break
        print(msg)
        msg['Subject'] = '[SYSLOGGING]'
        msg['From'] = 'nguyendinhmanh11k58@gmail.com'
        msg['To'] = 'nguyendinhmanh11k58@gmail.com'
        msg['From'] = 'nguyendinhmanh11k58@gmail.com'
        server.sendmail('manhnddev11@gmail.com', ['nguyendinhmanh11k58@gmail.com'], msg.as_string())
    server.quit()
        
def main():
    _queue = Queue()
    log_record = LogRecord('data type error', LogLevel.INFO, 'This is an info log messsage')


    p = Process(target=send_mail, args=(_queue,))
    p.start()

    _queue.put("Message 1")    
    _queue.put("Message 2")    
    _queue.put("Done")

    #block until all item in queue are done
    
    #unblock check_queue
    # _queue.put(None)
    print("done main")

main()