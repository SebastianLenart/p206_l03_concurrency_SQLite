"""
If you don’t want the put() method to block if the queue is full, you can set the block argument to False:

queue.put(item, block=False)


****************************************
In this case, the put() method will raise the queue.Full exception if the queue is full:

try:
   queue.put(item, block=False)
except queue.Full as e:
   # handle exceptoin

****************************************
To add an item to a sized limited queue and block with a timeout, you can use the timeout parameter like this:

try:
   queue.put(item, timeout=3)
except queue.Full as e:
   # handle exceptoin

****************************************
To get an item from the queue without blocking, you can set the block parameter to False:

try:
   queue.get(block=False)
except queue.Empty:
   # handle exception

****************************************
To get an item from the queue and block it with a time limit, you can use the get() method with a timeout:

try:
   item = queue.get(timeout=10)
except queue.Empty:
   # ...

****************************************
Waiting for all tasks on the queue to be completed
To wait for all tasks on the queue to be completed, you can call the join() method on the queue object:

queue.join()
****************************************
For example, the following creates a queue that can store up to 10 items:
queue = Queue(maxsize=10)


"""