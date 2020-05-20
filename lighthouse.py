#!/usr/bin/python3

import time

import board
import digitalio
import RPi.GPIO as GPIO

#HARDWARE SETUP
# Model+ P1
# 2[=========XGYR]26
# 1[=============]25
# LED=[26,24,22] #RED, YELLOW, GREEN
# Model+ P1
# 2[===============XGYR]40
# 1[===================]39
LED = [40,38,36] #RED, YELLOW, GREEN (uncomment to use)

FLASH_TIME=0.5
RED, YELLOW,GREEN = 0, 1, 2
ON, OFF = True, False

def GPIOsetup():
   GPIO.setmode(GPIO.BOARD)
   for led in (RED, YELLOW, GREEN):
      GPIO.setup(LED[led], GPIO.OUT)


def ControlLights():
    for led in (RED, YELLOW, GREEN):
        GPIO.output(LED[led], ON)
        time.sleep(FLASH_TIME)
    for led in (RED, YELLOW, GREEN):
        GPIO.output(LED[led], OFF)
        time.sleep(FLASH_TIME)
    for _ in range(2):
        for led in (RED, YELLOW, GREEN):
            GPIO.output(LED[led], ON)
        time.sleep(FLASH_TIME)
        for led in (RED, YELLOW, GREEN):
            GPIO.output(LED[led], OFF)
        time.sleep(FLASH_TIME)


def blinkaLights():
    print("hello blinky!")
    red = digitalio.DigitalInOut(board.D40)
    yellow = digitalio.DigitalInOut(board.D38)
    green = digitalio.DigitalInOut(board.D36)
    for led in [red, yellow, green]:
        led.direction = digitalio.Direction.OUTPUT
    while True:
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)


if __name__ == "__main__":
    # GPIOsetup()
    # ControlLights()
    # GPIO.cleanup()
    blinkaLights()
