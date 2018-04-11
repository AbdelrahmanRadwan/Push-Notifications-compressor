import datetime
from dateutil import parser

a = "2017-08-01 23:06:47"

day = parser.parse(a)
day = day.replace(hour=23)
day = day.replace(minute=59)
day = day.replace(second=59)

print (day)