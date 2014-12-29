import platform


def prevent_standby():
    if platform.system() == 'Windows':
        print('Preventing standby')


def allow_standby():
    if platform.system() == 'Windows':
        print('Allowing standby')


def long_running(func):
    def inner(*args, **kwargs):
        prevent_standby()
        result = func(*args, **kwargs)
        allow_standby()
        return result
    return inner
