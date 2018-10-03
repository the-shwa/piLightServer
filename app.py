from flask import Flask, render_template, request
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
	pi.set_PWM_dutycycle(17, red)
	pi.set_PWM_dutycycle(22, green)
	pi.set_PWM_dutycycle(24, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
@app.route('/range', methods=['GET', 'POST'])
def range():
    #print('got here')
    if request.method == 'POST':
        red = request.form['red']
        green = request.form['green']
        blue = request.form['blue']
        pi.set_PWM_dutycycle(17, red)
        pi.set_PWM_dutycycle(22, green)
        pi.set_PWM_dutycycle(24, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
@app.route('/party', methods=['GET', 'POST'])
def party():
    if request.method == 'POST':
        red = randint(0,255)
        green = randint(0,255)
        blue = randint(0,255)
        pi.set_PWM_dutycycle(17, red)
        pi.set_PWM_dutycycle(22, green)
        pi.set_PWM_dutycycle(24, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
@app.route('/fade', methods=['GET', 'POST'])
def party():
    if request.method == 'POST':
        red = randint(0,255)
        green = randint(0,255)
        blue = randint(0,255)
        pi.set_PWM_dutycycle(17, red)
        pi.set_PWM_dutycycle(22, green)
        pi.set_PWM_dutycycle(24, blue)
        return render_template('index.html',red=red, green=green, blue=blue)
    if request.method == 'GET':
        return render_template('index.html',red=red, green=green, blue=blue)
    else: #bad :(
        return render_template('bad.html')
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
