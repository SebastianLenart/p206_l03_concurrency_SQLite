"""
enerally, programs deal with two types of tasks:

I/O-bound tasks: if a task does a lot of input/output operations, it’s called an I/O-bound task.
Typical examples of I/O-bound tasks are reading from files, writing to files, connecting to databases,
and making a network request. For I/O-bound tasks, you can use multithreading to speed them up.
CPU-bound tasks: when a task does a lot of operations using a CPU, it’s called a CPU-bound task. For example,
number calculation, image resizing, and video streaming are CPU-bound tasks. To speed up the program with lots of
CPU-bound tasks, you use multiprocessing

"""