"""
Sometimes, you may want to execute a task in the background. To do that you use a special kind of thread called a daemon thread.

By definition, daemon threads are background threads. In other words, daemon threads execute tasks in the background.
Daemon threads are helpful for executing tasks that support non-daemon threads in the program. For example:

Log information to a file in the background.
Scrap contents from a website in the background.
Auto-save the data into a database in the backgro


!!!
The program terminates because it doesn’t need to wait for the daemon thread to complete.
Also, the daemon thread is killed automatically when the program exits.



"""

from threading import Thread
import time


def show_timer():
    count = 0
    while True:
        count += 1
        time.sleep(1)
        print(f'Has been waiting for {count} second(s)...')


t = Thread(target=show_timer, daemon=True)
t.start()

answer = input('Do you want to exit?\n')
