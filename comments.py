import csv
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
from time import sleep
from openpyxl import load_workbook
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')  

DEVELOPER_KEY = "###"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("##")

def add_data(conceptId,conceptName, vID, comments):
	data = [conceptId,conceptName, vID, comments]
	with open("comments.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

wb = load_workbook(filename='videos.xlsx', read_only=True)
ws = wb['Sheet1']
concepts = 0
for li in ws.rows:
  conceptId = li[0].value
  conceptName = li[1].value
  video_id = li[2].value
  if len(video_id) == 11:
  	stopHere = False
  	print video_id
  	try:
		results = youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=video_id,
		    textFormat="plainText"
		  ).execute()
	except HttpError, e:
		print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
		stopHere = True
	if stopHere == False:
		print '.'
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
			  		  videoId=video_id,
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
		add_data(conceptId,conceptName,video_id,comments)
		concepts += 1
		print str(concepts) + ') ' +str(conceptId) + ' : ' + str(conceptName) + ' - ' + str(video_id) + ' Scrapped ' + str(count) + ' comments'
print "Done Scrapping all Videos : " + str(concepts)