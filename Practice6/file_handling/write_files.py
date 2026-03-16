#Append and Verify
filename = "sample_data.txt"

with open(filename, "a") as file:
    file.write("\nNew line for Task 3")

with open(filename, "r") as file:
    print(file.read())



