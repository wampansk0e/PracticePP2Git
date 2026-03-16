#Read and print file contents
filename = "sample_data.txt"

with open(filename, "r") as file:
    print(file.read())