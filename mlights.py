#!/usr/bin/python3

import json
import time

import board
import digitalio
import requests


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    time.sleep(1.0)
    led.value = False
    time.sleep(2.0)
    return


if __name__ == "__main__":
    leds = {"green": digitalio.DigitalInOut(board.D16),
            "yellow": digitalio.DigitalInOut(board.D20),
            "red": digitalio.DigitalInOut(board.D21)}
    while True:
        response = requests.get(f"http://localhost:8080/getlevel")
        text = json.loads(response.text)
        level, message = list(text)[0], list(text.values())[0]
        if level == "off":
            time.sleep(5.0)
        else:
            led = leds[message]
            for x in range(3):
                blink(led)
