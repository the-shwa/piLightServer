GREEN_PIN = 22

import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread
STEPS     = 0.05
bright = 255
g = 0.0
pi = pigpio.pi()

def updateColor(color, step):
	color += step

	if color > 255:
		return 255
	if color < 0:
		return 0

	return color

def setLights(pin, brightness):
    realBrightness = int(int(brightness) * (float(bright) / 255.0))
    pi.set_PWM_dutycycle(pin, realBrightness)

up = True
setLights(GREEN_PIN, g)
while True:
    if up and g < 255:
        g = updateColor(g, STEPS)
    elif g == 255:
        g = updateColor(g, -STEPS)
        up = False
    elif not up and g > 0:
        g = updateColor(g, -STEPS)
    elif g == 0:
        g = updateColor(g, STEPS)
        up = True
    setLights(GREEN_PIN, g)

setLights(GREEN_PIN, 0)
time.sleep(0.5)
pi.stop()
