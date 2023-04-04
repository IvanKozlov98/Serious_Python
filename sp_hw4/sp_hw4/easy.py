import timeit
import threading
import multiprocessing
from functools import partial


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def worker(f, n):
    for _ in range(10):
        f(n)


def main_easy():
    n = 30  # Large number to test
    num_workers = 10

    def my_timeit(func):
        def wrapper(*args, **kwargs):
            start = timeit.default_timer()
            func(*args, **kwargs)
            end = timeit.default_timer()
            execution_time = end - start
            return execution_time
        return wrapper

    @my_timeit
    def synchronous_exec():
        worker(fib, n)

    @my_timeit
    def threading_exec():
        threads = []
        for _ in range(num_workers):
            thread = threading.Thread(target=worker, args=(fib, n))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    @my_timeit
    def multiprocessing_exec():
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.map(partial(worker, fib), [n] * num_workers)

    synchronous_time = synchronous_exec()
    threading_time = threading_exec()
    multiprocessing_time = multiprocessing_exec()

    # Save results to a text file
    with open("../artifacts/easy.txt", "w") as f:
        f.write(f"Synchronous execution: {synchronous_time:.5f} seconds\n")
        f.write(f"Threading execution: {threading_time:.5f} seconds\n")
        f.write(f"Multiprocessing execution: {multiprocessing_time:.5f} seconds\n")
