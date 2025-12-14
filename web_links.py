# web_links = {}

# def addlink(query, link):
#   web_links.update({query : link})

# print(web_links)
import os
import json

file_path = "web_links.json"

if os.path.exists(file_path):
  try:
    with open(file_path, 'r') as fp:
      links = json.load(fp)
  except:
    links = {}
else:
  links = {}

def addlink(query, link):
  links[link] = query

  with open(file_path, 'w') as fp:
    json.dump(links, fp, indent=4)