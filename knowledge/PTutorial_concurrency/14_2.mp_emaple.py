import time
import os
from PIL import Image, ImageFilter

import multiprocessing

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

    # create processes
    processes = [multiprocessing.Process(target=create_thumbnail, args=[filename])
                 for filename in filenames]

    # start the processes
    for process in processes:
        process.start()

    # wait for completion
    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f'It took {finish - start:.2f} second(s) to finish')


if __name__ == '__main__':
    main()