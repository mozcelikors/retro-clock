#! /usr/bin/env python
# R E T R O  C L O C K by mozcelikors
# based on Digital Clock by HorlogeNumerique

import os, sys, pygame
from pygame.locals import *
import datetime
from subprocess import *

#weather-api
from weather import Weather, Unit

#For animation
i = 0

base_dir = '/home/pi/retro-clock/'
animation_folder = "frames/"
animations = ["frame1.png", "frame2.png", "frame3.png", "frame4.png", "frame5.png", "frame6.png", "frame7.png", "frame8.png", "frame9.png", "frame10.png", "frame11.png", "frame12.png", "frame13.png", "frame14.png", "frame15.png", "frame16.png", "frame17.png", "frame18.png", "frame19.png", "frame20.png", "frame21.png", "frame22.png", "frame23.png", "frame24.png", "frame25.png", "frame26.png", "frame27.png", "frame28.png", "frame29.png", "frame30.png", "frame31.png", "frame32.png", "frame33.png", "frame34.png", "frame35.png", "frame36.png", "frame37.png"]

# One cycle toggling variable
k=0
w=0 # weather refresh counter

city = 'IZMIR'

def main():
    global i
    global k
    global w

    size = width, height = 800, 480
    screen = pygame.display.set_mode(size)
    pygame.display.toggle_fullscreen()
    pygame.mouse.set_visible(0)
    icon = pygame.Surface((1, 1))
    icon.set_alpha(0)
    pygame.display.set_icon(icon)

    
    pygame.display.set_caption("Retro Clock")

    pygame.init()

    #Get weather
    weather = Weather (unit=Unit.CELSIUS)
    location = weather.lookup_by_location(city)
    condition = location.condition
    print (condition.text)
    print (condition.temp)

   
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0

    fontcolor = 128, 214, 255
    fontsize = 100

    font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", fontsize)

    #commandeDate = ["date", "+%Y-%m-%d %H:%M:%S.%N"]
    commandeDate = ["date", "+%S.%N"]

    delta = datetime.timedelta(seconds = 0)

    backgroundClock = "00:00:00"
    alarm1 = "2014-08-19 22:13:00"

    while 1:

        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.MOUSEBUTTONUP:
               sys.exit(0)

        #screen.fill(black)
        # Background image
        #texture = pygame.image.load ("texture4.png")
        #screen.blit(texture, [0,0])


        # Weather info - get every 1 cycle
        if (w==0):
            weather = Weather (unit=Unit.CELSIUS)
            location = weather.lookup_by_location(city)
            condition = location.condition
            print (condition.text)
            print (condition.temp)

        now = datetime.datetime.today()

        date = now.strftime("%d %b %Y")
        secPython = float(str(now)[17:26])


        dt = str(now - delta)
        clock = dt[11:19]

        animation = pygame.image.load (base_dir + animation_folder + animations[i])
        screen.blit (animation, [0,0])
        if i>35:
            i = 0
        else:
            i = i+1

   
        if (w>5000):
            w = 0
        else:
            w = w + 1


        if (k>300):
            k = 0
        else:
            k = k + 1


        if (k<120):
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", fontsize)
            fontimg = font.render(clock, 1, fontcolor)
            fontimg_rect = fontimg.get_rect(center=(1.3*width/3,4.3*height/5))
            screen.blit(fontimg, [130, 3.65*height/5])

            clockicon = pygame.image.load (base_dir + "clock.png")
            screen.blit(clockicon,[20,3.8*height/5])

        elif (k<200):
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 90)
            fontimg = font.render(date, 1, fontcolor)
            screen.blit(fontimg, [140, 310])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render(now.strftime("%A"), 1, fontcolor)
            screen.blit(fontimg, [140, 400])

            calendaricon = pygame.image.load (base_dir + "calendar.png")
            screen.blit(calendaricon,[10,3.55*height/5])
        else:
            
            tempicon = pygame.image.load (base_dir + "temp.png")
            screen.blit (tempicon, [20, 3.3*height/5])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
            cityimg = font.render (city, 1, fontcolor) 

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
            fontimg = font.render(condition.temp + "\'C " + condition.text , 1, fontcolor)
            
            screen.blit(cityimg, [100, 320])
            screen.blit(fontimg, [100, 390])


            # Show weather icon if text matches and if text is short enough to display an icon
            if condition.text == "Sunny" :
                 weathericon = pygame.image.load (base_dir + "weathericons/sunny.png")
                 screen.blit (weathericon, [590, 3.35*height/5])
            elif condition.text == "Cloudy" or condition.text == "Windy" or condition.text == "Clear" or condition.text == "Cold":
                 weathericon = pygame.image.load (base_dir + "weathericons/cloudy.png")
                 screen.blit (weathericon, [590, 3.35*height/5])
            elif condition.text == "Rainy" or condition.text == "Showers":
                 weathericon = pygame.image.load (base_dir + "weathericons/rainy.png")
                 screen.blit (weathericon, [590, 3.35*height/5])
            elif condition.text == "Snowy" or condition.text == "Snow":
                 weathericon = pygame.image.load (base_dir + "weathericons/snowy.png")
                 screen.blit (weathericon, [590, 3.35*height/5])

        pygame.display.update() 
        pygame.time.delay(70)
        
        # Compute delta
        out=Popen(commandeDate,stdout=PIPE)
        (secUnix,serr)=out.communicate()
        delta = datetime.timedelta(seconds = int(float(secUnix) - float(secPython)))
        if alarm1 == str(now)[0:19]:
            print "Alarm"


        if alarm1 == str(now)[0:19]:
            print "Alarm"

if __name__ == '__main__': 
    main()    
