#!/usr/bin/python3

import os

# You should change 'test' to your preferred folder.
MYDIR = ("romandesignco")
CHECK_FOLDER = os.path.isdir(MYDIR)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)



"""
Development Notes:
- 

"""