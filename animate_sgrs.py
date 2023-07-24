import math
import random
from tkinter import Canvas, Tk, mainloop
from scipy.special import erfinv, erf

pixel_per_degrees = 3
canvas_width = 360 * pixel_per_degrees
canvas_height = 180 * pixel_per_degrees
framespersec = 24
rate_sgr = 5 #days
time_scale = 365.25 #days
filmtime = 60

def make_sstars(n_stars_milkyway, n_stars_spreadout):
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
        center = (x, y)

        thin_poles = random.random()
        if coslat > (thin_poles):
            static_star_list.append((x, y))

        #Creates stars that are spread all around the screen
    for i in range(n_stars_spreadout):

        longitude = -random.uniform(-180,180)
        latitude = random.uniform(-90, 90)
        
        coslat = math.cos( latitude * math.pi /180 )
        y = (90 - latitude) * pixel_per_degrees
        x = (( longitude * coslat) + 180 ) * pixel_per_degrees
        thin_poles = random.random()
        center = (x, y)
        if coslat > thin_poles:
            static_star_list.append((x, y))
               
    return static_star_list

static_star_list = make_sstars(4000, 500)
    
def main():
    #
    root = Tk()
    w = Canvas(root,
               width=canvas_width,
               height=canvas_height,
               bg = 'black')
    w.pack()
    ##define a time parameter for the universe
    time_param = 0
    draw_stars(w, static_star_list, 1, 'blue')
    SGR_list = make_SGRs(1)
    print('SGRs:', SGR_list)
    #initial drawing of SGRs
    draw_SGRs(w, SGR_list, 'white', time_param)
    #now kick off the animation
    root.after(1000 // framespersec, update_sky, root, w, SGR_list, time_param)
    mainloop()


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
        frequency_mean = 50
        frequency_range = 1
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

def draw_stars(w, stars, radius, color):
    """Draw fixed stars on the canvas"""
    for center in stars:
            w.create_oval(center[0]-radius, center[1]-radius,
                          center[0]+radius, center[1]+radius,
                          fill=color)

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
            ##all the other times loop runs
               
               #countdown = period_sec * framespersec
              # w.itemconfig(canvas_id, state = 'normal')
               
        #else:
         #      w.itemconfig(canvas_id, state =  'hidden')
          #     countdown -= 1
          ##nonw we are done updating all the state informatin
          ## it back into the sgr list
        sgr = (x, y, period_sec, countdown, canvas_id, Amp, frequency, tow)
        stars[i] = sgr

def next_sgr(rate, period_of_time):
    simple_ran = random.uniform(0, period_of_time)
    if simple_ran <= rate:
        return True
    else:
        return False

def update_sky(the_root, w, SGRs, time_param):
    w.delete('all')
    """Draws the Changing parts of the sky -- mostly the SGRs."""
    print('updating...')
    draw_stars(w, static_star_list, 1, 'blue')
    Prob_of_sgr = next_sgr(rate_sgr, time_scale)
    # print('new list:', new_sgr)
    if Prob_of_sgr:
        new_sgr = make_SGRs(1)
        SGRs.extend(new_sgr)
    # print('full list:', SGRs)
    draw_SGRs(w, SGRs, 'white', time_param)
    w.update()
    the_root.after(1000 // framespersec, update_sky, the_root, w, SGRs, time_param)

if __name__ == '__main__':
    main()
