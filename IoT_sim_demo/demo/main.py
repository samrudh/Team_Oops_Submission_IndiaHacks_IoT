#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import ATT_IOT as IOT                  
from time import sleep                   #pause the app
import string
import random
from random import randint
import thread
from sys import exit
import os



#set up the SmartLiving IoT platform
IOT.DeviceId = 0			 #"8PQHkYNlXdXLfT9Nn9eD5DQ"
IOT.ClientId = "yogesh"
IOT.ClientKey = "lm54hyfwcry"

results=[]


with open('input.txt') as inputfile:
    results = list(csv.reader(inputfile))



# delete the output file devicess.txt
with open('devicess.txt', 'w') as file1:
    pass


### timeup : to end session after endtime
timeup =1




str1 =  ""
str1 = ''.join(results[0])
a = str1.split('\t')
N=  a[1] # total number of devices

R=[]
A=[]
E=[]

#number of RPi R, Arduno A, intel Edision E
# R0 number of Rpi
# R1[0]= number of tem sensor  // number (float)
# R1[1]= Tmin
# R1[2]= Tmax
# R2[0] = number of level sensor  // int
# R2[1] = Lmin
# R2[2] = Lmax
# R3[0] = number of door sensor //boolean
# R= [R0, R1, R2, R3]

str1 =  ""
str1 = ''.join(results[2])
a = str1.split('\t')
R0=  a[2]
A0= a[4]
E0=a[6]

str1 =  ""
str1 = ''.join(results[3])
a = str1.split('\t')
R1=[a[2],a[3],a[4]]
R2=[a[6],a[7],a[8]]
R3=[a[10]]
R= [R0,R1,R2,R3]

str1 =  ""
str1 = ''.join(results[4])
a = str1.split('\t')
A1=[a[2],a[3],a[4]]
A2=[a[6],a[7],a[8]]
A3=[a[10]]
A= [A0,A1,A2,A3]

str1 =  ""
str1 = ''.join(results[5])
a = str1.split('\t')
E1=[a[2],a[3],a[4]]
E2=[a[6],a[7],a[8]]
E3=[a[10]]
E= [E0,E1,E2,E3]

inlist= [N,R,A,E]
#print inlist

#
IOT.connect()

##### add assets to sample devices
#### sample arduino DeviceId
#### sample Edison DeviceId
#### sample Raspberry DeviceId
IOT.DeviceId = "ucbSbmSsfTS3MpDOdP780pW"
IOT.connect()
#IOT.subscribe()
IOT.addAsset(0, "Pressure sensor", "Pressure sensor in inches", False, "number", "Undefined")
IOT.addAsset(1, "Lock On/Off sensor", "Digital lock on or off", False, "boolean", "Undefined")
IOT.sendValueHTTP(15,0)
IOT.sendValueHTTP("True",1)

def sendSamplepack():
    ## send values to Sample sensor
    ## sample Arduino
    IOT.DeviceId = "ucbSbmSsfTS3MpDOdP780pW"
    IOT.connect()
    val = random.uniform(29,31)
    IOT.sendValueHTTP(val,0)
    sleep(2)
    val = randint(0,1)
    if val== 0:
        IOT.sendValueHTTP("False",1)
    elif val == 1:
        IOT.sendValueHTTP("True",1)
    else:
        pass
    sleep(2)



for x in range(0, int(R0)):
    appstr = str(x)
    dtype = "SimulatedRPi" + appstr   
    idtype = "Rpi" + appstr         
    devlist=IOT.createDevice(dtype, "RaspberryPi Board", False)
    with open('devicess.txt', 'a') as file_:
        
        for y in range(0, int(R1[0])):
            sensName= "Temperature Sensor" + str(y)
            IOT.addAsset(y, sensName, "Temparaure sensor", False, "number", "Undefined")
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'T'+'\t'+ str(y) +'\t'+str(R1[1])+'\t'+str(R1[2]) +'\n')
            
        for y in range(0, int(R2[0])):
            sensName= "Level Sensor" + str(y)
            k=(y + int(R1[0]))
            IOT.addAsset(k, sensName, "Level sensor", False, 'integer', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'L'+'\t'+str(k )+ '\t'+str(R2[1])+'\t'+str(R2[2]) + '\n')
            
        for y in range(0, int(R3[0])):
            sensName= "Door Sensor" + str(y)
            k= y + int(R1[0])+ int(R2[0])
            IOT.addAsset(k, sensName, "Door sensor", False, 'boolean', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'D'+'\t'+str(k ) + '\t' + '\n')                  
for x in range(0, int(A0)):
    appstr = str(x)
    dtype = "SimulatedArduino" + appstr  
    devlist=IOT.createDevice(dtype, "Arduino Board", False)
    with open('devicess.txt', 'a') as file_:
        
        for y in range(0, int(A1[0])):
            sensName= "Temperature Sensor" + str(y)
            IOT.addAsset(y , sensName, "Temparaure sensor", False,  'number', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'T' +'\t'+ str(y) +'\t'+str(A1[1])+'\t'+str(A1[2]) + '\n')
            
        for y in range(0, int(A2[0])):
            sensName= "Level Sensor" + str(y)
            k=(y + int(A1[0]))
            IOT.addAsset(y  + int(A1[0]), sensName, "Level sensor", False, 'integer', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'L'+'\t'+str(k ) + '\t'+str(A2[1])+'\t'+str(A2[2])+ '\n')
            
        for y in range(0, int(A3[0])):
            sensName= "Door Sensor" + str(y)
            k= y + int(A1[0])+ int(A2[0])
            IOT.addAsset(y + int(A1[0])+ int(A2[0]), sensName, "Door sensor", False, 'boolean', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'D'+'\t'+str(k ) + '\t' + '\n')
            
for x in range(0, int(E0)):
    appstr = str(x)
    dtype = "SimulatedIntelEdison" + appstr  
    devlist=IOT.createDevice(dtype, "Intel Edision Board", False)
    with open('devicess.txt', 'a') as file_:
        
        for y in range(0, int(E1[0])):
            sensName= "Temperature Sensor" + str(y)
            IOT.addAsset(y, sensName, "Temparaure sensor", False,  'number', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'T' +'\t'+ str(y) +'\t'+str(E1[1])+'\t'+str(E1[2])+ '\n')
            
        for y in range(0, int(E2[0])):
            sensName= "Level Sensor" + str(y)
            IOT.addAsset(y + int(E1[0]), sensName, "Level sensor", False, 'integer', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'L'+'\t'+str(k ) + '\t'+str(E2[1])+'\t'+str(E2[2])+ '\n')
            
        for y in range(0, int(E3[0])):
            sensName= "Door Sensor" + str(y)
            k= y + int(E1[0])+ int(E2[0])
            IOT.addAsset(y + int(E1[0])+ int(E2[0]), sensName, "Door sensor", False, 'boolean', 'Undefined')
            file_.write(devlist[1] + '\t'+devlist [0] + '\t'+'D'+'\t'+str(k ) + '\t' + '\n')




def sendpack():
    ###### sending vallues to created devices
    results=[]
    with open('devicess.txt') as inputfile:
        results = list(csv.reader(inputfile))
    str1 =  ""
    
    for line in results:
        
        str1 = ''.join(line)
        a = str1.split('\t')
        name= a[0]
        idd = 0
        IOT.DeviceId = str(a[1])
        print "This id deviceid:" + '\n'
        print IOT.DeviceId
        idd = int(a[3])
        IOT.connect()
        
        if  a[2] == 'T':
            val = random.uniform(float(a[4]),float(a[5]))
            IOT.sendValueHTTP(val,idd)
            #IOT.send(val,idd)
            sleep(1)
        elif  a[2] == 'L':
            val = randint(int(a[4]),int(a[5]))
            IOT.sendValueHTTP(val,idd)
            sleep(1)
        elif  a[2] == 'D':
            val = randint(0,1)
            if val== 0:
               booll= "True"
            else:
               booll = "False"
                                     
            IOT.sendValueHTTP(booll,idd)
            sleep(1)

        else :
            print "Wromg entry"
                                
#### To get the endtime
str1 =  ""
str1 = ''.join(results[9])
a = str1.split('\t')
endtime = int(a[1])

def thread_func_endtime (endtime,timeup):
    print "Thread started"
    for imc in range(0, endtime):
        print "in thread" + str(imc)
        sleep(60*imc)
    print "exiting application"
    os._exit(1)
    


### network simulation ##############################
str1 = ""
str1 = ''.join(results[7])
a = str1.split('\t')
if a[1] == 'Y':
    print "network simulation needed"
    if a[2]=='F':
        print "Start flickery network thread"
        thread.start_new_thread(thread_func_flicker,())
    elif a[2]=='R':
        print "Start randomRare network thread"
        thread.start_new_thread(thread_func_randomRare,())
    else :
        print "invalid input"
elif a[1]== 'N':
    print "Do nothing"
else :
    print "Invalid input"

def thread_func_flicker():
    while 1:
        os.system('sudo ifconfig wlan0 down')
        sleep(5)
        os.system('sudo ifconfig wlan0 up')
        sleep(600)
	

def thread_func_randomRare():
    while 1:
        os.system('sudo ifconfig wlan0 down')
        sleep(5)
        os.system('sudo ifconfig wlan0 up')
        sleep(randint(600,6000))
                                        

######### Normal working starts ###########
	#### To get the occurance
str1 =  ""
str1 = ''.join(results[6])
a = str1.split('\t')
def thread_func_occurance(a,timeup):
 
    if a[1]=='F':
        for times  in range(0, int (a[2])):
            print "sending packet.." + str(times)+'\n'
            sendpack()
            sendSamplepack()
            sleep(60)
        print "done with for loop !!!!"
        os._exit(1)
                    
    elif a[1]=='P':
        while 1:
            print "sending packet in while"
            sendpack();
            sendSamplepack()
            sleep(int(a[2]));
                
            
    else :
        print "invalid input"
    
    

try:	
    #create timeup flag thread based on endtime
   
    thread.start_new_thread(thread_func_endtime,(endtime, timeup,))
    thread.start_new_thread(thread_func_occurance,(a,timeup, ))
    
except:
    print "unable to start thread"






      
    
                                
          
        
        


