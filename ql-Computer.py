# -*- coding: utf-8 -*-


'''This program, when an arduino is connected, will log the measurement'''
import matplotlib as mpl
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
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
writeIndex=0
writeVolt = False
qlogV = []

class App_Window:
    def __init__(self,parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)
        tk.Frame.__init__(self.parent)
        self.initialize()

    def initialize(self):
        self.cMain = tk.Canvas(self.parent,width=100,height=100)
        self.display_p = 0.0
        self.current_set_p = 0.0
        self.pLabel = tk.Label(self.frame, text='P_S')
        self.pLabel.pack()
        self.sp = tk.Label(self.frame,text=self.current_set_p)
        self.sp.pack()
        self.setP = tk.Entry(self.frame,width=10)
        self.setP.focus()
        self.setP.bind("<Return>",self.returnEntry)
        self.setP.pack()
        self.set_p_button = tk.Button(self.frame,text='set pressure',command=self.returnEntry)
        self.set_p_button.pack()
        self.currentPlabel = tk.Label(self.frame,text='p:')
        self.currentPlabel.pack()
        self.currentPlabelValue = tk.Label(self.frame,text='test')
        self.currentPlabelValue.pack()
        self.frame.pack()
        self.sp.config(text='test2')

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
