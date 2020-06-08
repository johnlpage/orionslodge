#!/usr/bin/python3
import datetime
import serial
import pymongo
import json
import ctypes
from pprint import pprint
from pymongo import MongoClient

with open("/home/pi/.mongo_uri") as fp:
    uri = fp.readline().rstrip()
client = MongoClient(uri)
calibration = -8

# cs = client.vision.food.watch()
with serial.Serial("/dev/ttyACM0", 115200, timeout=1) as ser:
    while True:
        try:
            line = ser.readline()  # read a '\n' terminated line
            if line != b"":
                str = line.decode("utf-8")
                print(str)
                reading = json.loads(str)
                reading["s"] = hex(int(reading["s"]) & 0xFFFFFFFF)
                if reading["n"] == "feed":
                    temp = int(reading["v"]) + calibration
                    now = datetime.datetime.now()
                    doc = {"time": now, "sensor": reading["s"], "value": temp}
                    rval = client.vision.food.update_one(
                        {"_id": "feeding"}, {"$set": doc}, upsert=True
                    )
                    print(doc, rval)
                if reading["n"] == "temp":
                    temp = int(reading["v"]) + calibration
                    now = datetime.datetime.now()
                    doc = {"time": now, "sensor": reading["s"], "value": temp}
                    rval = client.home.temp.insert_one(doc)
                    print(doc, rval)
        except Exception as e:
            print(e)
            # print(line)

        #       a = cs.try_next()

        a = None
        if a != None:
            print(a)
            l = a["fullDocument"]["letter"] + "\n"
            ser.write(l.encode())
