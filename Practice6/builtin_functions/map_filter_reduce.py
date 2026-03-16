#Use map() and filter() on lists
numbers = [10, 20, 30, 40, 50]

formatted_numbers = list(map(lambda p: f"${p}", numbers))
higher_numbers = list(filter(lambda p: p > 30, numbers))

#Aggregate with reduce()
from functools import reduce

words = ["Hello", "World"]

sentence = reduce(lambda x, y: x + " " + y, words)
highest = reduce(lambda a, b: a if a > b else b, numbers)

