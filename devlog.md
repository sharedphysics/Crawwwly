# Development Log

## Engine

URL Validation:
* DONE: ~Add URL validation before selenium is run.~
* DONE: ~If URL is not 200, then add mark column "skip" as true~
* DONE: ~When URL has "Skip" = true, then do not continue for this file.~
* For validation fails, add a section in the reports for failed URLs

Error Handling:
* Address error handling --> Selenium "page didn't load" issue
* Address keeping all browsers the same size for accuracy
* Add loop-skipping "Pass" exception (https://stackoverflow.com/questions/38707513/ignoring-an-error-message-to-continue-with-the-loop-in-python)

Selenium:
* Keep browser consistently same size
* Add wait time to ensure pages load correctly

Refactoring:
* Do rewrite to bundle actions -- do all selenium, then all pillow, then all metrics, etc
* Do a calculation of the runtimes between functions by differencing timestamps (https://docs.python.org/3/library/time.html)

Features:
* Record html differences
* Delete .png images
* Read simple names properly and escape them for filenames

## Reports
* Skip folders that are not in the domains.csv list
* Update reports page design as per Figma
* See historic scans

## Metrics

* DONE: ~Pillow: add % comparisons~
* DONE: ~Add % change over time~
* DONE: ~Add visualization of % change over time~
* Rotate X-axis labels 90% to fit better
* Add bar chart labels to better understand data
* Record data to second "full" chart for homepage reference

## Random
* Address which license is being used

## Documentation
* Clean up requirements.txt and dependencies list

---

# Enterprise Dev Log

## Engine

Error HandlingL:
* Address error handling --> Pillow if image not available as per previous selenium bug, measure against self and add note (page not monitored); send email to logs@email.com with error and site and user. 

## Database

* Fork enterprise version to be using a DB instead of CSVs
* Save and read comparative metrics DB
* Read sites to scrape from DB

## Storage

* Fork enterprise version to read from S3
* Save to & read images from AWS S3

## User Mgmt

* Create and log in to accounts
* Allow users to submit their own sites to monitor + validate them (ping w/ 200 response)
* Load data based on user profiles

## Pricing
* Add tiered pricing system
* Add ability to capture payments monthly
* Pricing w/ variables (count by sites monitored)