#!/usr/bin/python3

import csv
import os
from os import listdir
import fnmatch
import sys
from datetime import datetime
import PIL
from PIL import Image
from PIL import ImageChops
import webbrowser
import codecs


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
with open('domains-2.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        domainname = row['\ufeffdomains'] # This defines the domains
        simplename = row['simplename'] # This defines the simplename
        outputfilename = simplename + '-' + datestamp + '.png'
        outputfilenamejpg = simplename + '-' + datestamp + '.jpg'

        print ('\x1b[6;30;42m' + 'Now scanning: ' + domainname + '\x1b[0m' + '\n') # Adding some colors as well
       


        ###################################################
        # CHECK OR MAKE IMAGE DIRECTORIES
        ###################################################

        domainfolder = ('results/' + simplename)
        checkfolder = os.path.isdir(domainfolder)

        # If folder doesn't exist, then create it.
        if not checkfolder:
            os.makedirs(domainfolder)
            print('\x1b[3;37;40m' + '  -- New folder created for this domain' + '\x1b[0m')



        ###################################################
        # RUNNING SELENIUM TO CAPTURE SCREENSHOTS
        ###################################################

        os.system ('python3 crawly-selenium.py --url ' + domainname + ' --output results/' + simplename + '/' + outputfilename)
        print ('\x1b[3;37;40m' + '  -- File saved as ' + outputfilename + '\x1b[0m') # Log that file was saved



        ###################################################
        # CONVERT FROM PNG TO JPG
        # (because alpha layers mess with differences mapping)
        ###################################################
        png = Image.open('results/' + simplename + '/' + outputfilename)
        png.load() # required for png.split()

        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

        background.save('results/' + simplename + '/' + outputfilenamejpg, 'JPEG', quality=80)

        print('\x1b[3;37;40m' + '  -- Image converted to .jpg' + '\x1b[0m')



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
         
            # print('File 1 = ' + file_First) # Debug to test definition
            # print('File 2 = ' + file_Second) # Debug to test definition



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



        ###################################################
        # BUILD HTML REPORT SNIPPETS
        ###################################################

        print('\x1b[3;37;40m' + '  -- Building report snippets' + '\x1b[0m')

        writeHTMLSnippets = open(path + "-snippets.html","w+") # Create/open a snippets file to create reusable snippets for the report
        startImg = """<img class=\"img-large\" src=\"images/"""
        endImg = """\">"""

        writeHTMLSnippets.write(
                """    <div style=\"margin-top:100px; z-index:500;\">
            <h2>""" + simplename + """, """ + datestamp_Readable + """</h2>\r\n
                <div class=\"image-container\">\r\n
                    <h3>Current Site</h3>\r\n
                    <a href=\"""" + path_one + """\"><img class=\"imagediff\" src=\"""" + path_one + """\"></a>\r\n
                </div>    \r\n
                <div class=\"image-container\">\r\n
                    <h3>Comparative Differences</h3>\r\n
                    <a href=\"""" + output_comparisons + """\"><img class=\"imagediff\" src=\"""" + output_comparisons + """\"></a>\r\n
                </div>\r\n
                <div class=\"image-container\">\r\n
                    <h3>Previous Capture</h3>\r\n
                    <a href=\"""" + path_two + """\"><img class=\"imagediff\" src=\"""" + path_two + """\"></a>\r\n
                </div>\r\n
            </div>\r\n
            """
        )
        writeHTMLSnippets.close()

        print('\x1b[3;37;40m' + '  -- Finished building report snippets' + '\x1b[0m' + '\n')
        


###################################################
# COMBINE SNIPPETS INTO HTML REPORT
###################################################

print ('\x1b[6;30;42m' + 'Assembling full report...' + '\x1b[0m' + '\n') # Adding some colors as well

writeHTML_Report = open("Report.html","w+") # Create/open a snippets file to create reusable snippets for the report

# Assemble the top section
readTop=codecs.open('top.html', 'rb', encoding='utf-8')
writeHTML_Report.write(readTop.read()) 
writeHTML_Report.write("\n")

# Iterating through the snippets to add into the full report
reportSnippet_dirs = sorted(os.listdir("results"))
for file in reportSnippet_dirs: 
    if file.endswith(".html"): # Reading only .html files
        # This is a loop for each file.
        # It reads each file and reads the content to the writeFile, then adds a line break ("\n")
        readFile=codecs.open('results/' + file, 'rb', encoding='utf-8')
        writeHTML_Report.write(readFile.read()) 
        writeHTML_Report.write("\n") 

# Assemble the bottom section
writeHTML_Report.write("""</body></html>""") 

# Close the file
writeHTML_Report.close()

print ('\x1b[6;30;42m' + 'Report completed' + '\x1b[0m' + '\n') # Adding some colors as well

# Open the file to view the report.
webbrowser.open('file://' + os.path.realpath("Report.html"))




