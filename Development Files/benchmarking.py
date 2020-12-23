#!/usr/bin/python3

import time
import datetime
from datetime import datetime


benchmarkStart = datetime.now()

time.sleep(5)

benchmarkFinish = datetime.now()

benchmarkDiff = benchmarkFinish - benchmarkStart

benchmarkDiffstr = str(benchmarkDiff)

print('Benchmarking the time to finish executing: ' + benchmarkDiffstr)