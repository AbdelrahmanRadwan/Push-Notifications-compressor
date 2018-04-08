from datetime import datetime, timedelta
from dateutil import parser
import pandas as pd
import sys
import math
import datetime
from os.path import dirname, abspath
from tkinter import filedialog
from tkinter import *

Users = dict()
users_names = dict()

class user:
    number_of_notifications = 0
    last_notification_time = -1
    friends = list()
    def __init__(self, time):
        first_notification_time = time

    def new_notification(self, time, friend_id, friend_name):
        self.number_of_notifications += 1
        self.last_notification_time = time
        if friend_id not in self.friends:
            self.friends.append(friend_id)
    '''
    Firing a push notification, which means 
    to send the push notification to the user and/or save/log it.
    '''
    def fire(self):
        if len(self.friends) == 1:
            print("%s went on a tour." %users_names[self.friends[0]])
        else:
            print("%s and %d other went on a tour." % (users_names[self.friends[0]], self.number_of_notifications - 1))

'''
root = Tk()

root.overrideredirect(1)
root.withdraw()
root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
'''
base_dir = dirname(dirname(abspath(__file__)))

csv_file = base_dir + '/Komoot/Test_Cases/notifications - sample.csv'
df = pd.read_csv(csv_file)

print(df)
