#!/usr/bin/python3

import time

import board
import digitalio
import requests

DELAY = 1.0


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    time.sleep(DELAY)
    led.value = False
    time.sleep(DELAY)
    return


if __name__ == "__main__":
    leds = {"green": digitalio.DigitalInOut(board.D16),
            "yellow": digitalio.DigitalInOut(board.D20),
            "red": digitalio.DigitalInOut(board.D21)}
    while True:
        response = requests.get(f"http://localhost:8080/getlevel")
        level, message = list(response.text)[0], list(response.text.values())[0]
        if level == "off":
            time.sleep(10.0)
        else:
            led = leds[message]
            for x in range(10):
                blink(led)
