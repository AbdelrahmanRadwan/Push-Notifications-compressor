from os.path import (dirname, abspath)
import datetime
import pandas as pd
from tkinter import filedialog
from tkinter import *
from dateutil import parser
from operator import itemgetter

base_dir = dirname(dirname(abspath(__file__)))

# All the users in the system, ID => user(obj)
Users = dict()
# All the names of the users, ID => Name
users_names = dict()
rows = list()
class user:
    '''
    This class represents the users in the context of getting push notifications.
    '''
    '''
    A new user just created
    '''
    def __init__(self, id):
        self.id = id
        self.first_notification_time = 0
        self.received_push_notifications = 0 # total number of notifications
        self.number_of_notifications = 0 # per session
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
    def fire(self, time):
        global rows

        if len(self.friends) < 1:
            return
        if len(self.friends) == 1:
            message = "%s went on a tour." %users_names[self.friends[0]]
        else:
            message = "%s and %d other went on a tour." % (users_names[self.friends[0]], len(self.friends) - 1)

        rows.append([time,
                     self.first_notification_time,
                     self.number_of_notifications,
                     self.id,
                     message])

        print(time,
              self.first_notification_time,
              self.number_of_notifications,
              self.id,
              message)

        self.received_push_notifications+=1
        self.friends.clear()
        self.number_of_notifications = 0 # per session
        self.last_notification_time = -1
        self.first_notification_time = 0

    '''
    Notify the user with the friend's post in this time stamp.
    This is the route which fires and creates new notifications
    The rules here are:
    - Notification should not wait more than 4h on hold.
    - User should not receive more than 5 notifications per day.
    - Worst case: (4h) (4h) (4h) (4h) (8h) 
    '''
    def notify(self, friend_id, time_stamp):
        #first notification
        # seperated because the default time is 0 (int) not datetime; in order to avoid confusion
        if self.first_notification_time == 0 or self.received_push_notifications >= 4:
            self.new_notification(time_stamp, friend_id)
            return

        #new notification and the difference between it and the older one is less than 4h or not
        time_difference = time_stamp - self.first_notification_time
        number_of_minutes = time_difference.seconds/60
        #the same day, and difference no more than 4 hours, and not the last notification in the day
        if number_of_minutes <= 4*60:
            self.new_notification(time_stamp, friend_id)
        # we are in the first 4 sections, and difference more than 4 hours
        else:
            date1 = time_stamp
            date1 = date1.replace(hour=23)
            date1 = date1.replace(minute=59)
            date1 = date1.replace(second=59)

            date2 = self.first_notification_time + datetime.timedelta(hours=4)

            self.fire(min(date1, date2))
            self.new_notification(time_stamp, friend_id)

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
We started a new day or not
'''
def new_day(day1, day2):

    for _user in Users.values():
        if _user.first_notification_time != 0:
            days_difference = day2 - _user.first_notification_time
            if days_difference.days:
                day_temp = _user.first_notification_time
                day_temp = day_temp.replace(hour=23)
                day_temp = day_temp.replace(minute=59)
                day_temp = day_temp.replace(second=59)

                day1_temp = _user.first_notification_time + datetime.timedelta(hours=4)
                _user.fire(min(day_temp, day1_temp))

    '''days_difference = day2 - day1
    # this should be a new day actually.
    # In this case we have to fire everything that we have from before.
    if days_difference.days:
        for _user in Users.values():

            day_temp = day1
            day_temp = day_temp.replace(hour=23)
            day_temp = day_temp.replace(minute=59)
            day_temp = day_temp.replace(second=59)

            day1_temp = _user.first_notification_time + datetime.timedelta(hours=4)
            _user.fire(min(day_temp, day1_temp))'''

'''
This is the last day in the sheet.
'''
def end_days(day):
    # this should be a new day actually.
    # In this case we have to fire everything that we have from before.
    for _user in Users.values():
        if _user.number_of_notifications:
            day_temp = day
            day_temp = day_temp.replace(hour=23)
            day_temp = day_temp.replace(minute=59)
            day_temp = day_temp.replace(second=59)

            day1_temp = _user.first_notification_time + datetime.timedelta(hours=4)
            _user.fire(min(day_temp, day1_temp))

def main():

    # The data sample
    csv_file = base_dir + '/notification_data/notifications.csv'
    # The selected data sample
    directory = get_directory()
    # If the user didn't select anything, use the default csv file
    csv_file = directory or csv_file

    df = pd.read_csv(csv_file)

    #Going through all the records in the csv file.
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
            Users[user_id] = user(user_id)

        # check if this is a new day or not.
        if i:
            new_day(parser.parse(df["timestamp"][i - 1]), time_stamp)

        # notify the user with the friend's post in this time stamp.
        Users[user_id].notify(friend_id, time_stamp)


    #We reached the end of the file, and some people still didn't receive the final notifications of the last day.
    end_days(parser.parse(df["timestamp"][len(df)-1]))
    # The push notifications output table
    sorted(rows, key=itemgetter(2))
    df_output = pd.DataFrame(rows, columns=("notification_sent", "timestamp_first_tour", "tours", "receiver_id", "message"))
    df_output.to_csv(base_dir + "/push_notifications_results/push_notifications.csv", encoding='utf-8', index=False)

if __name__ == '__main__':
    main()