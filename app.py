RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24
abort = False
from flask import Flask, render_template, request
from thread import start_new_thread
import time
from random import *
import pigpio
pi = pigpio.pi()
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        return render_template('color.html')
    if request.method == 'GET':
        return render_template('index.html',red=255,green=255,blue=255)
    else: #bad :(
        return render_template('bad.html')
@app.route('/radio', methods=['GET', 'POST'])
def radio():
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = True
    if request.method == 'POST':
        color = request.form['color']
        if color == 'Red':
            red=255
            green=0
            blue=0
        if color == 'Green':
            red=0
            green=255
            blue=0
        if color == 'Blue':
            red=0
            green=0
            blue=255
        if color == 'Yellow':
            red=255
            green=255
            blue=0
        if color == 'Orange':
            red=255
            green=165
            blue=0
        if color == 'Purple':
            red=128
            green=0
            blue=128
        if color == 'White':
            red=255
            green=255
            blue=255
	if color == 'Off':
	    red=0
	    green=0
	    blue=0
	pi.set_PWM_dutycycle(RED_PIN, red)
	pi.set_PWM_dutycycle(GREEN_PIN, green)
	pi.set_PWM_dutycycle(BLUE_PIN, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
@app.route('/range', methods=['GET', 'POST'])
def range():
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = True
    if request.method == 'POST':
        red = request.form['red']
        green = request.form['green']
        blue = request.form['blue']
        pi.set_PWM_dutycycle(RED_PIN, red)
        pi.set_PWM_dutycycle(GREEN_PIN, green)
        pi.set_PWM_dutycycle(BLUE_PIN, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
@app.route('/random', methods=['GET', 'POST'])
def random():
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = True
    if request.method == 'POST':
        red = randint(0,255)
        green = randint(0,255)
        blue = randint(0,255)
        pi.set_PWM_dutycycle(RED_PIN, red)
        pi.set_PWM_dutycycle(GREEN_PIN, green)
        pi.set_PWM_dutycycle(BLUE_PIN, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')

def setLights(pin, brightness, maxBright):
	realBrightness = int(int(brightness) * (float(maxBright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

def updateColor(color, step):
	color += step
	if color > 255:
		return 255
	if color < 0:
		return 0
	return color

def fadeMulti(speed, bright):
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = False
    STEPS = float(speed)/1000
    r = 255.0
    g = 0.0
    b = 0.0
    setLights(RED_PIN, r, bright)
    setLights(GREEN_PIN, g, bright)
    setLights(BLUE_PIN, b, bright)
    while abort == False:
    	if r == 255 and b == 0 and g < 255:
    		g = updateColor(g, STEPS)
    		setLights(GREEN_PIN, g, bright)
    	elif g == 255 and b == 0 and r > 0:
    		r = updateColor(r, -STEPS)
    		setLights(RED_PIN, r, bright)
    	elif r == 0 and g == 255 and b < 255:
    		b = updateColor(b, STEPS)
    		setLights(BLUE_PIN, b, bright)
    	elif r == 0 and b == 255 and g > 0:
    		g = updateColor(g, -STEPS)
    		setLights(GREEN_PIN, g, bright)
    	elif g == 0 and b == 255 and r < 255:
    		r = updateColor(r, STEPS)
    		setLights(RED_PIN, r, bright)
    	elif r == 255 and g == 0 and b > 0:
    		b = updateColor(b, -STEPS)
    		setLights(BLUE_PIN, b, bright)
    print ("Aborting Fade")

def fadeRGB(speed, bright):
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = False
    STEPS = float(speed)/1000
    r = 0.0
    g = 0.0
    b = 0.0
    up = True
    setLights(RED_PIN, r, bright)
    setLights(GREEN_PIN, g, bright)
    setLights(BLUE_PIN, b, bright)
    while abort == False:
        if r >= 255 or g >= 255 or b >=255:
            up = False
    	if up and r == 0 and b == 0 and g < 255:
            g = updateColor(g, STEPS)
            setLights(GREEN_PIN, g, bright)
    	elif not up and r == 0 and b == 0 and g > 10:
            g = updateColor(g, -STEPS)
            setLights(GREEN_PIN, g, bright)
        elif not up and r == 0 and b == 0 and g <= 10:
            g = 0.0
            b = 10.0
            setLights(GREEN_PIN, g, bright)
            setLights(BLUE_PIN, b, bright)
            up = True
    	if up and r == 0 and b < 255 and g == 0:
            b = updateColor(b, STEPS)
            setLights(BLUE_PIN, b, bright)
    	elif not up and r == 0 and b > 10 and g == 0:
            b = updateColor(b, -STEPS)
            setLights(BLUE_PIN, b, bright)
        elif not up and r == 0 and b <= 10 and g == 0:
            b = 0.0
            r = 10.0
            setLights(BLUE_PIN, b, bright)
            setLights(RED_PIN, r, bright)
            up = True
        if up and r < 255 and b == 0 and g == 0:
            r = updateColor(r, STEPS)
            setLights(RED_PIN, r, bright)
    	elif not up and r > 10 and b == 0 and g == 0:
            r = updateColor(r, -STEPS)
            setLights(RED_PIN, r, bright)
        elif not up and r <= 10 and b == 0 and g == 0:
            r = 0.0
            g = 10.0
            setLights(RED_PIN, r, bright)
            setLights(GREEN_PIN, g, bright)
            up = True
    print ("Aborting Fade")

def fadeGreen(speed, bright):
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = False
    STEPS = float(speed)/1000
    g = 255.0
    setLights(RED_PIN, 0.0, bright)
    setLights(GREEN_PIN, g, bright)
    setLights(BLUE_PIN, 0.0, bright)
    up = False
    while abort == False:
    	if up and g < 255:
            g = updateColor(g, STEPS)
        elif g >= 255:
            g = updateColor(g, -STEPS)
            up = False
        elif not up and g > 50:
            g = updateColor(g, -STEPS)
        else:
            g = updateColor(g, STEPS)
            up = True
        setLights(GREEN_PIN, g, bright)
    print ("Aborting Fade")

def fadeRed(speed, bright):
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = False
    STEPS = float(speed)/1000
    r = 255.0
    setLights(RED_PIN, r, bright)
    setLights(GREEN_PIN, 0.0, bright)
    setLights(BLUE_PIN, 0.0, bright)
    up = False
    while abort == False:
    	if up and r < 255:
            r = updateColor(r, STEPS)
        elif r >= 255:
            r = updateColor(r, -STEPS)
            up = False
        elif not up and r > 50:
            r = updateColor(r, -STEPS)
        else:
            r = updateColor(r, STEPS)
            up = True
        setLights(RED_PIN, r, bright)
    print ("Aborting Fade")

def fadeBlue(speed, bright):
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = False
    STEPS = float(speed)/1000
    b = 255.0
    setLights(RED_PIN, 0.0, bright)
    setLights(GREEN_PIN, 0.0, bright)
    setLights(BLUE_PIN, b, bright)
    up = False
    while abort == False:
    	if up and b < 255:
            b = updateColor(b, STEPS)
        elif b >= 255:
            b = updateColor(b, -STEPS)
            up = False
        elif not up and b > 50:
            b = updateColor(b, -STEPS)
        else:
            b = updateColor(b, STEPS)
            up = True
        setLights(BLUE_PIN, b, bright)
    print ("Aborting Fade")

@app.route('/fade', methods=['GET', 'POST'])
def fade():
    global RED_PIN
    global GREEN_PIN
    global BLUE_PIN
    global abort
    abort = True
    time.sleep(0.5)
    if request.method == 'POST':
        speed = request.form['speed']
        bright = request.form['bright']
        color = request.form['color']
        if color == 'Red':
            start_new_thread(fadeRed, (speed,bright))
        if color == 'Green':
            start_new_thread(fadeGreen, (speed,bright))
        if color == 'Blue':
            start_new_thread(fadeBlue, (speed,bright))
        if color == 'Multi':
            start_new_thread(fadeMulti, (speed,bright))
        if color == 'RGB':
            start_new_thread(fadeRGB, (speed,bright))
        return render_template('index.html',red=255, green=255, blue=255)
    if request.method == 'GET':
        return render_template('index.html',red=255, green=255, blue=255)
    else: #bad :(
        return render_template('bad.html')
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
