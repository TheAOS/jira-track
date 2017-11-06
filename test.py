from track import Tracker
from datetime import datetime

def callback(success):
    print (success)

Tracker('config.json', callback).run()
