#!/usr/bin/python3
#lighthouse.py
import time
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
    for led in (RED, YELLOW, GREEN):
        GPIO.output(LED[led], ON)
    time.sleep(FLASH_TIME)
    for led in (RED, YELLOW, GREEN):
        GPIO.output(LED[led], OFF)


if __name__ == "__main__":
    GPIOsetup()
    ControlLights()
    GPIO.cleanup()
