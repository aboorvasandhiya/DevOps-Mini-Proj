import time

import RPi.GPIO as GPIO
from flask import Flask, render_template

from hal import hal_led as led
from hal import hal_input_switch as input_switch
from hal import hal_dc_motor as motor
from hal import hal_servo as servo
from hal import hal_usonic as usonic



app = Flask(__name__)


@app.route("/")
def index():

    templateData = {
        'title': 'ET0735 - Python Flask Raspberry Pi Demo',

    }
    return render_template('raspberry_pi.html', **templateData)




@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    if deviceName == 'Lights':
        if action == "on":
            on_light = led.set_output(1, 1)
        elif action == "off":
            off_light = led.set_output(1, 0)

    elif deviceName == 'Ceiling Fan':
        if action == "on":
           on_fan = motor.set_motor_speed(100)
        elif action == "off":
            off_fan = motor.set_motor_speed(0)

    elif deviceName == 'Door Lock':
        if action == "on":
            open_door = servo.set_servo_position(180)
        elif action == "off":
            close_door = servo.set_servo_position(0)


    elif deviceName == 'sensor':
        if action == "refresh":
            usonic_dist = usonic.get_distance()
            on_light = led.set_output(1, 1)




    # Read Sensors Status
    buttonSts = input_switch.read_slide_switch()
    usonic_dist = usonic.get_distance()
    close_door = servo.set_servo_position(0)
    open_door = servo.set_servo_position(180)
    off_fan = motor.set_motor_speed(0)
    on_fan = motor.set_motor_speed(100)
    off_light = led.set_output(1, 0)

    templateData = {
        'title': 'ET0735 - Python Flask Raspberry Pi Demo',
        'button': buttonSts,
        'usonic_dist': usonic_dist

    }

    return render_template('raspberry_pi.html', **templateData)


if __name__ == "__main__":
    led.init()
    input_switch.init()
    motor.init()
    servo.init()
    usonic.init()



    #Run Python Flask Web Server
    app.run(host='0.0.0.0', port=8080, debug=True)
