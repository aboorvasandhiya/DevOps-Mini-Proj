import mfrc522
from flask import Flask, render_template
from hal import hal_rfid_reader as RFID
from hal import hal_usonic as usonic
from hal import hal_lcd as LCD
from hal import hal_keypad as keypad
from hal import hal_buzzer as buzzer
from hal import hal_servo as servo
from hal import hal_dc_motor as motor
from hal import hal_led as led
from time import sleep
from threading import Thread
from hal import hal_temp_humidity_sensor as temp
from hal import hal_input_switch as input_switch
from hal import hal_adc as adc


status = 0
pin_input = []
password1 = [1, 2, 3, 4]
password2 = [2, 3, 4, 5]
password3 = [3, 4, 5, 6]


def thread_RFID():
        LCD1 = LCD.lcd()
        LCD1.lcd_clear()
        LCD1.lcd_display_string("Enter PIN or", 1)
        LCD1.lcd_display_string("tap card on reader", 2)
       
        ID1 = 948765671378
        ID2 = 644721127290
        
        while True:
                reader = RFID.init()
                id1 = reader.read_id_no_block()
                if (ID1 == id1) or (ID2 == id1):
                    
                    servo.set_servo_position(90)
                    status = 1
                    LCD1.lcd_clear()
                    LCD1.lcd_display_string("You may enter now.   ", 1)
                    distance = 100
                    while distance > 10:
                        distance = usonic.get_distance()
                        print("Measured distance = {0:0.1f} cm".format(distance))
                        sleep(1.0)
                    servo.set_servo_position(0)
                    status = 0
                    LCD1.lcd_display_string("Enter PIN or    ", 1)
                    LCD1.lcd_display_string("tap card on reader", 2)
                
                elif (id1 != None):
                    LCD1.lcd_display_string("Invalid card", 1)
                    sleep(2)
                    LCD1.lcd_display_string("Enter PIN or    ", 1)
                    LCD1.lcd_display_string("tap card on reader", 2)

def thread_keypad(key):
        LCD1 = LCD.lcd()
        pin_input.append(key)
        print(pin_input)
        LCD1.lcd_display_string("Enter Pin", 1)
        
        if len(pin_input) == 4:
            if pin_input == password1 or pin_input == password2 or pin_input == password3:
                servo.set_servo_position(90)
                status = 1
                LCD1.lcd_display_string("You may enter now.   ", 1)
                distance = 100
                while distance > 10:
                    distance = usonic.get_distance()
                    print("Measured distance = {0:0.1f} cm".format(distance))
                    sleep(1.0)
                servo.set_servo_position(0)
                status = 0
                pin_input.clear()
                LCD1.lcd_display_string("Enter PIN or    ", 1)
                LCD1.lcd_display_string("tap card on reader", 2)
        
            else:
                LCD1.lcd_display_string("Invalid Password.   ", 1)
                sleep(2)
                pin_input.clear()
                LCD1.lcd_display_string("Enter PIN or    ", 1)
                LCD1.lcd_display_string("tap card on reader", 2)

def thread_Alarm():
    buzzer.init()

    while True:

        if (status == 0) and (usonic.get_distance() < 10):  #change >
            buzzer.short_beep(0.5)
            sleep(1)

def adc_read_ldr():
    state = True
    while(state):

        ldr_value = adc.get_adc_value()
        if ldr_value <300:
            ldr_status = "dark"
        elif ldr_value <500 and ldr_value>300:
            ldr_status = "Normal Brightness"
        if ldr_value <800 and ldr_value>500:
            ldr_status = "Very bright"
        state = False

    return ldr_status

def thread_webserver():
    app = Flask(__name__)

    @app.route("/")
    def index():
        templateData = {
            'title': 'ET0735 - Python Flask Raspberry Pi Demo',

        }
        return render_template('raspberry_pi.html', **templateData)


    @app.route("/<deviceName>/<action>")
    def action(deviceName, action):
        if deviceName == 'Light':
            if action == "on":
                led.set_output(1, 1)
            elif action == "off":
                led.set_output(1, 0)

        elif deviceName == 'Ceiling Fan':
            if action == "on":
                motor.set_motor_speed(100)
            elif action == "off":
                motor.set_motor_speed(0)

        elif deviceName == 'Door':
            if action == "open":
                servo.set_servo_position(180)
            elif action == "lock":
                servo.set_servo_position(0)

        elif deviceName == 'Sensor':
            if action == "Refresh":
                temp_show = temp.read_temp_humidity()
                brightness = adc_read_ldr()

        # Read Sensors Status
        buttonSts = input_switch.read_slide_switch()
        temp_show = temp.read_temp_humidity()
        brightness = adc_read_ldr()

        templateData = {
            'title': 'ET0735 - Python Flask Raspberry Pi Demo',
            'button': buttonSts,
            'temp_show': temp_show,
            'brightness': brightness,
        }
        return render_template('raspberry_pi.html', **templateData)

    app.run(host='0.0.0.0', port=8080, debug=True)


def main():
    #initialise 
    
    keypad.init(thread_keypad)
    servo.init()
    usonic.init()
    led.init()
    input_switch.init()
    motor.init()
    servo.init()
    usonic.init()
    temp.init()
    adc.init()

    #threading
    T_ALARM = Thread(target = thread_Alarm)
    T_RFID = Thread(target = thread_RFID)
    T_KEY = Thread(target = keypad.get_key)
    T_WEB= Thread(target=thread_webserver)

    # Instantiate and initialize the LCD driver
    LCD1 = LCD.lcd()

    sleep(0.5)
    LCD1.backlight(0)  # turn backlight off

    sleep(0.5)
    LCD1.backlight(1)  # turn backlight on
    
    T_RFID.start()
    T_KEY.start()
    T_WEB.start()
    T_ALARM.start()
if __name__ == "__main__":
    main()
