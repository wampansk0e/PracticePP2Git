#Create Nested Directories
import os

path = "my_dir/practice6dir"

os.makedirs(path, exist_ok = True)

#List Files and Folders
import os

items = os.listdir('.')

for item in items:
    if os.path.isdir(item):
        print(f"Folder: {item}")
    else:
        print(f"File: {item}")

#Find Files by Extension
import glob

extension = "*.txt"
files = glob.glob(extension)

for file in files:
    print(f"- {file}")