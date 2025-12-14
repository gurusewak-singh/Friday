import os
import json

file_path = "song_links.json"

if os.path.exists(file_path):
  try:
    with open(file_path, 'r') as fp:
      songlinks = json.load(fp)
  except:
    songlinks = {}
else:
  songlinks = {}

def addsonglink(song, link):
  songlinks[link] = song
  with open(file_path, 'w') as fp:
    json.dump(songlinks, fp, indent=4)