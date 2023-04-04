from functools import partial
import math
import time
import concurrent.futures
import logging
import os
import threading


logging.basicConfig(filename='../artifacts/medium_logging.txt', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def integrate_segment(f, a, b, n_iter):
    current_thread = threading.current_thread()
    thread_id = current_thread.ident
    process_id = os.getpid()
    logging.info(f"Start run task of thread ID: {thread_id} and process ID: {process_id}")
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    logging.info(f"Finish task of thread ID: {thread_id} and process ID: {process_id}")
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, executor_class=concurrent.futures.ThreadPoolExecutor):
    if n_jobs <= 0:
        raise ValueError("n_jobs must be a positive integer")

    segment_n_iter = n_iter // n_jobs
    segment_step = (b - a) / n_jobs

    segments = [(a + i * segment_step, a + (i + 1) * segment_step) for i in range(n_jobs)]

    a_s = [a for a, _ in segments]
    b_s = [b for _, b in segments]
    ff = partial(integrate_segment, f, n_iter=segment_n_iter)
    with executor_class(max_workers=n_jobs) as executor:
        results = executor.map(ff, a_s, b_s)

    return sum(results)


def main_medium():
    cpu_num = os.cpu_count()

    test_values = range(1, cpu_num * 2 + 1)
    with open("../artifacts/medium_time_results.txt", "w") as time_results_file:
        time_results_file.write(f"n_jobs,execution_time\n")

        for n_jobs in test_values:
            for executor_class in [concurrent.futures.ThreadPoolExecutor, concurrent.futures.ProcessPoolExecutor]:
                executor_name = executor_class.__name__
                logging.info(f"Starting {executor_name} with {n_jobs} workers")
                start_time = time.perf_counter()
                result = integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, executor_class=executor_class)
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                time_results_file.write(f"{n_jobs},{execution_time:.6f} <- {executor_name} \n")
                logging.info(f"{executor_name} with {n_jobs} workers finished. Result: {result:.6f}, Execution time: {execution_time:.6f} seconds")
            time_results_file.write("-----------\n")
