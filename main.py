from datetime import (datetime, timedelta)
from os.path import (dirname, abspath)
from dateutil import parser
import pandas as pd
import sys
import math
import datetime
from tkinter import filedialog
from tkinter import *

base_dir = dirname(dirname(abspath(__file__)))

# All the users in the system,
Users = dict()
users_names = dict()

class user:

    '''
    A new user just created
    '''
    def __init__(self):
        self.first_notification_time = 0
        self.number_of_notifications = 0
        self.last_notification_time = -1
        self.friends = list()

    '''
    Adding a new notification that came to this user
    '''
    def new_notification(self, time, friend_id):
        self.number_of_notifications += 1
        self.last_notification_time = time
        if friend_id not in self.friends:
            self.friends.append(friend_id)
        #if this is the first notification
        if self.first_notification_time == 0:
            self.first_notification_time = time

    '''
    Firing a push notification, which means 
    to send the push notification to the user and/or save/log it.
    '''
    def fire(self):
        if len(self.friends) == 0:
            return
        elif len(self.friends) == 1:
            print("%s went on a tour." %users_names[self.friends[0]])
        else:
            print("%s and %d other went on a tour." % (users_names[self.friends[0]], self.number_of_notifications - 1))

        self.friends.clear()
        self.number_of_notifications = 0
        self.last_notification_time = -1

'''
Get the directory of the testing data
'''
def get_directory():
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=base_dir, title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

'''
We started a new day
'''
def new_day(day1, day2):
    pass

get_directory()
csv_file = base_dir + '/Komoot/Test_Cases/notifications - sample - one day.csv'
df = pd.read_csv(csv_file)

for i in range(len(df)):
    print(datetime.datetime(df["timestamp"][i]).month)

