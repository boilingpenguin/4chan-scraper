import urllib, json, os, datetime
from unidecode import unidecode
import unicodecsv as csv



#CHANGE THESE SETTINGS!
saveDirectory = '/path/to/parent/directory/'
boardLetter = 'pol'

print ("The current working directory is " + saveDirectory)  

#First we'll try to create a folder for the board.
path = saveDirectory + boardLetter
print ("Attempting to create directory for board at %s" % path)
try:  
	os.mkdir(path)
except OSError:  
	print ("Creation of the directory %s failed  - possible directory already exists" % path)
else:  
	print ("Successfully created the directory %s" % path)

#Get the 4chan board catalog JSON file and open it
url = "https://a.4cdn.org/" + boardLetter + "/catalog.json"
response = urllib.urlopen(url)
threadCatalog = json.loads(response.read())

#LOL I HAVE NO IDEA WHAT I'M DOING!

print("BEGINNING 4CHAN FRONT PAGE SCRAPE")
print("Current board: " + boardLetter)

downloadCounter = 0

#Only look at the front page
frontPage = threadCatalog[0]['threads']
#print frontPage[0]['com']

#Create a file to list all threads we've analyzed
allThreadFile = saveDirectory + boardLetter + "/frontPage-" + str(datetime.datetime.now()) + ".csv"
with open(allThreadFile, mode='a') as thread_file:
			thread_writer = csv.writer(thread_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			thread_writer.writerow(["timeStamp", "lastScraped", "posterID", "name", "postID", "subjectText", "commentText"])

print ("Now parsing front page threads...")
#There are always 20 threads on the front page. So we'll loop through and read each one
i = 0

while i < 20:
	print ("STARTING NEW THREAD - #" + str(frontPage[i]['no']))
	
	#Open the thread listing file, and write the information for the current thread
	#First we make some failsafes - if not all the information is filled in.
	if 'sub' in frontPage[i]:
		subjectText = frontPage[i]['sub']
	else:
		subjectText = "No Subject Text Provided"
	if 'com' in frontPage[i]:
		commentText = frontPage[i]['com']
	else:
		commentText = "No Comment Text Provided"
	with open(allThreadFile, mode='a') as thread_file:
			thread_writer = csv.writer(thread_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			try:
				thread_writer.writerow([frontPage[i]['now'], datetime.datetime.now(), frontPage[i]['id'], frontPage[i]['name'], frontPage[i]['no'], subjectText, commentText])
			except:
				thread_writer.writerow([frontPage[i]['now'], datetime.datetime.now(), "No ID", frontPage[i]['name'], frontPage[i]['no'], subjectText, commentText])

	
	# First we create a new directory for the thread
	path = saveDirectory + boardLetter + "/" + str(frontPage[i]['no']) + " - " + frontPage[i]['semantic_url']
	print ("Attempting to create directory for thread %s" % path)
	try:  
	    os.mkdir(path)
	except OSError:  
	    print ("Creation of the directory %s failed  - possible directory already exists" % path)
	else:  
	    print ("Successfully created the directory %s" % path)

	#Now we create a CSV File for the individual thread
	with open(path + "/thread.csv", mode='w') as thread_file:
			thread_writer = csv.writer(thread_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			thread_writer.writerow(["timeStamp", "posterID", "name", "postID", "subjectText", "commentText", "filename"])

	#Get the individual thread JSON file from 4chan and open it
	url = "https://a.4cdn.org/" + boardLetter + "/thread/" + str(frontPage[i]['no']) + ".json"
	response = urllib.urlopen(url)
	individualThread = json.loads(response.read())
	
	#print individualThread['posts']
	
	#Next, we loop through every post in this thread, and start gathering information. I use j to count which post (within the thread) I'm on
	j = 0
	for post in individualThread['posts']:
		#print post
		print ("Now processing post " + str(individualThread['posts'][j]['no']))
		timeStamp = individualThread['posts'][j]['now']
		name = individualThread['posts'][j]['name']
		try:
			posterID = individualThread['posts'][j]['id']
		except:
			posterID = "No ID"
		postID = individualThread['posts'][j]['no']
		if 'sub' in individualThread['posts'][j]:
			subjectText = individualThread['posts'][j]['sub']
		else:
			subjectText = "No Subject Text Provided"
		if 'com' in individualThread['posts'][j]:
			commentText = individualThread['posts'][j]['com']
		else:
			commentText = "No Comment Text Provided"
		#Was there an image posted? Let's snag it!
		if 'tim' in individualThread['posts'][j]:
			OGfilename = unidecode(individualThread['posts'][j]['filename'])
			#OGfilename = unidecode(OGfilename)
			renamedFile = str(individualThread['posts'][j]['tim'])
			fileExtension = str(individualThread['posts'][j]['ext'])
			filename = OGfilename + " - " + renamedFile + fileExtension
			postFile = urllib.URLopener()
			try:
				postFile.retrieve("https://i.4cdn.org/" + boardLetter + "/" + renamedFile + fileExtension, saveDirectory + "/" + boardLetter + "/" + str(frontPage[i]['no']) + " - " + frontPage[i]['semantic_url'] + "/" + filename)
				downloadCounter = downloadCounter + 1
			except:
				print("Fille Download Error :(")
				filename = filename + " - Download Error"
		else:
			filename = "No File Posted"
		
		with open(path + "/thread.csv", mode='a') as thread_file:
			thread_writer = csv.writer(thread_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
			thread_writer.writerow([timeStamp, posterID, name, postID, subjectText, commentText, filename])
	
		j = j + 1

	
	#Iterate the loop
	i = i + 1
print ("Front Page Scrape Completed - " + str(downloadCounter) + " files downloaded")