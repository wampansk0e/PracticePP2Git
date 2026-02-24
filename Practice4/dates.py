#Write a Python program to subtract five days from current date:
from datetime import datetime, timedelta

current = datetime.now()

date = current - timedelta(days=5)

print(current)
print(date)

#Write a Python program to print yesterday, today, tomorrow:
from datetime import datetime, timedelta
current = date.today()

yesterday = current - timedelta(days=1)
tomorrow = current + timedelta(days=1)

print(yesterday)
print(current)
print(tomorrow)

#Write a Python program to drop microseconds from datetime:
from datetime import datetime 

current = datetime.now()

no_micro = current.replace(microsecond=0)

print(current)
print(no_micro)

#Write a Python program to calculate two date difference in seconds.
from datetime import datetime

date1 = datetime(2025, 2, 24, 9, 41, 0)
date2 = datetime(2026, 2, 24, 9, 41, 30)

time = date2 - date1

seconds = time.total_seconds()

print(date1)
print(date2)
print(int(seconds))