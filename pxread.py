#!/home/fsf/anaconda3/bin/python
import os.path
import serial
import sys
import time
import csv

date = time.strftime("%d/%m/%y")   #get current date
if __name__ == '__main__':

    if len( sys.argv ) != 3:
        print("Usage: ", os.path.basename( sys.argv[0] ), "<COM port> <GPIB address>")
        sys.exit(1)

    comport = sys.argv[1];
    addr = sys.argv[2];
    
    ser = serial.Serial()
    
    try:
        success = True
        
        ser = serial.Serial( sys.argv[1], 9600, timeout=.5)

        f = open('flukereading'+str(time.time())+'.csv','w')
        f.write("#"+date+'\n')
        writer = csv.writer(f,delimiter=",")

        cmd = '++mode 1'.encode()
        print('Sending:', cmd)     
        ser.write(cmd)
        s = ser.read(256);
        if len(s) > 0:
            print(s)

        print(ser.timeout)
        cmd = '++addr ' + addr
        print('Sending:', cmd)       
        ser.write(cmd.encode())
        s = ser.read(256);
        if len(s) > 0:
            print(s)

        ser.timeout = .5
        cmd = '++auto 1'
        print('Sending:', cmd)        
        ser.write(cmd.encode())
        s = ser.readlines(256);
        if len(s) > 2:
            print(s)

        i = 0 #Set while loop to read
        finish =1000000000000 #number of data points
        cmd = '++read'
        print('Sending:', cmd)        
        ser.write(cmd.encode())
        while i< finish:
            s = ser.readline();
            decode_s = float(s.decode("utf-8"))
            if len(s) > 0:
 #               print(s)
                writer.writerow([time.time(),decode_s])
            i = i+1
        
        
    except serial.SerialException as e:
        print(e)
        f.close()
        
    except KeyboardInterrupt as e:
        ser.close()
        f.close()

    
