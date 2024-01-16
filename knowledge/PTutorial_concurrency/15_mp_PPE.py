import time
import os
from PIL import Image, ImageFilter

from concurrent.futures import ProcessPoolExecutor

filenames = [
    'images/1.jpg',
    'images/2.jpg',
    'images/3.jpg',
    'images/4.jpg',
    'images/5.jpg',
]


def create_thumbnail(filename, size=(50, 50), thumb_dir='thumbs'):
    # open the image
    img = Image.open(filename)

    # apply the gaussian blur filter
    img = img.filter(ImageFilter.GaussianBlur())

    # create a thumbnail
    img.thumbnail(size)

    # save the image
    img.save(f'{thumb_dir}/{os.path.basename(filename)}')

    # display a message
    print(f'{filename} was processed...')


def main():
    start = time.perf_counter()

    with ProcessPoolExecutor() as executor:
        executor.map(create_thumbnail, filenames)

    finish = time.perf_counter()

    print(f'It took {finish - start: .2f} second(s) to finish')


if __name__ == '__main__':
    main()

"""
The ProcessPoolExecutor extends the Executor class that has three methods:

submit() – dispatch a function to be executed by the process and return a Future object.
map() – call a function to an iterable of elements.
shutdown() – shut down the executor.
To release the resources held by the executor, you need to call the shutdown() method explicitly. To shut down the executor automatically, you can use a context manager.

The Future object represents an eventful result of an asynchronous operation. It has two main methods for getting the result:

result() – return the result from the asynchronous operation.
exception() – return an exception that occurred while running the asynchronous operation.
"""