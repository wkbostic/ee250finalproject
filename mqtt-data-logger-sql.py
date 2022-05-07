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
from twilio.rest import Client
from datetime import date
from datetime import datetime

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
cumulative = 0

# Twilio setup
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

#callbacks -all others define in functions module
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe([("vtho/cups",2)])
    client.message_callback_add("vtho/cups", on_message_cup)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# Custom callback for cup
def on_message_cup(client, userdata, msg):
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

    #create Twilio client
    client = Client(account_sid, auth_token)

    while (True):
        # If a message is detected, log number of cups found into database
        if(flag == 1):
            data_out = [date.today().strftime("%m%d%y"),datetime.now().strftime("%H%M"),numcups]
            data_query = "INSERT INTO "+ Table_name +"(date,time,count)VALUES(?,?,?)" 
            logger = userdata['logger']
            logger.Log_sensor(data_query,data_out)
            cumulative += 1
            flag = 0
        
        # If more than 5 cups have been detected today, notify the parent
        if(logger.access_data(table_name='logs.db') == 5):
            message = client.messages.create(
                to="+17143650338",
                from_="+19786783948",
                body="Uh oh! Your child is drinking! There are currently {} cups in their room.".format(1))
            break


########################
