#Backup Using shutil
import shutil

filename = "sample_data.txt"

backup = "sample_data_backup.txt"
shutil.copy(filename, backup)

#Delete Files Safely
import os

filename = "sample_data.txt"

if os.path.exists(filename):
    os.remove(filename)