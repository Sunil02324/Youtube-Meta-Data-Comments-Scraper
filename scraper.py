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

DEVELOPER_KEY = "##"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("##")


def add_data(conceptId,conceptName, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category):
	data = [conceptId,conceptName, vID,title,description,author,published,viewcount, duration, likes, dislikes,rating,category]
	with open("scraper.csv", "a") as fp:
	    wr = csv.writer(fp, dialect='excel')
	    wr.writerow(data)

def add_somedata(conceptId,conceptName,count):
  data = [conceptId,conceptName,count]
  with open("missing.csv", "a") as fp:
      wr = csv.writer(fp, dialect='excel')
      wr.writerow(data)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

wb = load_workbook(filename='concepts.xlsx', read_only=True)
ws = wb['ca_concepts']
concepts = 0
for li in ws.rows:
  conceptId = li[0].value
  conceptName = li[1].value
  search_response = youtube.search().list(
      q=conceptName,
      part="id,snippet",
      maxResults=30
    ).execute()
  count = 0
  for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        if count < 10:
          vID = search_result["id"]["videoId"]
          url = "https://www.youtube.com/watch?v=" + vID
          loop1 = True
          Try = True
          while loop1 and Try:
            try:
              video = pafy.new(url)
              loop1 = False
            except IOError as e:
              print e
              print "Socket error. Sleeping for 2 seconds"
              Try = False
              sleep(2)
              continue
            except requests.exceptions.ConnectionError as e:
              print "Proxy Error. Sleeping for 2 seconds"
              Try = False
              sleep(2)
              continue  
          if Try:
            add_data(conceptId,conceptName,vID,video.title,video.description,video.author,video.published,video.viewcount, video.duration, video.likes, video.dislikes,video.rating,video.category)
            count += 1
            print str(count) + ") Added new video " + vID
        else:
          break
      else:
        continue
  concepts += 1
  if count < 10:
    add_somedata(conceptId,conceptName,count)
  print str(concepts) + ") Scraping Done for " + str(conceptId) + " - " + str(conceptName)
print "Scraped " + str(concepts) + " Concepts"
