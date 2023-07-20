import math
import time
import random
from itertools import cycle
import sys
from tkinter import *
from tkinter import ttk
from scipy.special import erfinv, erf
from mesa import Agent, Model
from mesa.time import RandomActivation

#var_radius = 5 * ( 1 + math.sin(1  * frames  * srgtime))
frames = 25
srgtime = 0.5

def main():
    ## prepare a basic canvas
    root = Tk()
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height,
               bg = 'black')
    w.pack()   	# boiler-plate: we always call pack() on tk windows


class SGR:
        
  #    color = 'blue'

    def __init__(self):
        x = random.randint(0, canvas_width)
        y = random.randint(0, canvas_height)
        self.pulse(x, y)

   # def create(xcor, ycor):
        
    def pulse(xcor, ycor):
        for i in range (20):
            center = [(xcor, ycor)]
            frames = 25
            var_radius = 5 * ( 1 + math.sin(i  * 25  * srgtime))
            w.create_oval(center[0]-var_radius, center[1]-var_radius,
                          center[0]+var_radius, center[1]+var_radius,
                          fill=color)
            w.update()
        root.after(40, self.pulse())


Origin = SGR()

root.after(10000,lambda: root.destroy())
        
        ## update the canvas
   # mainloop()
   
main()
