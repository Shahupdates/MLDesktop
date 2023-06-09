import os
import shutil

# get the list of all files and directories in the desktop
path = os.path.expanduser("~/Desktop")
files = os.listdir(path)

# Loop through the files and move them based on their extension
for file in files:
    name, ext = os.path.splitext(file)
    
    # This is the name of the directory to move the file to
    dir_name = ext[1:]  # remove the dot
    
    # Create the directory if it doesn't already exist
    new_dir = os.path.join(path, dir_name)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
        
    # Move the file
    shutil.move(os.path.join(path, file), new_dir)
