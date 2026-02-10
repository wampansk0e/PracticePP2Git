#If you have only one statement to execute, you can put it on the same line as the if statement.
a = int(input())
b = int(input())
bigger = a if a > b else b
print("Bigger is", bigger)