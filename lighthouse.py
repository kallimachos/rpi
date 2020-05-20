#!/usr/bin/python3

import time

import board
import digitalio

# import RPi.GPIO as GPIO


DELAY = 0.5


# def GPIOLights():
#     GPIO.setmode(GPIO.BOARD)
#     red = 40
#     yellow = 38
#     green = 36
#     for pin in [red, yellow, green]:
#         GPIO.setup(pin, GPIO.OUT)
#         GPIO.output(pin, True)
#         time.sleep(DELAY)
#         GPIO.output(pin, False)
#         time.sleep(DELAY)
#     GPIO.cleanup()


def blinkaLights():
    red = digitalio.DigitalInOut(board.D21)
    yellow = digitalio.DigitalInOut(board.D20)
    green = digitalio.DigitalInOut(board.D16)
    for led in [red, yellow, green]:
        led.direction = digitalio.Direction.OUTPUT
        led.value = True
        time.sleep(DELAY)
        led.value = False
        time.sleep(DELAY)


if __name__ == "__main__":
    # GPIOLights()
    blinkaLights()
