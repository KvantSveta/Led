import signal
from time import sleep
from datetime import datetime
from threading import Event

import RPi.GPIO as GPIO

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()


signal.signal(signal.SIGTERM, handler)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

RED = 17
GREEN = 27
BLUE = 22

GPIO.setup(RED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BLUE, GPIO.OUT, initial=GPIO.LOW)

red_frq = GPIO.PWM(RED, 50)
red_frq.start(0)
green_frq = GPIO.PWM(GREEN, 50)
green_frq.start(0)
blue_frq = GPIO.PWM(BLUE, 50)
blue_frq.start(0)


def pwm_colour_up(colour_freq, time_shine=0.1):
    for c in range(101):
        colour_freq.ChangeDutyCycle(c)
        sleep(time_shine)
    sleep(1)

def pwm_colour_down(colour_freq, time_shine=0.1):
    for c in range(101):
        colour_freq.ChangeDutyCycle(100 - c)
        sleep(time_shine)
    sleep(1)


while run_service.is_set():
    if 6 <= datetime.now().hour < 22:
        pwm_colour_up(red_frq)
        pwm_colour_up(green_frq)
        pwm_colour_down(red_frq)
        pwm_colour_up(blue_frq)
        pwm_colour_down(green_frq)
        pwm_colour_up(red_frq)
        pwm_colour_up(green_frq)

        pwm_colour_down(red_frq)
        pwm_colour_down(green_frq)
        pwm_colour_up(red_frq)
        pwm_colour_down(blue_frq)
        pwm_colour_up(green_frq)
        pwm_colour_down(red_frq)
        pwm_colour_down(green_frq)

    else:
        sleep(60)

red_frq.stop()
green_frq.stop()
blue_frq.stop()

GPIO.cleanup([RED, GREEN, BLUE])
