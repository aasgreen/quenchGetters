#!/bin/bash

echo $1
gnuplot -e "filename='$1'" --persist plt.gnu
