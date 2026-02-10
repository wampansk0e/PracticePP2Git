#he else statement is executed when the if condition (and any elif conditions) evaluate to False.
temperature = int(input())

if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")