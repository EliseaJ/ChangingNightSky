from tkinter import *
import math
import random
from scipy.special import erfinv, erf
import time

###root = Tk()

pixel_per_degrees = 3
canvas_width = 360 * pixel_per_degrees
canvas_height = 180 * pixel_per_degrees
framespersec = 24
rate_sgr = 5 #days
time_scale = 365.25 #days
filmtime = 60
flare_radius = 1

def make_sstars(n_stars_milkyway, n_stars_spreadout, n_stars_center):
    """Creates regular static stars background"""
    
    """Stars centered around the galatic center"""
    static_star_list = []
    for i in range(n_stars_milkyway):

        longitude = random.uniform(-180,180)
        ranlat = random.uniform(-1, 1)
        latitude = erfinv(ranlat) * 5
        #latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi / 180)
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees

        M_min = 2.5
        alpha = 3.5
        ranB = random.random()
        brightness = (M_min * (1 - ranB)) ** (-1/(-alpha + 1))

        thin_poles = random.random()

        if coslat > (thin_poles):
            static_star_list.append((x, y, brightness))

    """Creates stars that are spread all around the screen"""
    for i in range(n_stars_spreadout):

        longitude = -random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi /180 )
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees

        M_min = 2.5
        alpha = 3.5
        ranB = random.random()
        brightness = (M_min * (1 - ranB)) ** (-1/(-alpha + 1))

        thin_poles = random.random()

        if coslat > thin_poles:
            static_star_list.append((x, y, brightness))
    num = 1
    """Creates stars at the galatic center"""
    for i in range(n_stars_center):
        ranlong = random.uniform(-1, 1)
        longitude = erfinv(ranlat) * 10
        ranlat = random.uniform(-1, 1)
        latitude = erfinv(ranlat) * 10
        coslat = math.cos( latitude * math.pi /180 )
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees

        M_min = 2.5
        alpha = 3.5
        ranB = random.random()
        brightness = (M_min * (1 - ranB)) ** (-1/(-alpha + 1))

        rate_of_thining = 1
        thin_poles = random.random() * rate_of_thining
        if coslat > thin_poles:
            #print('yay', num, x, y)
            num += 1
            static_star_list.append((x, y, brightness))

    return static_star_list

static_star_list = make_sstars(4000, 500, 1000)


root = Tk()
w = Canvas(root,
           width=canvas_width,
           height=canvas_height,
           bg = 'black')

def our_command():
    pass
    

def main():
    my_menu = Menu(root)
    root.config(menu=my_menu)
    w.pack()

    #Make Tk menue
    file_menu = Menu(my_menu)
    my_menu.add_cascade(label="Pick a Sky", menu=file_menu)
    file_menu.add_command(label="new...", command = our_command)
    file_menu.add_separator()
    file_menu.add_command(label="Static Sky", command = set_up_ss)
    file_menu.add_separator()
    file_menu.add_command(label="Visiable Flare", command = set_up_flare)
    file_menu.add_separator()
    
    file_menu.add_command(label="Exit", command = root.quit)
    
    mainloop()

#Universal Code
def draw_stars(w, stars, color):
    """Draw fixed stars on the canvas"""
    for center in stars:
            w.create_oval(center[0]-center[2], center[1]-center[2],
                          center[0]+center[2], center[1]+center[2],
                          fill=color)
   
#All static sky code
def set_up_ss():
    flare_radius = 1
    ##define a time parameter for the universe
    time_param = 0
    start_time = time.time()
    print('time start:', time_param)
    draw_stars(w, static_star_list, 'white')
    #time for next sgr
    #next_sgr = next(time_iter)
    #print(static_star_list)
    flare_list = make_flare()
    #####print('SGRs:', SGR_list)
    #initial drawing of SGRs
    draw_flare(w, flare_list, flare_radius, 'white', time_param)
    #now kick off the animation
    root.after(1000 // framespersec, update_static_sky, root, w, flare_list, time_param, start_time, flare_radius)

#visiable flare star
def set_up_flare():
    flare_radius = 10
    ##define a time parameter for the universe
    time_param = 0
    start_time = time.time()
    print('time start:', time_param)
    draw_stars(w, static_star_list, 'white')
    #time for next sgr
    #next_sgr = next(time_iter)
    #print(static_star_list)
    flare_list = make_flare()
    #####print('SGRs:', SGR_list)
    #initial drawing of SGRs
    draw_flare(w, flare_list, flare_radius, 'white', time_param)
    #now kick off the animation
    root.after(1000 // framespersec, update_static_sky, root, w, flare_list, time_param, start_time, flare_radius)

def make_flare():
    """Create SGRs, These are more elaborate than fixed stars."""
    centerlist = []
    for i in range(1):
        longitude = -100
        latitude = 30
        coslat = math.cos( latitude * math.pi /180 )
        sgry = (90 - latitude) * pixel_per_degrees
        sgrx = (( longitude * coslat) + 180 ) * pixel_per_degrees

        countdown = -1
        canvas_id = None # id of all object
        centerlist.append((sgrx, sgry, countdown, canvas_id))
    return centerlist

def draw_flare(w, stars, radius, color, time_param):
    """Draw the SGRs. This has some interesting behaviors: and Sgr may
    have never been drawn before, so we might need to acivate it ad we
    might need to light it up of dim it."""

    for i, sgr in enumerate(stars):
        [x, y, countdown, canvas_id] = sgr
        # countdown can be -1 (if we never enter this function
        # beforeor 0 if we nee to do a falash or greater than 0 if we
        # are quite
        if countdown == -1:
            ##first time for this one -we have to creat oval
            canvas_id = w.create_oval(x-radius, y-radius,
                                      x+radius, y+radius,
                                      fill=color)
            countdown += 1
        elif countdown == 0:
            print('wee')
            my_rad = radius + (radius/10) 
            canvas_id = w.create_oval(x-my_rad, y-my_rad,
                                      x+my_rad, y+my_rad,
                                      fill=color)
            flare_frequency = time_scale * 1.5 // framespersec
            random_next = random.randint(0, flare_frequency)
            countdown = random_next
            
        else:
            canvas_id = w.create_oval(x-radius, y-radius,
                                      x+radius, y+radius,
                                      fill=color)
            
            countdown -= 1
            ##nonw we are done updating all the state informatin
            ## it back into the sgr list
        sgr = [x, y, countdown, canvas_id]
        print(sgr)
        stars[i] = sgr

def update_static_sky(the_root, w, SGRs, time_param, start_time, flare_radius):
    """Draws the Changing parts of the sky -- mostly the SGRs."""
    w.delete('all')
    # calulates the time at which root updates then converst it to seconds
    #time.time() - start_time_param
    print(time_param)
    my_time = start_time - time.time()
    #updates everything 
    print('updating...')
    #draw_stars(w, static_star_list, 'white')
    draw_stars(w, static_star_list, 'white')
    draw_flare(w, SGRs, flare_radius, 'white', time_param)
    w.update()
    #if time_param >= 60:
    #   the_root.destroy()
    time_param += 1/framespersec
    if my_time >= 60:
        w.delete('all')
    else:
        the_root.after(1000 // framespersec, update_static_sky, the_root, w, SGRs, time_param, start_time, flare_radius)



def update_sky(the_root, w, SGRs, time_param):
    """Draws the Changing parts of the sky -- mostly the SGRs."""
    print('updating...')
    draw_SGRs(w, SGRs, 5, 'white', time_param)
    w.update()
    the_root.after(1000 // framespersec, update_sky, the_root, w, time_param)
    #the_root.after(1000 // framespersec, update_sky, the_root, w, SGRs, time_param)

if __name__ == '__main__':
    main()
