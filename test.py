from ClientLauncher.extensions.error_handler import do_without_error

def a():
    return 11


print(do_without_error(a))

