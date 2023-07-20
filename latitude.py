import time
import math
import random
from itertools import cycle
import sys

#sets the canvas width and hight but keep in mind that the stars are not proportional to the night sky they won't get biger with the screen for smaller
pixil_per_degree = 3
canvas_width = 360 * pixil_per_degree
canvas_height = 180 * pixil_per_degree
#the code for the proporttings of the milky way
milkyway = canvas_height / 2
#additional code for a list. iter returns the next value of the code.
l = [1, 2, 3]
l_iter = iter(l)
#the frames of the code and how long it takes a gama ray to repeat needs to be a function. how long sgrlasts is how long th loop lasts about seconds. Why 60 = 
frames = 25
srgtime = 0.5

#for wait time
default_rate = 5.3
one_year = 365.25
filmtime = 60
filmwaitunits = 1
timeoflastevent = 0

## we use the tkinter widget set; this seems to come automatically
## with python3 on ubuntu 16.04, but on some systems one might need to
## install a package with a name like python3-tk
from tkinter import *
from tkinter import ttk
from scipy.special import erfinv, erf
#creates  regular static stars. then apends adding values to the list.


def sstars():
    
    #Stars centered around the center
    static_star_list = []
    for i in range(4000):

        longitude = random.uniform(-180,180)
        ranlat = random.uniform(-1, 1)
        latitude = erfinv(ranlat) * 10
        #latitude = random.uniform(-90, 90)

        coslat = math.cos( latitude * math.pi / 180)
        y = (90 - latitude) * pixil_per_degree
        x = (( longitude * coslat) + 180 ) * pixil_per_degree
        center = (x, y)

        thin_poles = random.random()
        if coslat > (thin_poles):
            static_star_list.append((x, y))

        #Creates stars that are spread all around the screen
    for i in range(500):

        longitude = -random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        
        coslat = math.cos( latitude * math.pi /180 )
        y = (90 - latitude) * pixil_per_degree
        x = (( longitude * coslat) + 180 ) * pixil_per_degree
        thin_poles = random.random()
        center = (x, y)
        if coslat > thin_poles:
            static_star_list.append((x, y))
            
    return static_star_list


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
        w.update()    
        
                
        root.after(10000,lambda: root.destroy())
        ## update the canvas
    mainloop()
   
main()
