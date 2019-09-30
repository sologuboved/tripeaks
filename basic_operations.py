import time


def which_watch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("\n{} took {}\n".format(func.__name__, time.strftime("%H:%M:%S", time.gmtime(time.time() - start))))
        return result

    return wrapper
