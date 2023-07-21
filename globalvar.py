#All of import statements
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

canvas_width = 360
canvas_height = 180
frames = 25
srgtime = 0.5
loop_start = 1

def main():
    ## prepare a basic canvas
    root = Tk()
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height,
               bg = 'black')
    w.pack()   	# boiler-plate: we always call pack() on tk windows

    def radius():
        global loop_start
        loop_start += 1
        Radius = 5 * ( 1 + math.sin(loop_start * frames  * srgtime))
        return Radius

    def next_event(rate, period_of_time):
        mm = rate / period_of_time
        R1 = random.random()
        t1 = timeoflastevent -( math.log(1 - R1)) / mm
        timeprinted = t1 / period_of_time * (filmtime * filmwaitunits)
        #want to later change code and add on the time of the last
        #event to he new equation so the time of last event is added
        #to time of next event timeoflastevent = curently is set to 0
        #time.sleep makes whole code stop which is bad
    #    time.sleep(timeprinted)
        
        #next three lines of code only work if definition is inside main loop
        round_time = round(timeprinted, 3)
        #time_ml = round_time * 1000
        root.after(int(round_time) * 1000), new_srg())

    def new_sgr():
        canvas_id = SGR(w)
        next_event()
        #time.sleep makes whole code stop which is bad
        #time.sleep(timeprinted)
        
        #next three lines of code only work if definition is inside main loop
        #round_time = round(timeprinted, 3)
        #time_ml = round_time * 1000
        #root.after(int(round_time * 1000), new_srg)


    class SGR:
        
        def __init__(self, canvas):
            loop_num = 0
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            self.pulse(x, y)
            
            # def create(xcor, ycor):
            
        def pulse(self, xcor, ycor):
            color = 'blue'
            center = [xcor, ycor]
            frames = 25
            var_radius = radius()
            w.create_oval(center[0]-var_radius, center[1]-var_radius,
                          center[0]+var_radius, center[1]+var_radius,
                          fill=color)
            x = xcor
            y = ycor
            w.update()
            root.after(1000, self.pulse(x, y))

        
    
        #Origin = SGR(w)

#root.after(10000,lambda: root.destroy())
        
        ## update the canvas
   # mainloop()
   
main()
