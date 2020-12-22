#!/usr/bin/env python3

from PIL import Image
import pandas
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


###################################################
# CREATE BAR CHART
###################################################

dataframeDiff = pd.read_csv("diff-history.csv")
print (dataframeDiff)

diffplot = plt.bar(x=dataframeDiff['timestamp'], height=dataframeDiff['difference'])

plt.savefig('diffplot.png')


"""
s = pd.Series([1, 2, 3])
fig, ax = plt.subplots()
s.plot.bar()
fig.savefig('my_plot.png')
"""

"""
NOTES:

- https://stackoverflow.com/questions/49015957/how-to-get-python-graph-output-into-html-webpage-directly

"""