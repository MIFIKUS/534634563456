def do_without_error(func):
    while True:
        try:
            return func()
        except Exception as e:
            print(e)
            pass
