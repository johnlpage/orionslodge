#!/usr/bin/python
import time
import os
import time
import pymongo
import pantilthat

with open("/home/pi/.mongo_uri") as fp:
    uri = fp.readline().rstrip()

client = pymongo.MongoClient(uri)
coll = client.motion.votes


def getdir(doc):
    bestvote = 0
    bestdir = None
    for dir in ("tiltup", "tiltdown", "panleft", "panright"):
        if doc.get(dir, 0) > bestvote:
            bestvote = doc.get(dir, 0)
            bestdir = dir
    return bestdir


step = 30
count = 0
pan = 0
tilt = 0

while True:
    doc = coll.find_one_and_replace({"_id": "largo"}, {}, upsert=True)
    dir = getdir(doc)
    if dir == None:
        count = count + 1
    if dir == "tiltup":
        tilt = tilt - step
    if dir == "tiltdown":
        tilt = tilt + step
    if dir == "panleft":
        pan = pan + step
    if dir == "panright":
        pan = pan - step

    if pan > 90:
        pan = 90
    if pan < -90:
        pan = -90
    if tilt > 90:
        tilt = 90
    if tilt < -90:
        tilt = -90

    if count > 9:
        count = 0
        pan = 0
        tilt = 0
        pantilthat.tilt(pan)
        pantilthat.pan(tilt)
    else:
        if dir != None:
            count = 0
            pantilthat.tilt(pan)
            pantilthat.pan(tilt)

    time.sleep(1)
