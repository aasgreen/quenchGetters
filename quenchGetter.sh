#!/bin/bash

echo $1 $2
python3 pyserial.py /dev/ttyS$1 $2 > outlog.log
