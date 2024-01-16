"""
A semaphore maintains a count. When a thread wants to access the shared resource, the semaphore checks the count.

If the count is greater than zero, it decreases the count and lets the thread accesses the resource. If the count is
zero, the semaphore blocks the thread until the count becomes greater than zero.

A semaphore has two main operations:

Acquire: the acquire operation checks the count and decrement it if it is greater than zero. If the count is zero,
the semaphore will block the thread until another thread releases the semaphore.
Release: the release operation increments the counts that allow other threads to acquire it.
"""

"""
with semaphore:
    # Code within this block has acquired the semaphore

    # Perform operations on the shared resource
    # ...
    
# The semaphore is released outside the with block
"""

import threading
import urllib.request

MAX_CONCURRENT_DOWNLOADS = 3
semaphore = threading.Semaphore(MAX_CONCURRENT_DOWNLOADS)


def download(url):
    with semaphore:
        print(f"Downloading {url}...")

        response = urllib.request.urlopen(url)
        data = response.read()

        print(f"Finished downloading {url}")

        return data


def main():
    # URLs to download
    urls = [
        'https://www.ietf.org/rfc/rfc791.txt',
        'https://www.ietf.org/rfc/rfc792.txt',
        'https://www.ietf.org/rfc/rfc793.txt',
        'https://www.ietf.org/rfc/rfc794.txt',
        'https://www.ietf.org/rfc/rfc795.txt',
    ]

    # Create threads for each download
    threads = []
    for url in urls:
        thread = threading.Thread(target=download, args=(url,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()

#!!!
"""
The output shows that only a maximum of three threads can download at the same time:

Downloading https://www.ietf.org/rfc/rfc791.txt...
Downloading https://www.ietf.org/rfc/rfc792.txt...
Downloading https://www.ietf.org/rfc/rfc793.txt...

####

For example, the following shows that thread #2 completed and released the semaphore, 
and the next thread start downloading the URL https://www.ietf.org/rfc/rfc794.txt

Finished downloading https://www.ietf.org/rfc/rfc792.txt
Downloading https://www.ietf.org/rfc/rfc794.txt...

Use Python semaphore to control the number of threads that can access a shared resource simultaneously

"""
