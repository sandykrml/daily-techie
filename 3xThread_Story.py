#!/usr/bin/env python
import json
from threading import Thread
import queue
import requests
import ast
import datetime
import sys
print(datetime.datetime.now())

num_threads = 15
data_q = queue.Queue()
dataout_q = queue.Queue()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

RawContent = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty").text
rawcon = [int(isli) for isli in ast.literal_eval(RawContent)]

with open("old_story.txt",'r') as nfile:
    fileData = [int(ieva) for ieva in ast.literal_eval(nfile.read())]
Data_Proces = [raw for raw in rawcon if raw not in fileData]
    
fob = open ("url.txt","w")
def eachRequests(each_story):
    story_data = requests.get("https://hacker-news.firebaseio.com/v0/item/"+str(each_story)+".json?print=pretty").text
    story_dict = ast.literal_eval(story_data)
    try:
        #fob.write(story_dict['title'].strip("Show HN:") +"-->"+ story_dict['url']+"\n")
        json.dump({"ID":story_dict['id'] , "Title": story_dict['title'].strip("Show HN:"), "Url" : story_dict['url'].translate(non_bmp_map)},fob)
    except KeyError as err:
        pass     
def thread_pinger(arg1, q):
  while True:
    storyid = q.get()
    eachRequests(storyid)
    q.task_done()

for arg1 in range(num_threads):
  worker = Thread(target=thread_pinger, args=(arg1, data_q))
  worker.setDaemon(True)
  worker.start()

for eachDat in Data_Proces:
  if eachDat:
        data_q.put(eachDat)

data_q.join()

while True:
  try:
    msg = dataout_q.get_nowait()
  except queue.Empty:
    break
  #print (msg)
fob.close()
with open("old_story.txt",'w') as oldfile:
    oldfile.write(RawContent)
print(datetime.datetime.now())
