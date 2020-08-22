#!/usr/bin/python3

import csv
import sys
from datetime import datetime
import os
from os import listdir
import fnmatch
import PIL
from PIL import Image
from PIL import ImageChops

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

        file_First = files[0] # Define the most recent image
        file_Second = files[1] # Define the second most recent image
        # print(file_First) # Debug to test definition
        # print(file_Second) # Debug to test definition



        ###################################################
        # COMPARE DIFFERENCES
        ###################################################
        path_one = path + '/' + file_First
        path_two = path + '/' + file_Second
        output_comparisons = path + '/' + "recent-differences.jpg"

        def compare_images(path_one, path_two, output_comparisons):
            image1 = Image.open(path_one, mode='r')
            image2 = Image.open(path_two, mode='r')

            diff = ImageChops.difference(image1, image2)
            diff.save(output_comparisons)
            #Flag = 1 if ImageChops.difference(image1, image2).getbbox() == None else 0

            #print (Flag)
            #out = abs(image1 - image2)
            #if diff.getbbox():

            ###################################################
            # VIEWING DIFFERENCES IN REALTIME
            ###################################################
            # differencesimage = Image.open(output_comparisons)
            # differencesimage.show()  

        compare_images(path_one, path_two, output_comparisons)








