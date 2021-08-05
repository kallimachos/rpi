#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Display busy message and lights."""

from os import getenv
from time import sleep

import adafruit_rgb_display.st7789 as st7789
import board
import colorlog
import digitalio
import psutil
import requests
from dotenv import find_dotenv, load_dotenv
from PIL import Image, ImageDraw, ImageFont

from utils import logconfig

logger = colorlog.getLogger()


def get_buttons():
    """Get display hardware buttons."""
    buttonA = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB = digitalio.DigitalInOut(board.D23)
    buttonB.switch_to_input()
    return buttonA, buttonB


def get_display():
    """Configuration for CS and DC pins."""
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
    """Create blank image for drawing. Use 'RGB' for full color."""
    height = disp.width  # swap height/width for landscape mode
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 270
    return image, height, width, rotation


def get_draw(disp, image, rotation):
    """Get drawing instance."""
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Draw black box to clear image.
    disp.image(image, rotation)
    return draw


def get_backlight():
    """Get backlight."""
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    return backlight


def draw_text(draw, height, width, data):
    """Draw text."""
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    line_height = font.getsize("text")[1]
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Draw black box to clear image.
    x = 0  # add padding to the left
    y = 2  # add padding to the top
    colors = ["#FF00FF", "#0000FF", "#00FF00", "#FFFF00", "#FFFFFF"]
    for key, value in data.items():
        draw.text((x, y), f"{key}: {value}", font=font, fill=colors.pop())
        y += line_height
    return


def get_stats():
    """Get RPi stats."""
    MB = 1048576
    GB = 1073741824
    metrics = {}
    metrics["IP"] = f"{psutil.net_if_addrs()['wlan0'][0].address}"
    metrics["CPU"] = f"{(psutil.getloadavg()[0] * 100):.1f}%"
    mem = psutil.virtual_memory()
    used = (mem.total - mem.available) / MB
    metrics["Mem"] = f"{used:.0f}/{(mem.total / MB):.0f}M {mem.percent:.0f}%"
    disk = psutil.disk_usage("/")
    metrics["Disk"] = f"{(disk.used / GB):.1f}/{(disk.total / GB):.1f}G {disk.percent:.0f}%"
    metrics["Temp"] = f"{psutil.sensors_temperatures()['cpu_thermal'][0].current:.1f} C"
    return metrics


def display_level(disp, draw, height, width):
    """Display current level."""
    logger.info("Checking level")
    response = session.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
    data = response.json()
    logger.info(f"Current level: {data}")
    draw_text(draw, height, width, data)
    disp.image(image, rotation)
    backlight.value = True
    sleep(5)
    return


def display_stats(disp, draw, height, width):
    """Display RPi stats."""
    logger.info("Getting stats")
    data = get_stats()
    logger.info(f"Stats: {data}")
    draw_text(draw, height, width, data)
    disp.image(image, rotation)
    backlight.value = True
    sleep(5)
    return


def reset_level(disp, draw, height, width):
    """Set level to off."""
    logger.info("Resetting level")
    data = {"level": "off", "msg": "", "end": ""}
    logger.info(f"Data: {data}")
    requests.post(f"http://{RPI_IP}:{RPI_PORT}/setlevel", json=data)
    logger.info(f"Level set: {data}")
    draw_text(draw, height, width, data)
    disp.image(image, rotation)
    backlight.value = True
    sleep(5)
    return


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    sleep(1)
    led.value = False
    sleep(1)
    return


if __name__ == "__main__":
    logconfig()
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    LEDS = {
        "low": digitalio.DigitalInOut(board.D16),  # green
        "med": digitalio.DigitalInOut(board.D20),  # yellow
        "high": digitalio.DigitalInOut(board.D21),  # red
    }
    print("mlights is running")
    buttonA, buttonB = get_buttons()
    disp = get_display()
    image, height, width, rotation = get_image(disp)
    draw = get_draw(disp, image, rotation)
    backlight = get_backlight()
    print("mdisplay is running")
    with requests.Session() as session:
        try:
            while True:
                response = session.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
                data = response.json()
                logger.info(f"Current level: {data}")
                if data["level"] == "off":
                    sleep(5)
                else:
                    led = LEDS[data["level"]]
                    for x in range(3):
                        blink(led)
                if buttonB.value and not buttonA.value:  # just button A pressed
                    display_level(disp, draw, height, width)
                elif buttonA.value and not buttonB.value:  # just button B pressed
                    display_stats(disp, draw, height, width)
                elif not buttonA.value and not buttonB.value:  # both buttons pressed
                    reset_level(disp, draw, height, width)
                else:  # neither button pressed
                    backlight.value = False
                    sleep(0.1)  # reduce CPU load by sleeping between loops
        except KeyboardInterrupt:
            backlight.value = False
