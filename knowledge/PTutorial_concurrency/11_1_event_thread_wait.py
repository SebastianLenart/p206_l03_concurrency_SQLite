from threading import Thread, Event
from time import sleep

def task(event: Event, id: int) -> None:
    print(f'Thread {id} started. Waiting for the signal....')
    event.wait()
    print(f'Received signal. The thread {id} was completed.')

def main() -> None:
    event = Event()

    t1 = Thread(target=task, args=(event,1))
    t2 = Thread(target=task, args=(event,2))

    t1.start()
    t2.start()

    print('Blocking the main thread for 3 seconds...')
    sleep(3)
    event.set()



if __name__ == '__main__':
    main()

"""
Thread 1 started. Waiting for the signal....
Thread 2 started. Waiting for the signal....
Blocking the main thread for 3 seconds...
Received signal. The thread 1 was completed.
Received signal. The thread 2 was completed.

"""


"""
Use the threading.Event class to communicate between threads.
Use the set() method to set the event and clear() method to unset the event.
Use the is_set() method to check if an event is set.
Use the wait() method to wait for the event to be set.

"""