#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time
import sys
sys.path.append('/usr/lib/pypy-upstream/site-packages')
import requests
import json
import datetime

PIN = 17
HUE = '192.168.1.217'
USERNAME = 'markmossberg'
BASE = 'http://{}/api/{}'.format(HUE, USERNAME)
BUTTON_SLEEP = 0.2

gpio.setmode(gpio.BCM)
gpio.setup(PIN, gpio.IN, pull_up_down=gpio.PUD_UP)


def callback():
    survey = requests.get(BASE + '/lights')
    survey = json.loads(survey.text)
    if any([survey[str(x)]['state']['on'] for x in range(1, 4)]):
        # if any are on, turn all off.
        for light in survey.keys():
            turn(light, False)
        print '[{}] Off'.format(datetime.datetime.now())
    else:
        # else if all are off, then all on
        for light in survey.keys():
            turn(light, True)
        print '[{}] On'.format(datetime.datetime.now())



def turn(light, state):
    data = json.dumps({'on':state})
    requests.put(BASE + '/lights/{}/state'.format(light), data=data)


def main():
    while True:
        inp = gpio.input(PIN)
        if not inp:
            callback()
        time.sleep(BUTTON_SLEEP)

if __name__ == '__main__':
    main()
