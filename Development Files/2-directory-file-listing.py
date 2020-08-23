#!/usr/bin/python3

import csv
import sys
from datetime import datetime
import os
from os import listdir
import fnmatch

###################################################
# DEFINE TIMESTAMP
###################################################
now = datetime.now()
datestamp = now.strftime("%m%d%Y-%H%M")
datestamp_Readable = now.strftime("%m/%d/%Y - %H:%M")
# print(datestamp) # debug printing timestamp (only date, really)


###################################################
# READING THE CSV DOMAINS LIST
###################################################
with open('domains.csv') as domainCSV:

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
        print('\x1b[3;37;40m' + '  -- Queueing up images for comparison...' + '\x1b[0m')

        path = 'results/' + simplename
        files = sorted(fnmatch.filter(os.listdir(path), "*.jpg")) # Defined a sorted-by-name, only .jpg file list

        file_First = files[0] # Define the most recent image
        try:
            file_Second = files[1] # Define the second most recent image
        except IndexError: # This handles index errors if a second image doesn't exist yet, i.e., you're scanning for the first time. It ends uo comparing against itself for a zero-diff.
            file_Second = files[0]
         
        print('File 1 = ' + file_First) # Debug to test definition
        print('File 2 = ' + file_Second) # Debug to test definition



