#!/usr/bin/env python
import socket,json,time
import sys
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/GreenHouse')
#from flask import Flask,render_template,url_for,request
db=client.GreenHouse
tests=db.tests
TCP_IP = '192.168.43.89'
TCP_PORT = 12397
field1=tests.insert({'Name':'pict','Hum':"61",'Lum':"0",'Temp':"30",'Moist':"0"})

while 1:
	s = socket.socket()
	s.connect((TCP_IP, TCP_PORT))
	data = s.recv(1024)
	#print(data)
	newdata = json.loads(data)
	if newdata["Name"]==None:
		Name=newdata["Name"]
		Name=0;
	else:	
		Name =(newdata["Name"])

	if newdata["Hum"]==None:
		Hum=newdata["Hum"]
		Hum=0;
	else:	
		Hum =(newdata["Hum"])

	if newdata["Temp"]==None:
		Temp=newdata["Temp"]
		Temp=0;
	else:	
		Temp =(newdata["Temp"])

	if newdata["Lum"]==None:
		Lum=newdata["Lum"]
		Lum=0;
	else:	
		Lum=(newdata["Lum"])

	if newdata["Moist"]==None:
		Moist=newdata["Moist"]
		Moist=0;
	else:	
		Moist =(newdata["Moist"])

	if Name==None:
		field=tests.insert({'Name':0,'Hum':Hum,'Lum':Lum,'Temp':Temp,'Moist':Moist})
	elif ( Hum==None):
		field=tests.insert({'Name':Name,'Hum':0,'Lum':Lum,'Temp':Temp,'Moist':Moist})
	elif ( Lum==None):
		field=tests.insert({'Name':Name,'Hum':Hum,'Lum':0,'Temp':Temp,'Moist':Moist})	
	elif ( Temp==None):
		field=tests.insert({'Name':Name,'Hum':Hum,'Lum':Lum,'Temp':0,'Moist':Moist})
	elif ( Moist==None):
		field=tests.insert({'Name':Name,'Hum':Hum,'Lum':Lum,'Temp':Temp,'Moist':0})	
	else:
		field=tests.insert({'Name':Name,'Hum':Hum,'Lum':Lum,'Temp':Temp,'Moist':Moist})
	time.sleep(16)
	
	tests.remove(field)
		
		
	s.close()


