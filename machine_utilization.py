import psutil
import time
import os


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_cpu_percent():
    process = psutil.Process(os.getpid())
    return process.cpu_percent()


def track():

    mem_before = get_process_memory()
    start = time.time()
    result = ''
    elapsed_time = elapsed_since(start)
    mem_after = get_process_memory()
    print("memory before: ", mem_before)
    print("memory after: ", mem_after)
    print("memory consumed: ", (mem_after - mem_before)/1024, "KB")
    print("cpu percent:", get_cpu_percent())

