import threading
import Queue
import time

wait_queue = Queue.Queue()
task_queue = Queue.Queue()


def do_stuff():
    print("%s doing stuff" % str(threading.current_thread()))
    time.sleep(5)


def queue_thread(sleep_time):
    # advertise current thread waiting
    time.sleep(sleep_time)
    wait_queue.put("waiting")

    # wait for permission to pass
    message = task_queue.get()

    print("%s got task: %s" % (threading.current_thread(), message))
    # unregister current thread waiting
    wait_queue.get()

    if message == "proceed":
        do_stuff()
        # kill size-1 threads waiting
        for _ in range(wait_queue.qsize() - 1):
            task_queue.put("die")
        # release last
        task_queue.put("proceed")

    if message == "die":
        print("%s died without doing stuff" % threading.current_thread())
        pass


t1 = threading.Thread(target=queue_thread, args=(1,))
t2 = threading.Thread(target=queue_thread, args=(2,))
t3 = threading.Thread(target=queue_thread, args=(3,))
t4 = threading.Thread(target=queue_thread, args=(4,))

# allow first thread to pass
task_queue.put("proceed")

t1.start()
t2.start()
t3.start()
t4.start()
