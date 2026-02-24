#I T E R A T O R S
#An iterator is an object that contains a countable number of values. You can traverse through all the values.
#Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from.

#Return an iterator from a tuple, and print each value:
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#Strings are also iterable objects, containing a sequence of characters:
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#We can also use a for loop to iterate through an iterable object:
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)

#Using loop for string:
mystr = "banana"

for x in mystr:
  print(x)

#To create an object/class as an iterator you have to implement the methods __iter__() and __next__() to your object.
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

#The example above would continue forever if you had enough next() statements, or if it was used in a for loop.
#To prevent the iteration from going on forever, we can use the StopIteration statement.
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)

#G E N E R A T O R S
#A generator function is a special type of function that returns an iterator object.
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)