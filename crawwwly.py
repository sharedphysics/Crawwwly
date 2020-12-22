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
import pandas
import pandas as pd
import requests
from requests.exceptions import ConnectionError
from pathlib import Path
import matplotlib.pyplot as plt


###################################################
# DEFINE TIMESTAMP
###################################################
now = datetime.now()
datestamp = now.strftime("%m%d%Y-%H%M")
datestamp_Readable = now.strftime("%m/%d/%Y - %H:%M")
# print(datestamp) # debug printing timestamp (only date, really)




###################################################
# VALIDATING THE URLS
###################################################

df = pandas.read_csv('domains.csv')
with open('domains.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        # identification = row['id'] # unused
        domainname = row['domains'] # This defines the domains
        simplename = row['simplename'] # This defines the simplename
        validation = row['validation'] # This defines the validation row
        
        try: 
            checkurl = requests.get(domainname)
            if checkurl.status_code < 400:
                print ('\u001b[37m' + domainname + " has been validated." + '\x1b[0m' + '\n') # Adding some colors as well

        except ConnectionError:
            print ('\u001b[31m' + domainname + " is not valid and will be skipped." + '\x1b[0m' + '\n') # Adding some colors as well

            #print(df)

            # df.loc[<row selection>, <column selection>]
            df.loc[df.domains == domainname, 'validation'] = "false"
            #print(df) # test output
        
    df.to_csv (r'domains.csv', index= False, header = True)




###################################################
# READING THE CSV DOMAINS LIST
###################################################
with open('domains.csv') as domainCSV:

    readCSV = csv.DictReader(domainCSV, delimiter=',')
    for row in readCSV:
        # print (row['\ufeffdomains']) # Debug to test that domains are read correctly

        domainname = row['domains'] # This defines the domains
        simplename = row['simplename'] # This defines the simplename
        validation = row['validation'] # This defines the validation row
        outputfilename = simplename + '-' + datestamp + '.png'
        outputfilenamejpg = simplename + '-' + datestamp + '.jpg'

        if validation != "false": # Do not work with urls that have not been validated. 


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

            os.system ('python3 crawwwly-selenium.py --url ' + domainname + ' --output results/' + simplename + '/' + outputfilename)
            print ('\x1b[3;37;40m' + '  -- File saved as ' + outputfilename + '\x1b[0m') # Log that file was saved



            ###################################################
            # CONVERT FROM PNG TO JPG
            # (because alpha layers mess with differences mapping)
            ###################################################
            try:
                png = Image.open('results/' + simplename + '/' + outputfilename)
                png.load() # required for png.split()

                background = Image.new("RGB", png.size, (255, 255, 255))
                background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

                background.save('results/' + simplename + '/' + outputfilenamejpg, 'JPEG', quality=80)
            
            except FileNotFoundError:
                print("Looks like the file wasn't created because the site didn't get scraped properly.")

            """
            png.load() # required for png.split()

            background = Image.new("RGB", png.size, (255, 255, 255))
            background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

            background.save('results/' + simplename + '/' + outputfilenamejpg, 'JPEG', quality=80)

            print('\x1b[3;37;40m' + '  -- Image converted to .jpg' + '\x1b[0m')
            """


            ###################################################
            # GETTING THE TWO MOST RECENT FILES FOR COMPARISON
            ###################################################
            print('\x1b[3;37;40m' + '  -- Queueing up images for comparison...' + '\x1b[0m')

            path = 'results/' + simplename
            files = sorted(fnmatch.filter(os.listdir(path), simplename+"*.jpg")) # Defined a sorted-by-name, only .jpg file list

            try: # error handling if page isn't scraped the first time.
                file_First = files[-1] # Define the most recent image
                try:
                    file_Second = files[-2] # Define the second most recent image
                except IndexError: # This handles index errors if a second image doesn't exist yet, i.e., you're scanning for the first time. It ends uo comparing against itself for a zero-diff.
                    file_Second = files[-1]
                # else:
                #    print("Page not monitored.")

            except IndexError: # This handles index errors in line 102 if the page wasn't scarped at all.
                    print("Page not monitored.")

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
            # CALCULATE DIFFERENCE PERCENTAGE AS NON-WHITE AREA PERCENTAGE
            ###################################################

            im = Image.open(output_comparisons)

            white = 0
            other = 0

            for pixel in im.getdata():
                if pixel == (255, 255, 255): # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
                   white += 1
                else:
                    other += 1
            print('white=' + str(white)+', Other='+str(other))

            calcDiff = (other / (white + other) * 100)
            diffPercentageRounded = str(round(calcDiff, 2)) #Same thing, but rounded as a two decimal variable

            print("Differences are calculated at " +  diffPercentageRounded + "%") 



            ###################################################
            # WRITE DIFFERENCES TO CSV
            ###################################################
            
            datestamp2 = now.strftime("%m/%d/%Y-%H:%M")
            stringDatestamp = str(datestamp2)
            
            DiffLog = Path(path + "diff-history.csv")

            if DiffLog.is_file():
                writeDiffLog = open(DiffLog,"a+") # open in append mode
                writeDiffLog.write(datestamp2 +  "," + diffPercentageRounded + "\n")
                writeDiffLog.close()
            else: 
                writeDiffLog = open(DiffLog,"w+") # open in write mode
                writeDiffLog.write("timestamp,difference\n") # adds a header b/c the file did not exist before
                writeDiffLog.write(datestamp2 + "," +  diffPercentageRounded +  "\n")
                writeDiffLog.close()



            ###################################################
            # CREATE BAR CHART
            ###################################################

            dataframeDiff = pd.read_csv(path + "diff-history.csv")
            
            #print (dataframeDiff) # Testing data that was read.

            diffplot = plt.bar(x=dataframeDiff['timestamp'], height=dataframeDiff['difference'])

            plt.savefig(path + "diffplot.png")

            plotPath = str(path + "diffplot.png") # save plotpath as a variable for future reference

            ###################################################
            # BUILD HTML REPORT SNIPPETS
            ###################################################

            print('\x1b[3;37;40m' + '  -- Building report snippets' + '\x1b[0m')

            writeHTMLSnippets = open(path + "-snippets.html","w+") # Create/open a snippets file to create reusable snippets for the report
            startImg = """<img class=\"img-large\" src=\"images/"""
            endImg = """\">"""

            writeHTMLSnippets.write(
                    """    <div class=\"clearfix snippet-container\">
                <div class=\"clearfix\" style=\"margin-top25px;\"><h2>""" + simplename + """, """ + domainname + """</h2><br><p>""" + datestamp_Readable + """</p></div>\r\n
                    <div><img src=\"""" + plotPath + """\"></div>\r\n
                    <div class=\"clearfix\"><div class=\"image-container\">\r\n
                        <h3>Current Site</h3>\r\n
                        <a href=\"""" + path_one + """\"><img class=\"imagediff\" src=\"""" + path_one + """\"></a>\r\n
                    </div>    \r\n
                    <div class=\"image-container\">\r\n
                        <h3>Comparative Differences (""" + diffPercentageRounded + """%)</h3>\r\n
                        <a href=\"""" + output_comparisons + """\"><img class=\"imagediff\" src=\"""" + output_comparisons + """\"></a>\r\n
                    </div>\r\n
                    <div class=\"image-container\">\r\n
                        <h3>Previous Capture</h3>\r\n
                        <a href=\"""" + path_two + """\"><img class=\"imagediff\" src=\"""" + path_two + """\"></a>\r\n
                    </div>\r\n
                    </div>
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




