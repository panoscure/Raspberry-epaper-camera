import sys
import os
sys.path.insert(1,"/home/pi/progs/sensor")
import subprocess
import json
import requests
#import schedule
from subprocess import check_output

import epd2in7                               # import the display drivers
from PIL import Image,ImageDraw,ImageFont     # import the image libraries
import time
from gpiozero import Button                   # import the Button control from gpiozero
from datetime import datetime
import logging


last_connect_datetime ='empty'

epd = epd2in7.EPD()                          # get the display object and assing to epd
#epd.init()                                    # initialize the display
#print("Clear...")                             # print message to console (not display) for debugging
#epd.Clear(0xFF)                               # clear the display

#total lines 7 and rows 12
line = [0,24,48,72,96,120,144]
column = [2,23,43,66,87,105,127,147,170,188,207,228]



def screen_init():
    global draw, HBlackImage,epd
    epd.init()
    epd.Clear(0xFF)
    #display_images('/home/pi/progs/sensor/epaper/logo.bmp')
    #time.sleep(7)

    # Drawing on the Horizontal image. We must create an image object for both the black layer
    # and the red layer, even if we are only printing to one layer
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 298*126
    #HRedImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 298*126

    # create a draw object and the font object we will use for the display
    draw = ImageDraw.Draw(HBlackImage)
#    font_free_sans()
#    drawLinesScreen()

def clear_screen():
    global epd
    epd.Clear(0xFF)

def font_free_sans(size):
    global font
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', size)

def font_free_mono():
    global font
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 30)

def font_free_serif():
    global font
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', 20)

def font_free_firasans():
    global font
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FiraSans-Two.ttf', 30)

def display_images(img_name):
    global HBlackImage
    blackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 298*126
    image = Image.open(img_name)
    new_image = image.resize((270, 180))
    blackImage.paste(new_image, (0,0))
    epd.display(epd.getbuffer(blackImage))


# Print a message to the screen
# @params string
def printToDisplay(string,line,column,size):
    font_free_sans(size)
    # draw the text to the display. First argument is starting location of the text in pixels
    draw.text((column, line), string, font = font, fill = 0)

    # Add the images to the display. Both the black and red layers need to be passed in, even
    # if we did not add anything to one of them
    #epd.display(epd.getbuffer(HBlackImage))

def epd_display():
    epd.display(epd.getbuffer(HBlackImage))


# Handle button presses
# param Button (passed from when_pressed)

def drawLine(from_pixel_χ,from_pixel_y,to_pixel_x,to_pixel_y):
#    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)  # 298*126
#    draw = ImageDraw.Draw(HBlackImage)
    draw.line((to_pixel_x,to_pixel_y, from_pixel_χ,from_pixel_y), fill=0)

    epd.display(epd.getbuffer(HBlackImage))

def draw_info_screen():
    draw.line((0,24, 298,24), fill=0)
    draw.line((0,48, 298,48), fill=0)
    draw.line((0,72, 298,72), fill=0)
    draw.line((0,96, 298,96), fill=0)
    draw.line((0,120, 298,120), fill=0)
    draw.line((0,144, 298,144), fill=0)

    draw.line((220,0, 220,144), fill=0)
    #epd.display(epd.getbuffer(HBlackImage))

def first_screen():
    draw.line((0,24, 298,24), fill=0)
    draw.line((0,48, 298,48), fill=0)
    draw.line((0,72, 298,72), fill=0)
    draw.line((0,96, 298,96), fill=0)
    draw.line((0,120, 298,120), fill=0)
    draw.line((0,144, 298,144), fill=0)


def handleBtnPress(btn):

    # get the button pin number
    pinNum = btn.pin.number

    # python hack for a switch statement. The number represents the pin number and
    # the value is the message we will print
    switcher = {
        5: "Hello, World!",
        6: "This is my first \nRPi project.",
        13: "Hope you liked it.",
        19: "Goodbye"
    }
    
    # get the string based on the passed in button and send it to printToDisplay()
    msg = switcher.get(btn.pin.number, "Error")
    printToDisplay(msg,18)

def increase_button_pressed():
    global button_pressed
    global terminal_list
    if button_pressed == len(terminal_list):
        button_pressed = 0
    button_pressed=button_pressed+1


def store_datetime():
    global last_connect_datetime
    now = datetime.now()
    # dd/mm/YY H:M:S
    last_connect_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
    #print("date and time =", last_connect_datetime)


def increase_and_request():
    increase_button_pressed()
    button1Press()


        # Set up logging

def log_actions():
    log = "/home/pi/progs/sensor/net/logs/net.log"
    logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


def create_wifi_config(SSID, password):
    config_lines = [
  '\n',
  'network={',
  '\tssid="{}"'.format(SSID),
  '\tpsk="{}"'.format(password),
  '\tkey_mgmt=WPA-PSK',
  '}'
    ]

    config = '\n'.join(config_lines)
    print(config)

    with open("/etc/wpa_supplicant/wpa_supplicant_back.conf", "a+") as wifi:
        wifi.write(config)

    print("Wifi config added")

def password_screen():
    draw.line((0,24, 298,24), fill=0)
    draw.line((0,48, 298,48), fill=0)
    draw.line((0,72, 298,72), fill=0)
    draw.line((0,96, 298,96), fill=0)
    draw.line((0,120, 298,120), fill=0)
    draw.line((0,144, 298,144), fill=0)

    for i in range(1,15):
        draw.line((i*20,0, i*20,144), fill=0)


def pass_chars():
    printToDisplay("a",line[0],column[0],18)
    printToDisplay("b",line[0],column[1],18)
    printToDisplay("c",line[0],column[2],18)
    printToDisplay("d",line[0],column[3],18)
    printToDisplay("e",line[0],column[4],18)
    printToDisplay("f",line[0],column[5],18)
    printToDisplay("g",line[0],column[6],18)
    printToDisplay("h",line[0],column[7],18)
    printToDisplay("i",line[0],column[8],18)
    printToDisplay("j",line[0],column[9],18)
    printToDisplay("k",line[0],column[10],18)
    printToDisplay("l",line[0],column[11],18)
    printToDisplay("m",line[1],column[0],18)
    printToDisplay("n",line[1],column[1],18)
    printToDisplay("o",line[1],column[2],18)
    printToDisplay("p",line[1],column[3],18)
    printToDisplay("q",line[1],column[4],18)
    printToDisplay("r",line[1],column[5],18)
    printToDisplay("s",line[1],column[6],18)
    printToDisplay("t",line[1],column[7],18)
    printToDisplay("u",line[1],column[8],18)
    printToDisplay("v",line[1],column[9],18)
    printToDisplay("w",line[1],column[10],18)
    printToDisplay("x",line[1],column[11],18)
    printToDisplay("y",line[2],column[0],18)
    printToDisplay("z",line[2],column[1],18)
    printToDisplay("1",line[2],column[2],18)
    printToDisplay("2",line[2],column[3],8)
    printToDisplay("3",line[2],column[4],18)
    printToDisplay("4",line[2],column[5],18)
    printToDisplay("5",line[2],column[6],18)
    printToDisplay("6",line[2],column[7],18)
    printToDisplay("7",line[2],column[8],18)
    printToDisplay("8",line[2],column[9],18)
    printToDisplay("9",line[2],column[10],18)
    printToDisplay("0",line[2],column[11],18)
    printToDisplay("~",line[3],column[0],18)
    printToDisplay("!",line[3],column[1],18)
    printToDisplay("@",line[3],column[2],18)
    printToDisplay("#",line[3],column[3],18)
    printToDisplay("$",line[3],column[4],18)
    printToDisplay("%",line[3],column[5],18)
    printToDisplay("^",line[3],column[6],18)
    printToDisplay("&",line[3],column[7],18)
    printToDisplay("*",line[3],column[8],18)
    printToDisplay("(",line[3],column[9],18)
    printToDisplay(")",line[3],column[10],18)
    printToDisplay("-",line[3],column[11],18)
    printToDisplay("_",line[4],column[0],18)
    printToDisplay("+",line[4],column[1],18)
    printToDisplay("=",line[4],column[2],18)
    printToDisplay(",",line[4],column[3],18)
    printToDisplay(".",line[4],column[4],18)
    printToDisplay("/",line[4],column[5],18)
    printToDisplay("?",line[4],column[6],18)
    printToDisplay("[",line[4],column[7],18)
    printToDisplay("]",line[4],column[8],18)
    printToDisplay("{",line[4],column[9],18)
    printToDisplay("}",line[4],column[10],18)
    printToDisplay("|",line[4],column[11],18)

    
