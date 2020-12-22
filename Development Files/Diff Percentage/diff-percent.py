#!/usr/bin/env python3

from PIL import Image
import pandas
import pandas as pd
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
"""
            ###################################################
            # COMPARE DIFFERENCES
            ###################################################
            path_one = path + '/' + file_First
            path_two = path + '/' + file_Second
            output_comparisons = path + '/' + "differences-" + datestamp + ".jpg"

            print('\x1b[3;37;40m' + '  -- Comparing ' + file_First + ' and ' + file_Second + '\x1b[0m')

            def compare_images(path_one, path_two, output_comparisons):
                image1 = Image.open(path_one, mode='r')
                image2 = Image.open(path_two, mode='r')

                diff = (ImageChops.difference(image1, image2)) # Run the difference comparison
                invert = ImageChops.invert(diff) # Invert the results b/c otherwise it is mostly black
                invert.save(output_comparisons)

                ###################################################
                # VIEWING DIFFERENCES IN REALTIME
                # (for debugging)
                ###################################################
                # differencesimage = Image.open(output_comparisons)
                # differencesimage.show() 
                        
            compare_images(path_one, path_two, output_comparisons)

            print('\x1b[3;37;40m' + '  -- Comparison finished, output saved as ' + output_comparisons + '\x1b[0m')
"""

###################################################
# COMPARE TWO IMAGES
###################################################

ImagePercent1 = Image.open("image1.jpg")
ImagePercent2 = Image.open("image2.jpg")
assert ImagePercent1.mode == ImagePercent2.mode, "Different kinds of images."
#assert ImagePercent1.size == ImagePercent2.size, "Different sizes."
 
pairs = zip(ImagePercent1.getdata(), ImagePercent2.getdata())
if len(ImagePercent1.getbands()) == 1:
    # for gray-scale jpegs
    dif = sum(abs(p1-p2) for p1,p2 in pairs)
else:
    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
 
ncomponents = ImagePercent1.size[0] * ImagePercent1.size[1] * 3
differencePercentage = (dif / 255.0 * 100) / ncomponents # Difference percentage
differencePercentageRounded = str(round(differencePercentage, 2)) #Same thing, but rounded as a two decimal variable

print ("Differences are calculated at " +  differencePercentageRounded + "%")


###################################################
# CALCULATE NON-WHITE AREA PERCENTAGE
###################################################

im = Image.open("diff.jpg")

white = 0
other = 0

for pixel in im.getdata():
    if pixel == (255, 255, 255): # if your image is RGB (if RGBA, (0, 0,     0, 255) or so
       white += 1
    else:
        other += 1
print('white=' + str(white)+', Other='+str(other))

calcDiff = (other / (white + other) * 100)

diffPercentageRounded = str(round(calcDiff, 2)) #Same thing, but rounded as a two decimal variable

print("Differences are calculated at " +  diffPercentageRounded + "%") 




###################################################
# WRITE DIFF TO CSV
###################################################

now = datetime.now()
datestamp = now.strftime("%m/%d/%Y-%H:%M")
stringDatestamp = str(datestamp)

DiffLog = Path("diff-history.csv")

if DiffLog.is_file():
    writeDiffLog = open(DiffLog,"a+") # open in append mode
    writeDiffLog.write(datestamp +  "," + diffPercentageRounded + "\n")
    writeDiffLog.close()
else: 
    writeDiffLog = open(DiffLog,"w+") # open in write mode
    writeDiffLog.write("timestamp,difference\n")
    writeDiffLog.write(datestamp + "," +  diffPercentageRounded +  "\n")
    writeDiffLog.close()


"""
Notes: 

- https://rosettacode.org/wiki/Percentage_difference_between_images#Python
- https://stackoverflow.com/questions/20457038/how-to-round-to-2-decimals-with-python
"""