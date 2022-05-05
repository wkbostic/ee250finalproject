# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 15:55:17 2021

@author: wkris
"""

from __future__ import print_function
import cv2 as cv
import argparse
import dweepy
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
    print(facestemp)
    cv.imshow('Capture - Face detection', frame)
    return len(facestemp)
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
            #dweepy.dweet_for('testthing', {'numcups': a})
            count = 0
    if cv.waitKey(10) == 27:
        cap.release()
        cv.destroyAllWindows()
        break