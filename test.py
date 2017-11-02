from track import Tracker

def pass_callback():
    print('pass')

def fail_callback():
    print('fail')

Tracker('config.json', pass_callback, fail_callback).run()
