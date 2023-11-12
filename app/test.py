import time
import datetime
now = datetime.datetime.now()


now1 = datetime.datetime.now()
time.sleep(1)
now2 = datetime.datetime.now()
diff = now2 - now1
print(diff.total_seconds())
exit()
seconds = (diff.hours * 60 + diff.minutes) * 60 + diff.seconds
print(seconds)