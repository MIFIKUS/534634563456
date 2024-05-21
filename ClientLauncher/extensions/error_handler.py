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
