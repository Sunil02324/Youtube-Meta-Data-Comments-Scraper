from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

DEVELOPER_KEY = "#AddYourDeveloperKey"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("#AddYourAPIKey")

def add_data(vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments):
	data = [vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category,comments]
	with open("scraper.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

videoId = raw_input("ID of youtube video : \n")
url = "https://www.youtube.com/watch?v=" + videoId
#Request fro Metadata of the Video
video = pafy.new(url)

#Request for Comments
results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoId,
		    textFormat="plainText"
		  ).execute()
totalResults = 0
totalResults = int(results["pageInfo"]["totalResults"])
count = 0
nextPageToken = ''
comments = []
further = True
first = True
while further:
	halt = False
	if first == False:
		print "."
		try:
	  		results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoId,
	  		  textFormat="plainText",
	  		  pageToken=nextPageToken
	  		).execute()
	  		totalResults = int(results["pageInfo"]["totalResults"])
	  	except HttpError, e:
			print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
			halt = True
	if halt == False:
	  	count += totalResults
	  	for item in results["items"]:
		  	comment = item["snippet"]["topLevelComment"]
		  	author = comment["snippet"]["authorDisplayName"]
		  	text = comment["snippet"]["textDisplay"]
		  	comments.append([author,text])
		if totalResults < 100:
			further = False
			first = False
		else:
			further = True
			first = False
			try:
				nextPageToken = results["nextPageToken"]
			except KeyError, e:
				print "An KeyError error occurred: %s" % (e)
				further = False

# Adding the full data to CSV
add_data(videoId,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category,comments)