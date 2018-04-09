import datetime
from dateutil import parser
a = "2017-08-01 00:06:47"
b = "2017-08-02 00:31:05"

a = parser.parse(a)
b = parser.parse(b)
c = b-a
print(c.days)

