#!/usr/bin/python3

import csv

with open('domains-2.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        domainname = row['\ufeffdomains'] # This defines the domains
        simplename = row['simplename'] # This defines the domains

        print (simplename,"\n") # Basic implmentation
        print ('\x1b[6;30;42m' + 'I will now scan ' + domainname + '\x1b[0m' + '\n') # Adding some colors as well
        




"""
########################
Development Notes:
########################

- Fixing headers w/ https://stackoverflow.com/questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python

- When printed, the header was showing up with \ufeff in the beginning. This is due to encoding from Excel. There's a fix for it in the form of: https://stackoverflow.com/questions/17912307/u-ufeff-in-python-string/17912811 but for sake of moving things forward I simply included that incoding in how the row is read. 

- Printing as colored text: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python#comment33067813_21786287

"""