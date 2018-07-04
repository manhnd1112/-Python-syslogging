import multiprocessing

class MyFancyClass(object):
    
    def __init__(self, name):
        self.name = name
    
def do_something(message):
    print('Log !{}'.format(message))


def worker(q):
    while True:
        obj = q.get()
        do_something(obj)


if __name__ == '__main__':
    queue = multiprocessing.Queue()

    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()
    
    queue.put('message')
    queue.put('message1')
    
    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    p.join()