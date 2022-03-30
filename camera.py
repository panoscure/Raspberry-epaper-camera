import sys
import os
sys.path.insert(1,"/home/pi/progs/sensor")
#import subprocess
import subprocess
from subprocess import check_output

import json
import requests
#import schedule

from PIL import Image,ImageDraw,ImageFont     # import the image libraries
import time
from gpiozero import Button                   # import the Button control from gpiozero
from datetime import datetime
import logging
import epaper
from signal import pause
import rasp_info
from picamera import PiCamera
import ftp_upload as ftp

epaper.log_actions()

btn1 = Button(5)                              # assign each button to a variable
btn2 = Button(6)                              # by passing in the pin number
btn3 = Button(13)                             # associated with the button
btn4 = Button(19)
last_connect_datetime ='empty'
button_pressed =0			      #keep the previous pressed button
step=0

#epd = epd2in7.EPD()                          # get the display object and assing to epd
#epd.init()                                    # initialize the display
#print("Clear...")                             # print message to console (not display) for debugging
#epd.Clear(0xFF)                               # clear the display

#total lines 7 and rows 12
line = [0,24,48,72,96,120,144]
column = [0,22,44,66,88,110,132,154,176,198,220,242]

photo_list = []    #store here the photo names
images_path = '/home/pi/progs/sensor/camera/pics/'
camera = ""

def get_photo_names():
    global photo_list
    photo_list = os.listdir(images_path)
    #for i in range(len(photo_list)):
    #    print(photo_list[i])

def camera_init():
    global camera
    camera = PiCamera()
    camera.resolution = (1280, 720)
    camera.vflip = True
    camera.contrast = 10
    #camera.image_effect = "watercolor"
    time.sleep(2)


def button1Press():
#sudo apt install python3-pip
#pip3 install picamera
    global images_path, camera
    file_name = "img_" + str(int(time.time())) + ".jpg"
    file_path = images_path+file_name
    camera.capture(file_path)
    print("Done.")
    try:
        epaper.screen_init()
        epaper.display_images(file_path)
        epaper.logging.info('Image displayed')

    except Exception as e:
        print(e)
        print("could not display logo")

    try:
        #upload image to ftp
        ftp.send_file(file_path,file_name)
    except Exception as e:
        print('could not upload to ftp',e)

    print("Button 1")

def button2Press():
    global photo_list, button_pressed

    if button_pressed != 2:
        get_photo_names()
        button_pressed = 2

    photo_list = photo_list[1:] + photo_list[:1]

    epaper.screen_init()
    epaper.draw_info_screen()
    if len(photo_list) < 6:
        for i in range(len(photo_list)):
            epaper.printToDisplay(str(photo_list[i]),line[i],column[0],18)
    else:
        for i in range(6):
            epaper.printToDisplay(str(photo_list[i]),line[i],column[0],18)

    epaper.printToDisplay("<--",line[0],column[10],18)
    epaper.epd_display()


def button3Press():
    global photo_list, button_pressed
    if button_pressed == 3:
        if os.path.exists(images_path + photo_list[0]):
            os.remove(images_path + photo_list[0])
            button2Press()
    else:
        button_pressed=3

    try:
        epaper.screen_init()
        epaper.display_images(images_path + photo_list[0])
        epaper.logging.info('Image Selected to display')
    except Exception as e:
        print(e)
        print("could not display logo")


def button4Press():
    global button_pressed
    button_pressed=4

    try:
        cpu = rasp_info.get_cpu()
        mem = rasp_info.get_memory()
        hdd = rasp_info.get_hdd()
        revision= rasp_info.get_revision()
        network_name=rasp_info.get_network_name()
    except Exception as e:
        print(e)
        print("could not load hardware info")

    epaper.screen_init()

    try:

        ip = str((check_output(['hostname', '-I'])))
        ip = ip[2:]
        size = len(ip)
        ip = ip[:size-3]
        epaper.printToDisplay("IP",line[0],column[10],18)
        epaper.printToDisplay(ip,line[0],column[0],18)
        epaper.printToDisplay("CPU",line[2],column[10],18)
        epaper.printToDisplay(cpu,line[2],column[0],18)
        epaper.printToDisplay("MeM",line[3],column[10],18)
        epaper.printToDisplay(mem,line[3],column[0],18)
        epaper.printToDisplay("H/D",line[4],column[10],18)
        epaper.printToDisplay(hdd,line[4],column[0],18)
        epaper.printToDisplay("Model",line[5],column[10],18)
        epaper.printToDisplay(revision,line[5],column[0],18)

        epaper.printToDisplay("Net",line[1],column[10],18)
        epaper.printToDisplay(str(network_name),line[1],column[0],18)


        epaper.printToDisplay("RASPBERRY INFO",line[6],column[2],18)

        epaper.draw_info_screen()
        epaper.epd_display()

    except Exception as e:
        print(e)
        print("Something went wrong on displaying raspberry info")
        epaper.printToDisplay("Cannot Retrieve raspberry info",line[3],column[0],18)



    print("button 4")


try:
#initialize camera
    camera_init()
    print("camera initialized")
except Exception as e:
    print(e)
    print("Could not initialize camera")

#display the logo
try:
    epaper.screen_init()
    epaper.display_images('/home/pi/progs/sensor/camera/pics/logo.bmp')
    epaper.logging.info('Logo displayed')
    time.sleep(7)

except Exception as e:
    print(e)
    print("could not display logo")

logging.info('Screen init and logo display')

try:
    epaper.screen_init()
    epaper.first_screen()
    epaper.printToDisplay("Press to take Photo",line[0],column[0],18)
    epaper.printToDisplay("Press to view Photos",line[2],column[0],18)
    epaper.printToDisplay("Press to display/Delete Photo",line[4],column[0],18)
    epaper.printToDisplay("View Raspberry Details",line[6],column[0],18)
    epaper.epd_display()

except Exception as e:
    print(e)
    print("something is wrong with the epaper")


while 1:
    # datetime object containing current date and time
#    now = datetime.now()

    # tell the button what to do when pressed
    btn1.when_pressed = button1Press
    btn2.when_pressed = button2Press
    btn3.when_pressed = button3Press
    btn4.when_pressed = button4Press

#    t_string = now.strftime("%M:%S")
    #print("time =", t_string)

