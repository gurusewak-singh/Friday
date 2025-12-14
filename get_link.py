from serpapi import GoogleSearch
from web_links import links, addlink
from song_links import songlinks, addsonglink
import re
import os
from dotenv import load_dotenv

load_dotenv()
SERP_API_KEY = os.getenv('SERP_API_KEY')

def getsonglink(query):
  query = query.lower()
  song = re.split(r"\bby\b|\bfrom\b", query)[0].strip()

  if song in songlinks:
    return songlinks[song]
  
  params = {
  "search_query" : query,
  "api_key" : SERP_API_KEY,
  "engine" : "youtube"
  }
  search_result = GoogleSearch(params)
  result = search_result.get_dict()
  link = result["video_results"][0]["link"]
  addsonglink(song, link)
  return link

# print(getsonglink("tum ho from rockstar"))

def getlink(query):
  query = query.lower()
  
  if query in links:
    return links[query]
  
  params = {
  "q" : query,
  "api_key" : SERP_API_KEY
}
  search_result = GoogleSearch(params)
  result = search_result.get_dict()
  link = result["organic_results"][0]["link"]
  
  addlink(query, link)

  return link

# print(getlink("Youtube"))