import signal
from time import sleep
from datetime import datetime
from threading import Event
from random import randint

import RPi.GPIO as GPIO

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()


signal.signal(signal.SIGTERM, handler)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

RED = 26
GREEN = 19
BLUE = 13

GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)

#     R  G  B
# (0, 0, 0, 0) black
# (1, 0, 0, 1) blue
# (2, 0, 1, 0) green
# (3, 0, 1, 1) aqua
# (4, 1, 0, 0) red
# (5, 1, 0, 1) purple
# (6, 1, 1, 0) yellow
# (7, 1, 1, 1) white

color = (
    'black',
    'blue',
    'green',
    'aqua',
    'red',
    'purple',
    'yellow',
    'white'
)

while run_service.is_set():
    if 6 <= datetime.now().hour < 22:
        i = randint(0, 7)

        # print(i, color[i])

        if i in (4, 5, 6, 7):
            GPIO.output(RED, GPIO.HIGH)

        if i in (2, 3, 6, 7):
            GPIO.output(GREEN, GPIO.HIGH)

        if i in (1, 3, 5, 7):
            GPIO.output(BLUE, GPIO.HIGH)

        for i in range(30):
            if run_service.is_set():
                sleep(10)

        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    else:
        sleep(60)

GPIO.cleanup([RED, GREEN, BLUE])
