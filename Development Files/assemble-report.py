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

writeHTML_Report = open("index.html","w+") # Create/open a snippets file to create reusable snippets for the report

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
webbrowser.open('file://' + os.path.realpath("index.html"))