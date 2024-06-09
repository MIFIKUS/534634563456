import traceback


def do_without_error(func, args=None):
    if not args:
        while True:
            try:
                return func()
            except Exception as e:
                print(e)
                pass
    else:
        while True:
            try:
                return func(args)
            except Exception as e:
                print(e)
                pass


def endless_error_handler(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception:
                traceback.print_exc()
    return wrapper
