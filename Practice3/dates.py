#D A T E S
#A date in Python is not a data type of its own, but we can import a module named datetime to work with dates as date objects.
#Import the datetime module and display the current date:
import datetime

x = datetime.datetime.now()
print(x)

#Return the year and name of weekday:
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#To create a date, we can use the datetime() class (constructor) of the datetime module:
import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#The datetime object has a method for formatting date objects into readable strings.
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))