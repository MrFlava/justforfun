import threading
import datetime

from queue import Queue


class myThread(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_date(self.name, self.counter)
        print("Exiting " + self.name)


def print_date(threadName, counter):
    datefields = []
    today = datetime.date.today()
    datefields.append(today)
    print(
        "%s[%d]: %s" % (threadName, counter, datefields[0])
    )


# Создать треды
thread1 = myThread("Thread", 1)
thread2 = myThread("Thread", 2)

# Запустить треды
thread1.start()
thread2.start()

thread1.join()
thread2.join()
print("Exiting the Program!!!")

# def doubler(number):
#     """
#     A function that can be used by a thread
#     """
#     print(threading.currentThread().getName() + '\n')
#     print(number * 2)
#     print()
#
#
# if __name__ == '__main__':
#     for i in range(5):
#         my_thread = threading.Thread(target=doubler, args=(i,))
#         my_thread.start()
#
#
fibo_dict = {}
shared_queue = Queue()
input_list = [3, 10, 5, 7]

queue_condition = threading.Condition()


def fibonacci_task(condition):
    with condition:

        while shared_queue.empty():
            print("[{}] - waiting for elements in queue..".format(threading.current_thread().name))
            condition.wait()

        else:
            val = shared_queue.get()
            a, b = 0, 1
            for item in range(val):
                a, b = b, a + b
                fibo_dict[val] = a

            shared_queue.task_done()
            print("[{}] fibonacci of key [{}] with result [{}]".
                  format(threading.current_thread().name, val, fibo_dict[val]))


def queue_task(condition):
    print('Starting queue_task...')
    with condition:
        for item in input_list:
            shared_queue.put(item)

        print("Notifying fibonacci task threads that the queue is ready to consume...")
        condition.notifyAll()


threads = []
for i in range(4):
    thread = threading.Thread(target=fibonacci_task, args=(queue_condition,))
    thread.daemon = True
    threads.append(thread)

[thread.start() for thread in threads]

prod = threading.Thread(name='queue_task_thread', target=queue_task, args=(queue_condition,))
prod.daemon = True
prod.start()

[thread.join() for thread in threads]

print("[{}] - Result {}".format(threading.current_thread().name, fibo_dict))