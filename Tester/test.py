'''
This file is a unit test, to test if after 
'''
from os.path import (dirname, abspath)

import datetime
import pandas as pd
from tkinter import filedialog
from tkinter import *
from dateutil import parser

base_dir = dirname(dirname(abspath(__file__)))
analytics = dict()
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
Take the analytics dictionary and provide csv file to represent the results well
'''
def analytics_provider():
    rows = list()
    for date in analytics:
        for user in analytics[date]:
            row = [date, user]
            for i in range(len(analytics[date][user])):
                user_day = analytics[date][user][i]
                row.append(user_day[0])
                row.append(user_day[1])
                row.append(user_day[2])
            for i in range(len(analytics[date][user]), 5):
                row.append("-")
                row.append("-")
                row.append("-")

            print(row)
            rows.append(row)


    df_output = pd.DataFrame(rows,
                             columns=("day",
                                      "user",

                                      "notification1_receiving_time",
                                      "notification1_max_delay",
                                      "notification1_number_of_tours",

                                      "notification2_receiving_time",
                                      "notification2_max_delay",
                                      "notification2_number_of_tours",

                                      "notification3_receiving_time",
                                      "notification3_max_delay",
                                      "notification3_number_of_tours",

                                      "notification4_receiving_time",
                                      "notification4_max_delay",
                                      "notification4_number_of_tours",

                                      "notification5_receiving_time",
                                      "notification5_max_delay",
                                      "notification5_number_of_tours"))

    df_output.to_csv(base_dir + "/Tester/Testing_Results/analytics.csv", encoding='utf-8', index=False)


def main():
    global analytics
    # The data sample
    csv_file = base_dir + '/Results/push_notifications.csv'
    # The selected data sample
    directory = get_directory()
    # If the user didn't select anything, use the default csv file
    csv_file = directory or csv_file

    df = pd.read_csv(csv_file)

    for i in range(len(df)):
        timestamp_first_tour = parser.parse(df["timestamp_first_tour"][i])
        notification_sent = parser.parse(df["notification_sent"][i])
        tours = df["tours"][i]
        date = timestamp_first_tour.date()
        user_id = df["receiver_id"][i]

        if date not in analytics:
            analytics[date] = dict()
        if user_id not in analytics[date]:
            analytics[date][user_id] = list()
        x = notification_sent - timestamp_first_tour
        print(i, x)
        analytics[date][user_id].append((notification_sent, notification_sent - timestamp_first_tour,tours))
        if x.days >= 1:
            print(i, date, user_id, analytics[date][user_id][1].days)
            break
    analytics_provider()

if __name__ == '__main__':
    main()