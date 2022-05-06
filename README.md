# ee250finalproject
Names: Kristian Vu Bostic <wbostic@usc.edu>, Vy Ho <vtho@usc.edu>, Nika Shroff <nikashro@usc.edu> 

Video demo: 
	Demo run on computer: https://drive.google.com/file/d/13cG4oClyolC7JFaKpIJ3FGQwhRPHUBrl/view?usp=sharing
		Shows cup being tracked in camera view, freeboard sparkline showing number of cups, and number of cups being
		sent to MQTT broker and subscribers in terminal in background
	Demo of MQTT sending data from RPI: 
		Picture is taken using Arducam, number of cups is analyzed and sent to computer

Instructions: 
cuptracker.py is likely not runnable unless you have an Arducam. cuptrackerdemo.py should be run instead for demo purposes. 
Either run cuptracker.py on RPI and mqtt-data-logger-sql.py on computer or cuptrackerdemo.py and mqtt-data-logger-sql.py
both on computer, in separate terminals. 

External libraries: 
	Python libraries: sqlite3, paho.mqtt.client, twilio, Raspicam, OpenCV, dweepy
	External programs: Cascade Trainer GUI (https://amin-ahmadi.com/cascade-trainer-gui/)
