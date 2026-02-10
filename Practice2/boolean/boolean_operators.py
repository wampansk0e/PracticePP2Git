#The bool() function allows you to evaluate any value, and give you True or False in return
#The following will return True:
one = bool("abc")
two = bool(123)
two = bool(["apple", "cherry", "banana"])

#The following will return False:
four = bool(False)
five = bool(None)
six = bool(0)
seven = bool("")
eight = bool(())
nine = bool([])
ten = bool({})

print(one)