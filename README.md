![Example comparison, 10 minutes apart](example.png)

# Crawwwly - Visual Logging

This script is designed to help with visually-driven comparative monitoring. Crawwwly will go to a site, take a full screenshot, and compare that against the last screenshot captured to identify differences.

## How it works

Crawwwly goes through a multi-step process to capture, analyze, and report on data:

1. It parses a `.CSV` file to create a list of domains to scan
2. For each domain, a directory is created to begin capturing images for analysis
3. `Selenium` + `Firefox` open the site and capture a full-page screenshot
4. That image is compared against the previously captured image, as sorted by name (which means that if you're running Crawwwly multiple times a day, it may not compare correct images). If you're scanning a domain for the first time, the image is compared against itself. This is done through `Pillow`
5. An html snippet is generated for displaying the comparisons
6. Once all of the domains have been scanned, a full report is assembled into a single page from all of the snippets
7. The report is auto-opened for reading pleasure

# Running Crawwwly for the first time

# How to Use It
Crawly requires `FireFox`, `Python3`, `Selenium`, and `Pillow`. All of these (except Firefox) and be downloaded and configured from the `requirements.txt` file.

## Requirements
- Designed to run on `MacOS`, not `Windows`
- Requires to have `FireFox` installed
- Requires `Python3`

Running Crawwwwly is really easy:

1. Modify the `domains.csv` file, adding the full URLs that you want to monitor in column 1, and the appropriate "simple name" (no punctuation or spaces) in column 2. This will be used to set the web paths for scanning and then how those images and directories will be created.
2. In your terminal, enter the directory where Crawwwly was saved
3. Use `pip3 install requirements.txt` to install the dependencies
4. Run the script as `python3 crawwwwly.py` 

After that, you can run the script as `python3 crawwwwly.py`

## Setting a CRON

The real value of this script is to set up once and have it running on a schedule. If you're running Crawwwly locally, you can refer to: https://medium.com/better-programming/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30 otherwise, you'll need to refer to your server/hosting to figure out their cron-scheduling solution. 

I recommend running the script weekly for best results, but no more than daily. 

---

# Development Log

## V2
- Parse filenames to ensure correct last 2 images are being compared
- Capture difference as % for plotting
- Figuring out if we can bypass png->jpg conversion to avoid the alpha channel (transparency) issue
- Add a plot chart
- Terminal alert (email?) - % differences between two images, flagging above x%
- Refactoring for optimization: making all of the similar steps run together (i.e., to not open/close firefox and selenium for each site)

## General to do...
- Logo
- Hosted version for SaaS
