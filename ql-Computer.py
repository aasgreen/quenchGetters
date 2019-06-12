# -*- coding: utf-8 -*-


'''This program, when an arduino is connected, will log the measurement'''
import matplotlib as mpl

mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
FigureCanvasTkAgg= mpl.backends.backend_tkagg.FigureCanvasTkAgg

import tkinter as tk
#import serial
#import select
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
writeIndex=0
writeVolt = False
qlogV = []

class App_Window(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.framePlot = tk.Frame(self.parent)
        tk.Frame.__init__(self.parent)
        self.initialize()
    def close(self):
        self.parent.destroy()
        sys.exit()

    def initialize(self):
        self.display_p = 0.0
        self.current_set_p = 0.0
        self.pLabel = tk.Label(self.frame, text='P_S')
        self.pLabel.grid(row=0,column=0)
        self.sp = tk.Label(self.frame,text=self.current_set_p)
        self.sp.grid(row=0,column=1)
        self.setP = tk.Entry(self.frame)
        self.setP.focus()
        self.setP.bind("<Return>",self.returnEntry)
        self.setP.grid(row=1,column=0)
        self.set_p_button = tk.Button(self.frame,text='set pressure',command=self.returnEntry)
        self.set_p_button.grid(row=1,column=1)
        self.currentPlabel = tk.Label(self.frame,text='p:')
        self.currentPlabel.grid(row=2,column=0)
        self.currentPlabelValue = tk.Label(self.frame,text='test')
        self.currentPlabelValue.grid(row=2,column=1)
        self.exit_button = tk.Button(self.frame,text='exit',command=self.close)
        self.exit_button.grid(row=3)
        self.frame.pack()

     
        self.canvasFig = mpl.figure.Figure()
        self.FigureSubPlot = self.canvasFig.add_subplot(111)
        self.FigureSubPlot.plot(np.sin(np.linspace(0,100)))
        self.canvasMain = FigureCanvasTkAgg(self.canvasFig,self.frame)
        self.canvasMain.show()
        self.canvasMain.get_tk_widget().pack()
#        self.exit_button2.pack()
        self.framePlot.pack()

        self.framePlot.pack()
    def returnEntry(self):
        print('test1')
        #self.current_set_p=self.setP.get()
        result=self.setP.get()
        print(self.current_set_p)
        self.sp['text']=result
       # self.setP.delete(0,END)
        print('test')

root = tk.Tk()
    
MainWindow=App_Window(root)
root.mainloop()
