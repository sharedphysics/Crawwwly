#!/usr/bin/python3

import time
###################################################
# DEFINE TIMESTAMP
###################################################
now = datetime.now()
datestamp = now.strftime("%m%d%Y-%H%M")
datestamp_Readable = now.strftime("%m/%d/%Y - %H:%M")
# print(datestamp) # debug printing timestamp (only date, really)

"""
Development Notes:
- Timestamp details: https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
"""