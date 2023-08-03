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
    file_menu.add_command(label="new...", command = main)
    file_menu.add_separator()
    file_menu.add_command(label="Static Sky", command = set_up_ss)
    file_menu.add_separator()
    file_menu.add_command(label="Visiable Flare", command = set_up_flare)
    file_menu.add_separator()
    file_menu.add_command(label="X-ray Sky", command = my_xray_sky)
    file_menu.add_separator()
    file_menu.add_command(label="Clear Sky", command = clear_all)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command = root.quit)
    
    mainloop()


#Clear all stars out of sky
def clear_all():
    w.delete('all')

##### Static Skys 

#Universal Code
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

## Not in use

def update_sky(the_root, w, SGRs, time_param):
    """Draws the Changing parts of the sky -- mostly the SGRs."""
    print('updating...')
    draw_SGRs(w, SGRs, 5, 'white', time_param)
    w.update()
    the_root.after(1000 // framespersec, update_sky, the_root, w, time_param)
    #the_root.after(1000 // framespersec, update_sky, the_root, w, SGRs, time_param)


##### All the code for all X-ray Skys

def my_xray_sky():
    """starts all of the code sets everything up. Update sky is the
    continuse loop that continues to update everython for 60 seconds"""

    ##define a time parameter for the universe
    time_param = time.time()
    print('time start:', time_param)
    
    draw_x_stars(w, xray_stars, 'white')
    draw_pulsars(w, pulsar_list, 'blue', time_param)
    
    #time for next sgr
    next_sgr = next(time_iter)
    #print(static_star_list)
    SGR_list = make_SGRs(1)
    #####print('SGRs:', SGR_list)
    #initial drawing of SGRs
    draw_SGRs(w, SGR_list, 'white', time_param)
    
    #now kick off the animation
    root.after(1000 // framespersec, update_x_sky, root, w, SGR_list, pulsar_list, time_param, next_sgr)

def time_list(rate, period_of_time):
    next_event = []
    while sum(next_event) < filmtime * 1000:
        mm = rate / period_of_time
        R1 = random.random()
        #gives you a result in days
        t1 =  -( math.log(1 - R1)) / mm
        #gives you the result converted to scale of film (365 days in
        #milliseconds)
        timeprinted = (t1 / period_of_time) * (filmtime * 1000)
        next_event.append(timeprinted)
    print('sgr appear times:', next_event)
    return next_event

time_iter = time_list(rate_sgr, time_scale)


def make_xray_sstars(n_stars_milkyway, n_stars_spreadout, n_stars_center):
    """Creates regular static stars background"""
    
    """Stars centered around the galatic center"""
    static_star_list = []
    for i in range(n_stars_milkyway):
        #time_iter = iter(time_till_next_srg)

        longitude = random.uniform(-180,180)
        ranlat = random.uniform(-1, 1)
        latitude = erfinv(ranlat) * 5
        #latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi / 180)
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees

        M_min = 4.5
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

        M_min = 4.5
        alpha = 3.5
        ranB = random.random()
        brightness = (M_min * (1 - ranB)) ** (-1/(-alpha + 1))

        thin_poles = random.random()

        if coslat > thin_poles:
            static_star_list.append((x, y, brightness))
    num = 1
    """Creates stars at the galatic center"""
    for i in range(n_stars_center):
        longitude = 0
        latitude = 0
        coslat = math.cos( latitude * math.pi /180 )
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees
        brightness = 20
        static_star_list.append((x, y, brightness))      
               
    return static_star_list


xray_stars = make_xray_sstars(100, 20, 1)
def make_pulsars(n_stars):
    """Create Pulsars, These are only a few and go off randomly."""
    centerlist = []
    for i in range(n_stars):
        longitude = -random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi /180 )
        puly = (90 - latitude) * pixel_per_degrees
        pulx = (( longitude * coslat) + 180 ) * pixel_per_degrees

        start_time = random.uniform(0,60) * framespersec

        period_sec = random.randint(6, 12)
        countdown = 0
        canvas_id = None # id of all object
        AMP = 0
        tow = 10
        centerlist.append((pulx, puly, period_sec, countdown, canvas_id, AMP, tow, start_time))
    return centerlist

pulsar_list = make_pulsars(5)

def make_bursters(x_stars):
    longitude = random.uniform(-180,180)
    latitude = random.uniform(-90, 90)
    coslat = math.cos( latitude * math.pi /180 )
    sgry = (90 - latitude) * pixel_per_degrees
    sgrx = (( longitude * coslat) + 180 ) * pixel_per_degrees
    
    #Calculates amplitude
    ran1 = random.uniform(-1,1)
    mean = 10 ** 5
    rnge = 10 ** 4
    Amp = ((erfinv(ran1) + mean)* rnge)

    #Calculates frequency
    ran2 = random.uniform(-1,1)
    frequency_mean = 10
    frequency_range = 0.1
    #random.randint(2,100)
    frequency = ((erfinv(ran2) + frequency_mean) * frequency_range)
    
    #Everything else
    period_sec = random.randint(6, 12)
    countdown = 0
    canvas_id = None # id of all object
    tow = 50
    
    #comple into 1 set 
    centerlist.append((sgrx, sgry, period_sec, countdown, canvas_id, Amp, frequency, tow))
    print('centerlist', centerlist)
    return centerlist    

def make_SGRs(n_stars):
    """Create SGRs, These are more elaborate than fixed stars."""
    centerlist = []
    for i in range(n_stars):
        #lat and long
        longitude = random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi /180 )
        sgry = (90 - latitude) * pixel_per_degrees
        sgrx = (( longitude * coslat) + 180 ) * pixel_per_degrees

        #Calculates amplitude
        ran1 = random.uniform(-1,1)
        mean = 10 ** 5
        rnge = 10 ** 4
        Amp = ((erfinv(ran1) + mean)* rnge)

        #Calculates frequency
        ran2 = random.uniform(-1,1)
        frequency_mean = 10
        frequency_range = 0.1
        #random.randint(2,100)
        frequency = ((erfinv(ran2) + frequency_mean) * frequency_range)

        #Everything else
        period_sec = random.randint(6, 12)
        countdown = 0
        canvas_id = None # id of all object
        tow = 50
        
        #comple into 1 set 
        centerlist.append((sgrx, sgry, period_sec, countdown, canvas_id, Amp, frequency, tow))
        print('centerlist', centerlist)
    return centerlist    

def draw_x_stars(w, stars, color):
    """Draw fixed stars on the canvas"""
    for center in stars:
            w.create_oval(center[0]-center[2], center[1]-center[2],
                          center[0]+center[2], center[1]+center[2],
                          fill=color)
def draw_pulsars(w, pulsars, color, time_param):
    """Draw the SGRs. This has some interesting behaviors: and Sgr may
    have never been drawn before, so we might need to acivate it ad we
    might need to light it up of dim it."""

    for i, pulsar in enumerate(pulsars):
        [x, y, period_sec, countdown, canvas_id, Amp, tow, start_time] = pulsar
        # countdown can be -1 (if we never enter this function
        # beforeor 0 if we nee to do a falash or greater than 0 if we
        # are quite
        """Draw the SGRs. This has some interesting behaviors: and Sgr may
        have never been drawn before, so we might need to acivate it ad we
        might need to light it up of dim it."""
        if start_time > 0:
            start_time -=1
            ran1 = random.uniform(-1,1)
            mean = 10 ** 3
            rnge = 10 ** 2
            Amp = ((erfinv(ran1) + mean)* rnge)


        elif countdown >= 0:
            center = [x, y]
            decay = countdown - 0 / .1
            size = Amp * (1 + math.sin(2 * math.pi * decay))/2
            decay_size = size * math.exp (-decay/tow) /100
            print('ds', decay_size)
            var_radius = decay_size
            canvas_id = w.create_oval(center[0]-var_radius, center[1]-var_radius,
                                      center[0]+var_radius, center[1]+var_radius,
                                      fill=color)
            w.itemconfig(canvas_id, state='normal')
            countdown += 1
            if var_radius <= 0.001:
                #correlation between the amplitude of the burst and
                #the time untill the next burst
                start_time += Amp * random.uniform(0, 1440) / 1000
                countdown -= countdown

        elif countdown < 0:
            print('negitive countdown')
        
        pulsar = (x, y, period_sec, countdown, canvas_id, Amp, tow, start_time)
        print(pulsar)
        pulsars[i] = pulsar

def draw_SGRs(w, stars, color, time_param):
    """Draw the SGRs. This has some interesting behaviors: and Sgr may
    have never been drawn before, so we might need to acivate it ad we
    might need to light it up of dim it."""

    for i, sgr in enumerate(stars):
        [x, y, period_sec, countdown, canvas_id, Amp, frequency, tow] = sgr
        # countdown can be -1 (if we never enter this function
        # beforeor 0 if we nee to do a falash or greater than 0 if we
        # are quite
        if countdown >= 0:
            ##first time for this one -we have to creat oval
            center = [x, y]
            decay = countdown - 0 / .1
            size = Amp * (1 + math.sin(2 * math.pi * frequency * decay))/2
            decay_size = size * math.exp (-decay/tow) /1000000
            var_radius = decay_size
            canvas_id = w.create_oval(center[0]-var_radius, center[1]-var_radius,
                                      center[0]+var_radius, center[1]+var_radius,
                                      fill=color)
            w.itemconfig(canvas_id, state='normal')
            countdown += 1
        elif countdown < 0:
            print('negitive countdown')
            #countdown = period_sec * framespersec
            # w.itemconfig(canvas_id, state = 'normal')
            
        #else:
        #      w.itemconfig(canvas_id, state =  'hidden')
        #     countdown -= 1
        #now we are done updating all the state informatin
        #and sending it back into the sgr list
        sgr = (x, y, period_sec, countdown, canvas_id, Amp, frequency, tow)
        stars[i] = sgr

def update_x_sky(the_root, w, SGRs, pulsars, start_time_param, next_sgr):
    w.delete('all')
    """Draws the Changing parts of the sky -- mostly the SGRs."""

    # calulates the time at which root updates then converst it to seconds
    time_param = time.time() - start_time_param
    print(time_param)
    print(next_sgr)
    
    #Check to see if it is time to create a new sgr
    if time_param * 1000 >= next_sgr:
        new_sgr = make_SGRs(1)
        SGRs.extend(new_sgr)
        print('full list:', SGRs)
        next_time = next(time_iter)
        next_sgr += next_time
        
    #updates everything 
    print('updating...')
    draw_x_stars(w, xray_stars, 'white')
    draw_SGRs(w, SGRs, 'white', time_param)
    draw_pulsars(w, pulsars, 'blue', time_param)
    
    w.update()
    if time_param >= 60:
        w.delete('all')
    else:
        the_root.after(1000 // framespersec, update_x_sky, the_root, w, SGRs, pulsars, start_time_param, next_sgr)


if __name__ == '__main__':
    main()
#things to add and ask: Whoopers steady flickering x raystars, list of x ray and sgr and supernova stars., 
