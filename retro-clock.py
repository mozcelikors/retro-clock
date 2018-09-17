#! /usr/bin/env python
# R E T R O  C L O C K by mozcelikors
# based on Digital Clock by HorlogeNumerique

import os, sys, pygame
from pygame.locals import *
import datetime
from subprocess import *
import threading

#forex-python currency api
from forex_python.converter import CurrencyRates

#weather-api
from weather import Weather, Unit

base_dir = '/home/pi/retro-clock/'
animation_folder = "frames/"
animations = ["frame1.png", "frame2.png", "frame3.png", "frame4.png", "frame5.png", "frame6.png", "frame7.png", "frame8.png", "frame9.png", "frame10.png", "frame11.png", "frame12.png", "frame13.png", "frame14.png", "frame15.png", "frame16.png", "frame17.png", "frame18.png", "frame19.png", "frame20.png", "frame21.png", "frame22.png", "frame23.png", "frame24.png", "frame25.png", "frame26.png", "frame27.png", "frame28.png", "frame29.png", "frame30.png", "frame31.png", "frame32.png", "frame33.png", "frame34.png", "frame35.png", "frame36.png", "frame37.png"]

# Counters for timing & scheduling
i=0 # animation frame counter
k=0 # one cycle counter
w=0 # weather refresh counter
c=0 # exchange rate refresh counter

# Weather variables
city = 'IZMIR'
temperature = "N/A"
weathercondition = " "

# Currency variables
usd_in_try = "N/A"
eur_in_try = "N/A"

# Music playing flag
f_music_playing = 0

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0

fontcolor = 128, 214, 255
fontcolor2 = 255, 227, 89
fontsize = 100

def retrieve_weather():
    global weathercondition
    global temperature

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


def retrieve_currency():
    global usd_in_try
    global eur_in_try

    try:
        currate = CurrencyRates()
        usd_in_try = currate.get_rate('USD', 'TRY')
        eur_in_try = currate.get_rate('EUR', 'TRY')
    except Exception as error:
        usd_in_try = "N/A"
        eur_in_try = "N/A"

def music_scene():
    global fontsize
    global clock
    global width
    global height
    global screen
    musicicon = pygame.image.load (base_dir + "music.png")
    screen.blit (musicicon, [0, 3.3*height/5])

    font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 55)
    nowplayingimg = font.render ("Now Playing:", 1, fontcolor)

    artistname = "Yuki Katamura"
    if len(artistname)>23:
        font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
        artistnameimg = font.render(artistname[0:23]+"..." , 1, fontcolor2)
    else:
        font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
        artistnameimg = font.render(artistname , 1, fontcolor2)

    songname = "Dark Souls 3 Theme"
    if len(songname)>23:
        font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
        songnameimg = font.render(songname[0:23]+"..." , 1, fontcolor2)
    else:
        font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 50)
        songnameimg = font.render(songname , 1, fontcolor2)

    screen.blit(nowplayingimg, [120, 300]) #300
    screen.blit(artistnameimg, [120, 365])
    screen.blit(songnameimg, [120, 420])

    #Clock on corner
    font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 40)
    fontimg = font.render(clock, 1, fontcolor)
    screen.blit(fontimg, [610,30])
    clockicon = pygame.image.load (base_dir + "clocksmall.png")
    screen.blit(clockicon,[540,30])

def clock_scene():
    global fontsize
    global clock
    global width
    global height
    global screen
    font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", fontsize)
    fontimg = font.render(clock, 1, fontcolor)
    fontimg_rect = fontimg.get_rect(center=(1.3*width/3,4.3*height/5))
    screen.blit(fontimg, [130, 3.65*height/5])

    clockicon = pygame.image.load (base_dir + "clock.png")
    screen.blit(clockicon,[20,3.8*height/5])

def calendar_scene():
    global fontsize
    global date
    global now
    global width
    global height
    global screen
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

def weather_scene():
    global fontsize
    global temperature
    global weathercondition
    global now
    global width
    global height
    global screen
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

def main():
    global fontsize
    global i
    global k
    global w
    global c
    global temperature
    global weathercondition
    global clock
    global date
    global width
    global height
    global screen
    global now

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
    retrieve_weather()

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



        # Exchange rate info
        if (c==0):
            threading.Thread(target=retrieve_currency).start()

        # Weather info - get every 1 weather cycle
        if (w==0):
            threading.Thread(target=retrieve_weather).start()

        now = datetime.datetime.today()

        date = now.strftime("%d %b %Y")
        secPython = float(str(now)[17:26])


        dt = str(now - delta)
        clock = dt[11:19]

        animation = pygame.image.load (base_dir + animation_folder + animations[i])
        screen.blit (animation, [0,0])

        if temperature == "N/A" or usd_in_try == "N/A":
            # Connection lost logo, if connection is lost
            connlosticon = pygame.image.load (base_dir + "connlost.png")
            screen.blit(connlosticon,[20, 30])


        # Animation timer
        if i>35:
            i = 0
        else:
            i = i+1

        # Exchange rate timer
        if (c>1000):
            c = 0
        else:
            c = c + 1

        # Weather request timer
        if (w>7000):
            w = 0
        else:
            w = w + 1

        # One cycle timer
        if (k>600):
            k = 0
        else:
            k = k + 1

        # Add scenes
        if (f_music_playing==1): # If bluetooth is connected for A2DP, then we prioritize it
            music_scene()

        elif (k<100): #Clock
            clock_scene()

        elif (k<200): #Calendar
            calendar_scene()

        elif (k<300):
            clock_scene()

        elif (k<400): #Temperature
            weather_scene()

        elif (k<500):
            clock_scene()

        else: # Currency rates

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render("USD", 1, fontcolor2)
            screen.blit(fontimg, [175, 330])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render("EUR" , 1, fontcolor2)
            screen.blit(fontimg, [175, 400])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render(str(usd_in_try)+" TRY", 1, fontcolor)
            screen.blit(fontimg, [320, 330])

            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 60)
            fontimg = font.render(str(eur_in_try)+" TRY" , 1, fontcolor)
            screen.blit(fontimg, [320, 400])

            calendaricon = pygame.image.load (base_dir + "currency.png")
            screen.blit(calendaricon,[30,3.66*height/5])

            #Clock on corner
            font = pygame.font.Font(base_dir + "fonts/trs-million.ttf", 40)
            fontimg = font.render(clock, 1, fontcolor)
            screen.blit(fontimg, [610,30])
            clockicon = pygame.image.load (base_dir + "clocksmall.png")
            screen.blit(clockicon,[540,30])


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
