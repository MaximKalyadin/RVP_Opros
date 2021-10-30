from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1


def event(pid, counter):
    counter += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid) + local_time(counter))
    return counter


def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    event(pid, counter)


def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    recv_message(pipe23, pid, counter)


def process_three(pipe32):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe32, pid, counter)
    send_message(pipe32, pid, counter)


if __name__ == '__main__':
    one_and_two, two_and_one = Pipe()
    two_and_three, three_and_two = Pipe()

    process1 = Process(target=process_one,
                       args=(one_and_two,))
    process2 = Process(target=process_two,
                       args=(two_and_one, two_and_three))
    process3 = Process(target=process_three,
                       args=(three_and_two,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
