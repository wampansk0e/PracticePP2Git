#The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".
score = int(input())

if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")