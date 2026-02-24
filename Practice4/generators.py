#Create a generator that generates the squares of numbers up to some number N.
def generator(N):
    for i in range(1, N + 1):
        yield i * i

N = 10
for x in generator(N):
    print(x)

#Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
def even(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i

n = int(input())
print(",".join(str(num) for num in even(n)))

#Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
def divide(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = int(input())
for x in divide(n):
    print(x)

#Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def square(a, b):
    for i in range(a, b + 1):
        yield i * i

a = int(input())
b = int(input())

for x in square(a, b):
    print(x)

#Implement a generator that returns all numbers from (n) down to 0.
def count(n):
    while n >= 0:
        yield n
        n -= 1

n = int(input())

for x in count(n):
    print(x)