#!/usr/bin/python3

import time

import board
import digitalio

DELAY = 0.5


def blink(color):
    colors = {"green": digitalio.DigitalInOut(board.D16),
              "yellow": digitalio.DigitalInOut(board.D20),
              "red": digitalio.DigitalInOut(board.D21)}
    led = colors[color]
    while True:
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        time.sleep(DELAY)
        led.value = False
        time.sleep(DELAY)


if __name__ == "__main__":
    pass
