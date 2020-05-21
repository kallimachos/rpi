#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print system stats."""

import subprocess
from time import sleep

import adafruit_rgb_display.st7789 as st7789
import board
import digitalio
import psutil

from PIL import Image, ImageDraw, ImageFont


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


def get_stats():
    MB = 1048576
    GB = 1073741824
    metrics = {}
    metrics["IP"] = f"IP: {psutil.net_if_addrs()['wlan0'][0].address}"
    # metrics["CPU"] = f"CPU: {psutil.cpu_percent(interval=0.0)}%"
    metrics["CPU"] = f"CPU: {(psutil.getloadavg()[0] * 100):.1f}%"
    mem = psutil.virtual_memory()
    used = (mem.total - mem.available) / MB
    metrics["Mem"] = f"Mem: {used:.0f}/{(mem.total / MB):.0f}M {mem.percent:.0f}%"
    disk = psutil.disk_usage("/")
    metrics["Disk"] = f"Disk: {(disk.used / GB):.1f}/{(disk.total / GB):.1f}G {disk.percent:.0f}%"
    metrics["Temp"] = f"Temp: {psutil.sensors_temperatures()['cpu-thermal'][0].current:.1f} C"
    return metrics


def draw_text(draw, backlight, height, width, metrics):
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    line_height = font.getsize(metrics["IP"])[1]
    backlight.value = True
    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # Draw black box to clear image.
    x = 0
    y = 2  # add padding to the top
    colors = {
        "IP": "#FFFFFF",
        "CPU": "#FFFF00",
        "Mem": "#00FF00",
        "Disk": "#0000FF",
        "Temp": "#FF00FF",
    }
    for metric, fill in colors.items():
        draw.text((x, y), f"{metrics[metric]}", font=font, fill=fill)
        y += line_height
    return


if __name__ == "__main__":
    disp = get_display()
    image, height, width, rotation = get_image(disp)
    draw = get_draw(disp, image, rotation)
    backlight = get_backlight()
    try:
        while True:
            metrics = get_stats()
            draw_text(draw, backlight, height, width, metrics)
            disp.image(image, rotation)
            sleep(30)
    except KeyboardInterrupt:
        backlight.value = False
