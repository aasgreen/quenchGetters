#!/home/fsf/anaconda3/bin/python
import os.path
import serial
import sys
import time
import csv
import datetime

date = time.strftime("%d/%m/%y")   #get current date
if __name__ == '__main__':

    if len( sys.argv ) != 3:
        print("Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <saveName>")
        sys.exit(1)

    comport = sys.argv[1];
    outName = sys.argv[2];
    
    ser = serial.Serial()
    
    try:
        success = True
        
        ser = serial.Serial( sys.argv[1], 9600, timeout=.5)
        ser.flushInput()
        
        #send serial command to begin reading
        startTime = datetime.datetime.now()
        cmd = 'S0'
        ser.write(str.encode(cmd+'\n'))
        f = open(outName+'.csv','w')
        f.write("#"+date+'\n')
        writer = csv.writer(f,delimiter=",")


        i = 0 #Set while loop to read
        finish =1000000000000 #number of data points
        while i< finish:
            s = ser.readline();
            decode_s = float(s.decode("utf-8"))
            print(decode_s)
            if len(s) > 0:
 #               print(s)
                nowTime = datetime.datetime.now()
                delTime = nowTime-startTime
                writer.writerow([delTime.total_seconds(),decode_s])
            i = i+1
        
        
    except serial.SerialException as e:
        print(e)
        f.close()
        
    except KeyboardInterrupt as e:
        ser.close()
        f.close()

    
