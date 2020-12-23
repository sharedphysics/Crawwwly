#!/usr/bin/env python3

###################################################
# This is a standalone file. Full script integrated into crawwwly.py
###################################################

import csv
import os
from os import listdir
import fnmatch
import sys
import pandas
import pandas as pd
import requests
from requests.exceptions import ConnectionError


###################################################
# VALIDATING THE URLS
###################################################

df = pandas.read_csv('domains.csv')
with open('domains.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        identification = row['id'] # This defines the domains
        domainname = row['domains'] # This defines the domains
        simplename = row['simplename'] # This defines the simplename
        validation = row['validation'] # This defines the validation row
        
        try: 
            checkurl = requests.get(domainname)
            if checkurl.status_code < 400:
                print ('\x1b[6;30;42m' + domainname + " has been validated." + '\x1b[0m' + '\n') # Adding some colors as well

        except ConnectionError:
            print ('\x1b[6;30;42m' + domainname + " is not valid and will be skipped." + '\x1b[0m' + '\n') # Adding some colors as well

            #print(df)

            # df.loc[<row selection>, <column selection>]
            df.loc[df.domains == domainname, 'validation'] = "false"
            #print(df) # test output
        
    df.to_csv (r'domains.csv', index= False, header = True)
           

"""
Documentation:

https://stackoverflow.com/questions/6471275/python-script-to-see-if-a-web-page-exists-without-downloading-the-whole-page

If domain is valid:
https://www.codespeedy.com/check-if-a-string-is-a-valid-url-or-not-in-python/#:~:text=To%20check%20whether%20the%20string,…)%20if%20URL%20is%20invalid.
https://stackoverflow.com/questions/48665846/check-if-a-website-exists-with-requests-isnt-working/48666039

Reaplcing values:
https://stackoverflow.com/questions/23307301/replacing-column-values-in-a-pandas-dataframe


"""

