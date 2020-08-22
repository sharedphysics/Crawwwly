#!/usr/bin/python3

import csv
import sys
from datetime import datetime
import os
from os import listdir
import fnmatch

# Defining the timestamp upfront:
now = datetime.now()
datestamp = now.strftime("%m%d%Y-%H%M")
# print(datestamp) # debug printing timestamp (only date, really)


###################################################
# READING THE CSV DOMAINS LIST
###################################################
with open('domains-2.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        domainname = row['\ufeffdomains'] # This defines the domains
        simplename = row['simplename'] # This defines the simplename
        outputfilename = simplename + '-' + datestamp + '.png'
        outputfilenamejpg = simplename + '-' + datestamp + '.jpg'


        ###################################################
        # GETTING THE TWO MOST RECENT FILES FOR COMPARISON
        ###################################################
        path = simplename
        files = sorted(fnmatch.filter(os.listdir(path), "*.jpg")) # Defined a sorted-by-name, only .jpg file list

        fileFirst = files[0] # Define the most recent image
        fileSecond = files[1] # Define the second most recent image
        # print(fileFirst) # Debug to test definition
        # print(fileSecond) # Debug to test definition



