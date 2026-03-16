#First of all we have to create a text file and write a sample data.
filename = "sample_data.txt"

with open(filename, "w") as file:
    file.write("This is the first line!\n")
    file.write("This is the second line!\n")
    file.write("This is the third line!")

