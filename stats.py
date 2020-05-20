#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print system stats."""

import psutil
import time

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


def get_display():
    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None

    # Config for display baudrate (default max is 24mhz):
    BAUDRATE = 64000000

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()

    # Create the ST7789 display:
    disp = st7789.ST7789(
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
    # Create blank image for drawing.
    # Make sure to create image with mode 'RGB' for full color.
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 270
    return image, height, width, rotation

def get_draw(disp, image, rotation):
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    return draw

def get_backlight():
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    return backlight

def get_stats():
    MB = 1048576
    GB = 1073741824
    metrics = {}
    metrics["IP"] = f"IP: {psutil.net_if_addrs()['wlan0'][0].address}"
    metrics["CPU"] = f"CPU: {psutil.cpu_percent(interval=0.1)}%"
    mem = psutil.virtual_memory()
    used = (mem.total - mem.available) / MB
    metrics["MemUsage"] = f"Mem: {used:.0f}/{(mem.total / MB):.0f}M {mem.percent:.0f}%"
    disk = psutil.disk_usage("/")
    metrics["Disk"] = f"Disk: {(disk.used / GB):.1f}/{(disk.total / GB):.1f}G {disk.percent:.0f}%"
    metrics["Temp"] = f"Temp: {psutil.sensors_temperatures()['cpu-thermal'][0].current:.1f} C"
    return metrics

def write_text(disp, image, draw, backlight, height, width, metrics, counter):
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

    # Turn on the backlight
    backlight.value = True

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Write four lines of text.
    y = top
    draw.text((x, y), f'{metrics["IP"]}  {counter}', font=font, fill="#FFFFFF")
    y += font.getsize(metrics["IP"])[1]
    draw.text((x, y), metrics["CPU"], font=font, fill="#FFFF00")
    y += font.getsize(metrics["CPU"])[1]
    draw.text((x, y), metrics["MemUsage"], font=font, fill="#00FF00")
    y += font.getsize(metrics["MemUsage"])[1]
    draw.text((x, y), metrics["Disk"], font=font, fill="#0000FF")
    y += font.getsize(metrics["Disk"])[1]
    draw.text((x, y), metrics["Temp"], font=font, fill="#FF00FF")

    disp.image(image, rotation)
    # time.sleep(0.2)
    return

if __name__ == "__main__":
    disp = get_display()
    image, height, width, rotation = get_image(disp)
    draw = get_draw(disp, image, rotation)
    backlight = get_backlight()
    try:
        counter = 0
        while True:
            metrics = get_stats()
            write_text(disp, image, draw, backlight, height, width, metrics, counter)
            counter += 1
    except KeyboardInterrupt:
        backlight.value = False
