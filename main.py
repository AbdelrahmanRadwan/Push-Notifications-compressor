from os.path import (dirname, abspath)
import pandas as pd
from tkinter import filedialog
from tkinter import *
from dateutil import parser

base_dir = dirname(dirname(abspath(__file__)))

# All the users in the system, ID => user(obj)
Users = dict()
# All the names of the users, ID => Name
users_names = dict()

class user:
    '''
    This class represents the users in the context of getting push notifications.
    '''

    '''
    A new user just created
    '''
    def __init__(self):
        self.first_notification_time = 0
        self.received_push_notifications = 0
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

        self.received_push_notifications+=1
        self.friends.clear()
        self.number_of_notifications = 0
        self.last_notification_time = -1

    '''
    Notify the user with the friend's post in this time stamp.
    This is the route which fires and creates new notifications
    The rules here are:
    - Notification should not wait more than 4h on hold.
    - User should not receive more than 5 notifications per day.
    - Worst case: (4h) (4h) (4h) (4h) (8h) 
    '''
    def notify(self, friend_id, time_stamp):

        pass

'''
Get the directory of the testing data
'''
def get_directory():
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=base_dir, title="Select file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    return root.filename
'''
We started a new day
'''
def new_day(day1, day2):
    pass

def main():
    # The data sample
    csv_file = base_dir + '/Komoot/Test_Cases/notifications - sample - one day.csv'
    # The selected data sample
    directory = get_directory()
    # If the user didn't select anything, use the default csv file
    csv_file = directory or csv_file

    df = pd.read_csv(csv_file)
    for i in range(len(df)):

        time_stamp = parser.parse(df["timestamp"][i])
        user_id = df["user_id"][i]
        friend_id = df["friend_id"][i]
        friend_name = df["friend_name"][i]

        # A new friend, didn't apper before
        if friend_id not in users_names:
            users_names[friend_id] = friend_name
        # A new user, didn't appear before
        if user_id not in Users:
            Users[user_id] = user()

        # notify the user with the friend's post in this time stamp.
        Users[user_id].notify(friend_id, time_stamp)

if __name__ == '__main__':
    main()