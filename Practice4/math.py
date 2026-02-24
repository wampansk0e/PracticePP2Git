#Write a Python program to convert degree to radian.
import math

degree = float(input())
radian = math.radians(degree)

print(radian)

#Write a Python program to calculate the area of a trapezoid.
a = float(input())
b = float(input())
c = float(input())

area = 0.5 * (a + b) * c

print(area)

#Write a Python program to calculate the area of regular polygon.
import math

sides = int(input())
length = float(input())

area = (sides * length**2) / (4 * math.tan(math.pi / sides))

print(area)

#Write a Python program to calculate the area of a parallelogram.
base = float(input())
height = float(input())

area = base * height

print(area)
