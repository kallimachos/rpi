#!/usr/bin/python3

import json
import time
from os import getenv

import board
import digitalio
import requests
from dotenv import find_dotenv, load_dotenv


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    time.sleep(1.0)
    led.value = False
    time.sleep(2.0)
    return


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    leds = {
        "low": digitalio.DigitalInOut(board.D16),  # green
        "med": digitalio.DigitalInOut(board.D20),  # yellow
        "high": digitalio.DigitalInOut(board.D21),  # red
    }
    while True:
        response = requests.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
        text = json.loads(response.text)
        level, message = list(text)[0], list(text.values())[0]
        if level == "off":
            time.sleep(5.0)
        else:
            led = leds[message]
            for x in range(3):
                blink(led)
