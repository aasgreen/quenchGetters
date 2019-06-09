# -*- coding: utf-8 -*-


'''This program, when an arduino is connected, will log the measurement'''

import serial
import select
import sys
import numpy as np
import time
import math
import scipy
import csv
Log = 0 #global variable telling us if the arduino is sending data to be logged from a quench run
LogLine = []
pSet = 10000.
voltRead = 0.

arPort = 5
vPort = 4
#Get current date
date = time.strftime("%d/%m/%Y")
arConnected = False #Variable to see if arduino is connected
vConnected = False #Variable to see if arduino is connected
try:
    aSer = serial.Serial("/dev/ttyS{:d}".format(arPort), 9600,timeout=.1) # or acm1
    print('arduino connected!')
except Exception as e:
    print(e)
try:
    vSer = serial.Serial("/dev/ttyS{:d}".format(vPort), 9600,timeout=.1) # or acm1
   # ser.flushInp    
    aSer.flushOutput()
    aSer.flushInput()
    vSer.flushInput()
    vSer.flushOutput()
    print('volt connected!')
    connected=True
    #Set loop to check if connected:

    #while not connected:
    #    if ser.read():
    #        print("Connected!")
    #        connected = True
    #    else:
    #        print('not connected')
    #        ser.close()
    #        ser = serial.Serial("/dev/ttyS{:d}".format(port), 9600,timeout=.1) # or acm1
    #        ser.flushInput()
    #        
   #Now, initialize variables to hold data
    glass = []
    film = []

    ## Tell arduino to blink to confirm status print("Intructions: C-blink, L:log pressure")

    #Loop to test if user input data, or arduino sends data
    fileWrite=False
    cmd = 'S0'
    vSer.write(str.encode(cmd+'\n'))
    while connected:
        try:
            inp, outp, err = select.select([sys.stdin, aSer,vSer], [], [], .2)
            

           
            #if user has typed anything, send it to the arduino
            if sys.stdin in inp:
                line = sys.stdin.readline()
        
                linel = line.strip()
                print('line '+line)
                #Test quit condition
                if linel== "q":
                    connected = False
                    aSer.close()
                    vSer.close()
                    break
                #If not, then write to serial
                if linel =='L':
                    fileWrite=True
                    glassF = open('pressure'+str(time.time())+'.csv','w')
                    glassF.write("#"+date)
                    print("File Open")
                    writer = csv.writer(glassF,delimiter=',')

                elif ('s' in linel):
                    print('test')
                    pSet = float((linel[1::]))
                elif line == "t":
                    filmF = open('film'+str(time.stime()),'w')
                    filmF.writelines("#"+date)

                aSer.write(line.encode())
                #print(line.encode())

            #read voltage and send it to arduino
          
            if vSer in inp :
                line = vSer.readline().decode()
                #print(line.strip())
                try:
                    voltRead =1000*float(line.strip())
               # print('now print')
                    #print("v: "+str(voltRead)) 
                    aSer.write(('v'+str(voltRead)+"\n").encode())
                    #print(('v'+str(voltRead)+"\n").encode())
    #                aSer.flushOutput()
    #                aSer.flushInput()
    #                vSer.flushInput()
    #                vSer.flushOutput()
                    #aSer.write(('v'+str(0.1)+'\r\n').encode())
                except Exception as e:
                    print('stream corrupted')
                    print(e)
                


            #if the arduino has printed anything, display it:
            if aSer in inp:

                line = aSer.readline().decode()
                print('a: '+line)
                LogLine.append(line)
                if Log ==1:
                    qlog.append(line)
                if line == "Begin Read\r\n":
                    qlog=[]
                    Log = 1
                    print('Now going to log data')
                if line == "End Read\r\n":
                    fileName =input('Please enter quenching run...: ')
                    with open('qRun-'+fileName+'.csv','w') as outqlog:
                        for row in qlog[:-1]:
                           outqlog.write(row) 

                    #np.savetxt('qRun-'+fileName+'.csv',qlog,delimiter=',')
                    Log = 0
                if fileWrite:
                    row =  [float(x) for x in line.strip().strip('\x00').split(',')]
                    #glassF.write(row)
                    writer.writerow(row)  
            #    print('printing')
            #time.sleep(.1)
            print(str(pSet)+' '+str(voltRead*10./0.025))
            if (math.isclose(pSet, voltRead*10./0.025,rel_tol=1e-1)):
                print('trigger')
        except Exception as e:
            print(e)
            vSer.close()
            aSer.close()
            break
 
 
except Exception as e:
    print(e)
    vSer.close()
    aSer.close()
   #close port and end program
    #glassF.close()
    #Now, read out files created:


