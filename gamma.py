import time
import math
import random
from itertools import cycle
import sys

## we use the tkinter widget set; this seems to come automatically
## with python3 on ubuntu 16.04, but on some systems one might need to
## install a package with a name like python3-tk
from tkinter import *
from tkinter import ttk
from scipy.special import erfinv, erf

#sets the canvas width and hight but keep in mind that the stars are
#not proportional to the night sky they won't get biger with the
#screen for smaller
canvas_width = 360 * 3
canvas_height = 180 * 3
#the code for the proporttings of the milky way
milkyway = canvas_height / 2

#additional code for a list. iter returns the next value of the code.
l = [1, 2, 3]
l_iter = iter(l)
#the frames of the code and how long it takes a gama ray to repeat
#needs to be a function. how long sgrlasts is how long th loop lasts
#about seconds. Why 60 =
frames = 25
srgtime = 0.5

#for wait time
default_rate = 50.3
one_year = 365.25
filmtime = 60
filmwaitunits = 1
timeoflastevent = 0

#creates 1000 regular static stars. then apends adding 1000 values to the list.
def sstars():
        static_star_list = []

        for i in range(10000):
         x = random.randint(0, canvas_width)
         ranlat = random.uniform(-1, 1)
         y = erfinv(ranlat) * 40 + milkyway
         radius = (10)
         center = (x, y)
         color = ("white")
         static_star_list.append((x, y))

        for i in range(1000):
         x = random.randint(0, canvas_width)
         y = random.randint(0, canvas_height)
         radius = (10)
         center = (x, y)
         color = ("white")
         static_star_list.append((x, y))

        return static_star_list

def next_event(rate, period_of_time):
        mm = rate / period_of_time
        R1 = random.random()
        t1 = timeoflastevent -( math.log(1 - R1)) / mm
        timeprinted = t1 / period_of_time * (filmtime * filmwaitunits)
        #want to later change code and add on the time of the last event to he new equation so the time of last event is added to time of next event
        #timeoflastevent =   curently is set to 0

        #time.sleep makes whole code stop which is bad
        time.sleep(timeprinted)
        
        #next three lines of code only work if definition is inside main loop
        #round_time = round(timeprinted, 3)
        #time_ml = round_time * 1000
        #root.after(int(round_time * 1000), new_srg)
  
        
def main():
    ## prepare a basic canvas
    root = Tk()
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height,
               bg = 'black')
    w.pack()   	# boiler-plate: we always call pack() on tk windows
    static_star_list = sstars() # generate these just once
    for i in range(25*180): 	# 3 minutes if it's 24 frames/sec
        w.delete('all')
  
        ## clear the canvas and then draw the new state
        color = 'blue'
        #Where Will the srg happen?????
        
        srgx = random.randint(0,canvas_width)
        srgy = random.randint(0,canvas_height)
        # first draw the static stars
        fixed_radius = 1

        for center in static_star_list:
            w.create_oval(center[0]-fixed_radius, center[1]-fixed_radius,
                          center[0]+fixed_radius, center[1]+fixed_radius,
                          fill=color)
        #w.update()    
        
        
        # When will srg happen
        next_event(default_rate, one_year)
        # then  draw the dynamic star
        
        #Calculates amplitude
        ran1 = random.uniform(-1,1)
        mean = 10 ** 5
        rnge = 10 ** 4
        Amp = ((erfinv(ran1) + mean)* rnge)


        #Calculates frequency
        ran2 = random.uniform(-1,1)
        frequency_mean = 50
        frequency_range = 1
        #random.randint(2,100)
        frequency = ((erfinv(ran2) + frequency_mean) * frequency_range)

        mytow = 50
        def howlongsgrlasts():
                return 180

        for i in range(howlongsgrlasts()):
                w.delete('all')
                center = (srgx, srgy)
                #need to add an equation for the aplitude right before
                #perenthisis.
                decay = i - 0 / .1
                rounded_num = round(1)
                size = Amp * (1 + math.sin(2 * math.pi * frequency * decay))/2
                decay_size = size * math.exp (-decay/mytow) /1000000
                var_radius = decay_size
                w.create_oval(center[0]-var_radius, center[1]-var_radius,
                              center[0]+var_radius, center[1]+var_radius,
                              fill=color)
                w.update()
                time.sleep(1/5)
                #update_time = (1/25 * 1000)
                #time.sleep(decay_size/Amp/(1+math.sin))
                #root.after(int(decay_size/Amp/(1+math.sin)), root.update())    
        
        root.after(10000,lambda: root.destroy())
        
        ## update the canvas
    mainloop()
   
main()
