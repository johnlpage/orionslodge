#!/usr/bin/python
from picamera.array import PiRGBArray
from picamera import PiCamera
from pprint import pprint
import datetime
import time
import base64
import pymongo
import bson
import time
import zlib

vision_width = 128
vision_height = 96
camera = PiCamera()
camera.resolution = (vision_width, vision_height)
camera.color_effects = None
camera.sensor_mode = 0
camera.iso = 800
# camera.rotation = 180
camera.brightness = 55

rawCapture = PiRGBArray(camera)
time.sleep(0.5)
name = "petbot"

with open("/home/pi/.mongo_uri") as fp:
    uri = fp.readline().rstrip()
client = pymongo.MongoClient(uri)

db = client.vision
coll = db.frames
try:
    coll.insert_one({"_id": "umberto"})
except:
    pass


# cycle through the stream of images from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    image = image[:, :, 2]
    bytes = image.tobytes()
    zbytes = zlib.compress(bytes)
    r = {
        "x": vision_width,
        "y": vision_height,
        "data": bson.binary.Binary(zbytes),
        "when": datetime.datetime.utcnow(),
    }
    coll.update_one({"_id": "umberto"}, {"$set": r})
    rawCapture.truncate(0)
    time.sleep(0.1)
