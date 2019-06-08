# -*- coding: utf-8 -*-


'''This program, when an arduino is connected, will log the measurement'''

import serial
import select
import sys
import numpy as np
import time
import scipy
import csv
Log = 0 #global variable telling us if the arduino is sending data to be logged from a quench run
LogLine = []

port = 0
#Get current date
date = time.strftime("%d/%m/%Y")
connected = False #Variable to see if arduino is connected
try:
    ser = serial.Serial("/dev/ttyACM{:d}".format(port), 9600,timeout=.1) # or acm1
    ser.flushInput()

    #Set loop to check if connected:

    while not connected:
        if ser.read():
            print("Connected!")
            connected = True
        else:
            print('not connected')
            ser.close()
            ser = serial.Serial("/dev/ttyACM{:d}".format(port), 9600,timeout=.1) # or acm1
            ser.flushInput()
            
   #Now, initialize variables to hold data
    glass = []
    film = []

    ## Tell arduino to blink to confirm status

    print("Intructions: C-blink, L:log pressure")

    #Loop to test if user input data, or arduino sends data
    fileWrite=False
    
    while connected:
        try:
            inp, outp, err = select.select([sys.stdin, ser], [], [], .2)

            #if user has typed anything, send it to the arduino

            #print('trying')
            if sys.stdin in inp:
                line = sys.stdin.readline()
        
                linel = line.strip()
                print('line '+line)
                #Test quit condition
                if linel== "q":
                    connected = False
                    ser.close()
                    glassF.close()
                    break
                #If not, then write to serial
                if linel =='L':
                    fileWrite=True
                    glassF = open('pressure'+str(time.time())+'.csv','w')
                    glassF.write("#"+date)
                    print("File Open")
                    writer = csv.writer(glassF,delimiter=',')

                elif line == "t":
                    filmF = open('film'+str(time.stime()),'w')
                    filmF.writelines("#"+date)

                ser.write(linel.encode())
                

            #if the arduino has printed anything, display it:
            if ser in inp:

                line = ser.readline().decode()
                print(line)
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

        except Exception as e:
            print(e)
            ser.close()
            glassF.close()
            break
 
 
except Exception as e:
    print(e)
    ser.close()
    glassF.close()
   #close port and end program
    #glassF.close()
    #Now, read out files created:


