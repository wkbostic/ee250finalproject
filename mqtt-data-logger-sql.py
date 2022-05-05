## Code template from http://www.steves-internet-guide.com/logging-mqtt-sensor-data-to-sql-database-with-python/?fbclid=IwAR35B-yBNrX_B9Fk8AtvuhSzOgSDhKpFSHJ72qcGYoTyb8Lm4BrG-V_GINQ

"""
This will log messages to file.Los time,message and topic as JSON data
"""
from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import os
import time
import sys, getopt,random
import logging
from sql_logger import SQL_data_logger
import threading
from datetime import date
from datetime import datetime

import cv2 as cv
import argparse
import dweepy

#sql
db_file="logs.db"
Table_name="logs"
table_fields={
    "date":"int",
    "time":"int",
    "count":"int"}
###

#global variables
flag = 0
numcups = 0

## frame analyzer
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    frame_gray = cv.GaussianBlur(frame_gray,(5,5),cv.BORDER_DEFAULT)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    facestemp = []
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        if (w > 150 and w < 300 and h > 150 and h < 300):
            frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            facestemp.append((x,y,w,h))
        faceROI = frame_gray[y:y+h,x:x+w]
    #print(facestemp)
    cv.imshow('Capture - Face detection', frame)
    return len(facestemp)

#callbacks -all others define in functions module
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe([("vtho/cups",2)])
    client.message_callback_add("vtho/cups", on_message_cup)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# Custom callback for LED
def on_message_cup(client, userdata, msg):
    # Turn LED on connection D3 on or off
    flag = 1
    numcups = int(str(msg.payload, "utf-8"))
    print(numcups)
    

if __name__ == '__main__':
    #Set up database
    logger=SQL_data_logger(db_file)
    logger.drop_table("logs")
    logger.create_table("logs",table_fields)
    client_userdata = {'logger':logger}

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client(userdata=client_userdata)
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
    parser.add_argument('--face_cascade', help='Path to face cascade.', default='cascade.xml')#haarcascade_frontalface_alt.xml')
    parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
    args = parser.parse_args()
    face_cascade_name = args.face_cascade
    face_cascade = cv.CascadeClassifier()
    #-- 1. Load the cascades
    if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
        print('--(!)Error loading face cascade')
        exit(0)
    camera_device = args.camera
    #-- 2. Read the video stream
    cap = cv.VideoCapture(camera_device)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    count = 0;
    while True:
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        count = count + 1
        a = detectAndDisplay(frame)
        if(count == 100):
                client.publish("vtho/cups", a)
                #dweepy.dweet_for('testthing', {'numcups': a})
                count = 0
        if cv.waitKey(10) == 27:
            cap.release()
            cv.destroyAllWindows()
            break
        if(flag == 1):
            data_out = [date.today().strftime("%m%d%y"),datetime.now().strftime("%H%M"),numcups]
            data_query = "INSERT INTO "+ Table_name +"(date,time,count)VALUES(?,?,?)" 
            logger = userdata['logger']
            logger.Log_sensor(data_query,data_out)
            flag = 0


########################