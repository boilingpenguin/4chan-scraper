# 4chan-scraper #
Use python to scrape the posts, replies, and files from the front page of a 4chan imageboard

## Welcome ##

This simple Python script uses 4chan's read-only APIs (https://github.com/4chan/4chan-API) to scrape the information from the front page of a given imageboard. In addition to saving every image posted to the board, the script will also generate multiple CSV files that record which threads were on the front page at a given time. A folder is generated for each thread's images, as well as an individual CSV file that records each reply in the thread as well.

## Required Modules: ##
This script uses the following python modules:
- unidecode
- urllib
- json
- os
- datetime
- unicodecsv

Make sure that you have all of these installed and updated.

## How to use: ##
1. Before running, open the file and adjust the settings variables at the top of the file. The `saveDirectory` is the top-level folder that 4chan data will be scraped into. Within this folder, the script will create sub-folders for each 4chan board. The `boardLetter` is the 4chan imageboard that you want to download. Only enter the letters, and don't include the forward slashes. For example:


`saveDirectory = '/Users/boilingpenguin/Desktop/4chanDownloader'`

`boardLetter = 'pol'`

2. Run the `4chan Downloader.py` python file. 
3. That's it. Just sit back and wait.

## Known Issues: ##
Full disclaimer - I have no real Python training, and I barely know what I'm doing... I'm sure that as written I've broken a lot of conventions and of course am not doing things "the right way." But it works. Most of the time. Here are some problems that I know about and may get around to fixing eventually.

- Not all boards have the same data. E.g. if there's no "ID" or "name" provided, the script will likely fail. Need to add a check for this metadata, and fill in some other data, such as "No name given"

- Unicode handling is really not well done. Possible it will still fail if passed certain characters that freak out the csv writer. Not sure what the best solution is.

- Really inefficient image downloading - it will re-download the image every time. Not only is this inefficient for network usage, it may inadvertently overwrite the original version. Also really messes up your file metadata most likely

- Time/date formats are inconsistent. Also, 4chan provides EST times, whereas the script will record your local system time. 

- ID versus Tripcode handling. Right now I'm only recording the ID. 
