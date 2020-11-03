#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Display busy message."""

from os import getenv
from time import sleep

import adafruit_rgb_display.st7789 as st7789
import board
import colorlog
import digitalio
import requests
from dotenv import find_dotenv, load_dotenv
from PIL import Image, ImageDraw, ImageFont

from utils import logconfig

logger = colorlog.getLogger()


def get_buttons():
    buttonA = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB = digitalio.DigitalInOut(board.D23)
    buttonB.switch_to_input()
    return buttonA, buttonB


def get_display():
    # Configuration for CS and DC pins
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None
    BAUDRATE = 64000000  # Config for display baudrate (default max is 24mhz)
    spi = board.SPI()  # Setup SPI bus using hardware SPI
    disp = st7789.ST7789(  # Create the ST7789 display
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        width=135,
        height=240,
        x_offset=53,
        y_offset=40,
    )
    return disp


def get_image(disp):
    # Create blank image for drawing. Use 'RGB' for full color.
    height = disp.width  # swap height/width for landscape mode
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 270
    return image, height, width, rotation


def get_draw(disp, image, rotation):
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Draw black box to clear image.
    disp.image(image, rotation)
    return draw


def get_backlight():
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    return backlight


def draw_text(draw, height, width, data):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    line_height = font.getsize(data["level"])[1]
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Draw black box to clear image.
    x = 0
    y = 2  # add padding to the top
    colors = {
        "low": "#FFFFFF",
        "med": "#FFFF00",
        "high": "#00FF00",
    }
    for key, value in data.items():
        draw.text((x, y), f"{key}:{value}", font=font, fill=colors["low"])
        y += line_height
    return


if __name__ == "__main__":
    logconfig()
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    buttonA, buttonB = get_buttons()
    disp = get_display()
    image, height, width, rotation = get_image(disp)
    draw = get_draw(disp, image, rotation)
    backlight = get_backlight()
    with requests.Session() as session:
        while True:
            if buttonB.value and not buttonA.value:  # just button A pressed
                logger.info("Checking level")
                response = session.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
                data = response.json()
                logger.info(f"Current level: {data}")
                draw_text(draw, height, width, data)
                disp.image(image, rotation)
                backlight.value = True
                sleep(5)
            elif buttonA.value and not buttonB.value:  # just button B pressed
                pass
            elif buttonA.value and not buttonB.value:  # both buttons pressed
                pass
            else:  # neither button pressed
                backlight.value = False
                sleep(0.1)  # reduce CPU load by sleeping between loops
