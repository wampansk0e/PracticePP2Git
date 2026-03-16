#Move/Copy Files Between Directories
import shutil
import os

source = "my_file.txt"
destination = "my_dir/practice6dir"

if os.path.exists(source):
    shutil.copy(source, f"{destination}/{source}")
    shutil.move(source, f"{destination}/{source}")