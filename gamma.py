import time
import math
import random
from tkinter import Canvas, Tk, mainloop
from scipy.special import erfinv, erf

random.seed(6)

pixel_per_degrees = 3
canvas_width = 360 * pixel_per_degrees
canvas_height = 180 * pixel_per_degrees
framespersec = 24
rate_sgr = 5 #days
time_scale = 365.25 #days
filmtime = 60


Big_list = [('Sco X-1', 359.094173, 23.784398, 2800, 8, (2 * (10 ** 38))),
            ('4U 1543-475', 330.917895, 5.426286, 4000, 8,( 7 * (10 **38)))]

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

time_till_next_srg = time_list(rate_sgr, time_scale)

time_iter = iter(time_till_next_srg)

def make_xray_sstars(n_stars_milkyway, n_stars_spreadout, n_stars_center):
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
    centerlist = []
    for i in range(n_stars):

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
        frequency_mean = 1
        frequency_range = 1
        #random.randint(2,100)
        frequency = ((erfinv(ran2) + frequency_mean) * frequency_range)
        if frequency <=0:
            pass
        #Everything else
        period_sec = random.randint(6, 12)
        countdown = 0
        canvas_id = None # id of all object
        tow = 10000
    
        #comple into 1 set 
        centerlist.append((sgrx, sgry, period_sec, countdown, canvas_id, Amp, frequency, tow))
    print('pulsars', centerlist)
    return centerlist    

pulsar_list = make_pulsars(4)

def make_bursters(n_stars):
    """Create Pulsars, These are only a few and go off randomly."""
    centerlist = []
    for i in range(n_stars):
        longitude = -random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        coslat = math.cos( latitude * math.pi /180 )
        puly = (90 - latitude) * pixel_per_degrees
        pulx = (( longitude * coslat) + 180 ) * pixel_per_degrees

        start_time = random.uniform(0,60) * framespersec
        M_min = 4.5
        alpha = 3.5
        ranB = random.random()
        brightness = (M_min * (1 - ranB)) ** (-1/(-alpha + 1))

        standard = brightness * 2 
        period_sec = random.randint(6, 12)
        countdown = 0
        canvas_id = None # id of all object
        AMP = 0
        tow = 10
        centerlist.append((pulx, puly, period_sec, countdown, canvas_id, AMP, tow, start_time, standard))
    return centerlist

burster_list = make_bursters(5)

def main():
    """starts all of the code sets everything up. Update sky is the
    continuse loop that continues to update everython for 60 seconds"""
    root = Tk()
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height,
               bg = 'black')
    w.pack()
    
    ##define a time parameter for the universe
    time_param = time.time()
    print('time start:', time_param)
    
    draw_stars(w, xray_stars, 'white')
    draw_bursters(w, burster_list, 'white', time_param)
    
    #time for next sgr
    next_sgr = next(time_iter)
    #print(static_star_list)
    SGR_list = make_SGRs(1)
    #####print('SGRs:', SGR_list)
    #initial drawing of SGRs
    draw_SGRs(w, SGR_list, 'white', time_param)
    draw_pulsars(w, pulsar_list, 'white', time_param)
    #now kick off the animation
    root.after(1000 // framespersec, update_x_sky, root, w, SGR_list, burster_list, time_param, next_sgr)
    mainloop()


def draw_pulsars(w, pulsars, color, time_param):
    """Draw the SGRs. This has some interesting behaviors: and Sgr may
    have never been drawn before, so we might need to acivate it ad we
    might need to light it up of dim it."""

    for i, pul in enumerate(pulsars):
        [x, y, period_sec, countdown, canvas_id, Amp, frequency, tow] = pul
        # countdown can be -1 (if we never enter this function
        # beforeor 0 if we nee to do a falash or greater than 0 if we
        # are quite
        if countdown >= 0:
            ##first time for this one -we have to creat oval
            center = [x, y]
            decay = countdown - 0 / .1
            size = Amp * (1 + math.sin(2 * math.pi * frequency * decay))/2
            decay_size = size /10000000 + 1
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
        pul = (x, y, period_sec, countdown, canvas_id, Amp, frequency, tow)
        pulsars[i] = pul


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

def draw_stars(w, stars, color):
    """Draw fixed stars on the canvas"""
    for center in stars:
            w.create_oval(center[0]-center[2], center[1]-center[2],
                          center[0]+center[2], center[1]+center[2],
                          fill=color)
def draw_bursters(w, bursters, color, time_param):
    """Draw the SGRs. This has some interesting behaviors: and Sgr may
    have never been drawn before, so we might need to acivate it ad we
    might need to light it up of dim it."""

    for i, burster in enumerate(bursters):
        [x, y, period_sec, countdown, canvas_id, Amp, tow, start_time, standard] = burster
        # countdown can be -1 (if we never enter this function
        # beforeor 0 if we nee to do a falash or greater than 0 if we
        # are quite
        """Draw the SGRs. This has some interesting behaviors: and Sgr may
        have never been drawn before, so we might need to acivate it ad we
        might need to light it up of dim it."""
        if start_time > 0:
            center = [x, y]
            start_time -=1
            ran1 = random.uniform(-1,1)
            mean = 10 ** 3
            rnge = 10 ** 2
            Amp = ((erfinv(ran1) + mean)* rnge)
            var_radius = standard
            canvas_id = w.create_oval(center[0]-var_radius, center[1]-var_radius,
                                      center[0]+var_radius, center[1]+var_radius,
                                      fill=color)
            w.itemconfig(canvas_id, state='normal')

        elif countdown >= 0:
            center = [x, y]
            decay = countdown - 0 / .1
            size = Amp * (1 + math.sin(2 * math.pi * decay))/2
            decay_size = (size * math.exp (-decay/tow) /1000) + standard
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
                start_time += Amp * random.uniform(0, framespersec) / 1000
                countdown = 0

        elif countdown < 0:
            print('negitive countdown')
        
        burster = (x, y, period_sec, countdown, canvas_id, Amp, tow, start_time, standard)
        print(burster)
        bursters[i] = burster

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

def update_x_sky(the_root, w, SGRs, bursters, start_time_param, next_sgr):
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
    draw_stars(w, xray_stars, 'white')
    draw_bursters(w, bursters, 'white', time_param)
    draw_pulsars(w, pulsar_list, 'white', time_param)
    draw_SGRs(w, SGRs, 'white', time_param)
    w.update()
    if time_param >= 60:
        w.delete('all')
    else:
        the_root.after(1000 // framespersec, update_x_sky, the_root, w, SGRs, bursters, start_time_param, next_sgr)

if __name__ == '__main__':
    main()
#things to add and ask: Whoopers steady flickering x raystars, list of x ray and sgr and supernova stars., 
