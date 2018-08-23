#! /usr/bin/env python
# R E T R O  C L O C K by mozcelikors
# based on Digital Clock by HorlogeNumerique

import os, sys, pygame
from pygame.locals import *
import datetime
from subprocess import *

#weather-api
from weather import Weather, Unit

base_dir = '/home/pi/retro-clock/'
animation_folder = "frames/"
animations = ["frame1.png", "frame2.png", "frame3.png", "frame4.png", "frame5.png", "frame6.png", "frame7.png", "frame8.png", "frame9.png", "frame10.png", "frame11.png", "frame12.png", "frame13.png", "frame14.png", "frame15.png", "frame16.png", "frame17.png", "frame18.png", "frame19.png", "frame20.png", "frame21.png", "frame22.png", "frame23.png", "frame24.png", "frame25.png", "frame26.png", "frame27.png", "frame28.png", "frame29.png", "frame30.png", "frame31.png", "frame32.png", "frame33.png", "frame34.png", "frame35.png", "frame36.png", "frame37.png"]

# Counters for timing & scheduling
i=0 # animation frame counter
k=0 # one cycle counter
w=0 # weather refresh counter

# Weather variables
city = 'IZMIR'
temperature = "N/A"
weathercondition = " "

def main():
    global i
    global k
    global w
    global temperature
    global weathercondition

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
    try:
        weather = Weather (unit=Unit.CELSIUS)
        location = weather.lookup_by_location(city)
        condition = location.condition
        temperature = condition.temp
        weathercondition = condition.text
        print (temperature)
        print (weathercondition)
    except Exception as err:
        temperature = "N/A"
        weathercondition = " "
        print (err)
   
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0

    fontcolor = 128, 214, 255
    fontcolor2 = 255, 227, 89
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




        # Weather info - get every 1 weather cycle
        if (w==0):
            try:
                weather = Weather (unit=Unit.CELSIUS)
                location = weather.lookup_by_location(city)
                condition = location.condition
                temperature = condition.temp
                weathercondition = condition.text
                print (temperature)
                print (weathercondition)
            except Exception as err:
                print (err)
                temperature = "N/A"
                weathercondition = " "

        now = datetime.datetime.today()

        date = now.strftime("%d %b %Y")
        secPython = float(str(now)[17:26])


        dt = str(now - delta)
        clock = dt[11:19]

        animation = pygame.image.load (base_dir + animation_folder + animations[i])
        screen.blit (animation, [0,0])

        if temperature == "N/A":
            # Connection lost logo, if connection is lost
            connlosticon = pygame.image.load (base_dir + "connlost.png")
            screen.blit(connlosticon,[20, 30])


        # Animation timer
        if i>35:
            i = 0
        else:
            i = i+1

        # Weather request timer
        if (w>7000):
            w = 0
        else:
            w = w + 1

        # One cycle timer
        if (k>500):
            k = 0
        else:
            k = k + 1


        if (k<200): #Clock
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", fontsize)
            fontimg = font.render(clock, 1, fontcolor)
            fontimg_rect = fontimg.get_rect(center=(1.3*width/3,4.3*height/5))
            screen.blit(fontimg, [130, 3.65*height/5])

            clockicon = pygame.image.load (base_dir + "clock.png")
            screen.blit(clockicon,[20,3.8*height/5])

        elif (k<350): #Calendar
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
            fontimg = font.render(date, 1, fontcolor)
            screen.blit(fontimg, [175, 330])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render(now.strftime("%A"), 1, fontcolor2)
            screen.blit(fontimg, [175, 400])

            calendaricon = pygame.image.load (base_dir + "calendar.png")
            screen.blit(calendaricon,[10,3.55*height/5])
             
            #Clock on corner
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 40)
            fontimg = font.render(clock, 1, fontcolor)
            screen.blit(fontimg, [610,30])
            clockicon = pygame.image.load (base_dir + "clocksmall.png")
            screen.blit(clockicon,[540,30])


        else: #Temperature
            
            tempicon = pygame.image.load (base_dir + "temp.png")
            screen.blit (tempicon, [20, 3.3*height/5])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
            cityimg = font.render (city, 1, fontcolor) 

            if temperature == "N/A":
                #If weather data is not available
                font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
                fontimg = font.render("NO WEATHER DATA" , 1, fontcolor2)
            else:
                #If weather data obtained successfully
                font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 70)
                fontimg = font.render(temperature + "\'C " + weathercondition , 1, fontcolor2)
            
            screen.blit(cityimg, [100, 320])
            screen.blit(fontimg, [100, 390])

            #Clock on corner
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 40)
            fontimg = font.render(clock, 1, fontcolor)
            screen.blit(fontimg, [610,30])
            clockicon = pygame.image.load (base_dir + "clocksmall.png")
            screen.blit(clockicon,[540,30])

            # Show weather icon if text matches and if text is short enough to display an icon
            if weathercondition == "Sunny" or weathercondition == "Mostly Sunny":
                 weathericon = pygame.image.load (base_dir + "weathericons/sunny.png")
                 if len(weathercondition) > 8:
                     screen.blit (weathericon, [590, 245])
                 else:
                     screen.blit (weathericon, [590, 3.35*height/5])
            elif weathercondition == "Cloudy" or weathercondition == "Mostly Cloudy" or weathercondition == "Partly Cloudy" or weathercondition == "Fair" or weathercondition == "Foggy" or weathercondition == "Windy" or weathercondition == "Clear" or weathercondition == "Cold":
                 weathericon = pygame.image.load (base_dir + "weathericons/cloudy.png")
                 if len(weathercondition) > 8:
                     screen.blit (weathericon, [590, 245])
                 else:
                     screen.blit (weathericon, [590, 3.35*height/5])
            elif weathercondition == "Rainy" or weathercondition == "Showers" or weathercondition == "Thundershowers" or weathercondition == "Freezing Rain" or weathercondition == "Mixed Rain and Snow":
                 weathericon = pygame.image.load (base_dir + "weathericons/rainy.png")
                 if len(weathercondition) > 8:
                     screen.blit (weathericon, [590, 245])
                 else:
                     screen.blit (weathericon, [590, 3.35*height/5])
            elif weathercondition == "Snowy" or weathercondition == "Snow" or weathercondition == "Snow Showers" or weathercondition == "Heavy Snow":
                 weathericon = pygame.image.load (base_dir + "weathericons/snowy.png")
                 if len(weathercondition) > 8:
                     screen.blit (weathericon, [590, 245])
                 else:
                     screen.blit (weathericon, [590, 3.35*height/5])

        hrm = now.strftime("%H:%M")

        # Happy new year
        if (now.strftime("%d%m") == "0101"):
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
            fontimg = font.render("HAPPY NEW YEAR!!!", 1, (255, 163, 245))
            screen.blit(fontimg, [195, 90])

            #Balloon image and animation
            if (i/15 == 0):
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,170])
            else:
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,150])

        # Welcome to a new day!
        elif ((hrm == "00:00" or hrm == "23:59" or hrm == "00:01") and temperature != "N/A"):
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
            fontimg = font.render("Welcome to a new day", 1, fontcolor2)
            screen.blit(fontimg, [100, 80])
            
            #Balloon image and animation
            if (i/15 == 0):
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,170])
            else:
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,150])

        # A new hour welcomes you!
        elif (now.strftime("%M") == "27" and temperature != "N/A"):
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
            fontimg = font.render("A new hour welcomes you", 1, fontcolor2)
            screen.blit(fontimg, [90, 90])
            
            #Balloon image and animation
            if (i/15 == 0): 
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,170])
            else: 
                balloonicon = pygame.image.load (base_dir + "balloon.png")
                screen.blit (balloonicon, [350,150])

        pygame.display.update() 
        pygame.time.delay(35)
        
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
