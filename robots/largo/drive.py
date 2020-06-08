#!/usr/bin/python
import time
import os
import RPi.GPIO as GPIO
import time
import pymongo
from gpiozero import Servo
from time import sleep
import smbus
import time
from pymongo import ReturnDocument

bus = smbus.SMBus(1)
address = 0x23
myGPIO=18

GPIO.setmode(GPIO.BCM)
energytomove = 250
yellow = 17
white = 22
grey= 23
green = 24

pinset=[yellow,grey,white,green]

for pin in pinset:
    GPIO.setup(pin,GPIO.OUT)

left1=green
left2=white
right1=yellow
right2=grey

with open("/home/pi/.mongo_uri") as fp:
  uri = fp.readline().rstrip()
client = pymongo.MongoClient(uri)

coll = client.motion.votes
framecol = client.vision.frames

def adjust_track(track1,track2,dir):
    if dir == 1:
        GPIO.output(track1,True)
        GPIO.output(track2,False)
    if dir == -1:
        GPIO.output(track1,False)
        GPIO.output(track2,True)
    if dir == 0:
        GPIO.output(track1,False)
        GPIO.output(track2,False)

def adjust_car(left,right):
    adjust_track(left1,left2,left)
    adjust_track(right1,right2,right)

#Connect to MongoDB and Get next set of instructions - plus
#Reset votes
def getdir(doc):
  bestvote=0;
  bestdir=None
  for dir in ('fwd','back','left','right','open','close'):
    if doc.get(dir,0) > bestvote:
        bestvote = doc.get(dir,0)
        bestdir = dir
  return bestdir
count = 0
left=0
right=0
runfor=0
votelen=1
luxspeed=10000


while True:
    lux = bus.read_word_data(address, 0x10)
    print(lux)
    framecol.update_one({'_id':'umberto'},{'$set':{'lux':lux},'$inc':{'energy':int(lux/luxspeed+10)}},upsert=True)
    energy = framecol.find_one_and_update({'_id':'umberto'},{'$set':{'lux':lux},'$min':{'energy':10000}},projection={'energy':1},return_document=ReturnDocument.AFTER)
    doc = coll.find_one_and_replace({"_id":"umberto"}, {},upsert=True);
    print(energy)
    dir = getdir(doc);    
    if dir == None:
        count=count+1
    if dir == 'open':
       myServo = Servo(myGPIO)
       myServo.min()
       time.sleep(0.5)
       myServo.close()
    if dir == 'close':
       myServo = Servo(myGPIO)
       myServo.max()
       time.sleep(0.5)
       myServo.close()
    if dir == 'fwd':
     left=1
     right=1
     runfor=1
    if dir == 'right':
     right=-1
     left=1
     adjust_car(left,right)
     time.sleep(0.15)
     runfor = 0
    if dir == 'left' :
     right=1
     left=-1
     adjust_car(left,right)
     time.sleep(0.15)
     runfor = 0
    if dir == 'back' : 
     right=-1
     left = -1
     runfor=1
    if runfor == 0 :
        left=0
        right=0
        count=0
    else:
       runfor=runfor-votelen
    if not ( left != 0 and left == right and  energy < energytomove ):
      adjust_car(left,right)
      if left != 0 and left == right :
        print("Spending Energy to move")
        framecol.update_one({'_id':'umberto'},{'$inc':{'energy':int(-energytomove)}},upsert=True);
        
    time.sleep(votelen)
GPIO.cleanup()
