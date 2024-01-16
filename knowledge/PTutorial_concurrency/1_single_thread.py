from time import sleep, perf_counter

def task():
    print('Starting a task...')
    sleep(1)
    print('done')


start_time = perf_counter()

task()
task()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')


"""
If you want to wait for the thread to complete in the main thread, you can call the join() method:

new_thread.join()
"""