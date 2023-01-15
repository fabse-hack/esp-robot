from dcmotor import DCMotor       
from machine import Pin, PWM
import neopixel 
from time import sleep
import machine
import urandom
import socket
import hcsr04
import time


sensor = hcsr04.HCSR04(15, 14)
# pin 15 neopixel / hcsr04 trigger
# pin 14 buzzer   / hcsr04 echo
# pin 5
# pin 4
# pin 13 enable
# pin 0
# pin 2
# pin 12 enable2

frequency = 15000

pin1 = Pin(5, Pin.OUT)    
pin2 = Pin(4, Pin.OUT)     
enable = PWM(Pin(13), frequency)
pin3 = Pin(0, Pin.OUT)
pin4 = Pin(2, Pin.OUT)
enable2 = PWM(Pin(12), frequency)


dc_motor = DCMotor(pin1, pin2, pin3, pin4, enable, enable2)      
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enable, enable2, 350, 1023)

def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val


def buzzer():
    buzzer = PWM(Pin(14, Pin.OUT), freq=randint(140,400), duty=randint(112,300))
    for i in range(randint(3,10)):
        np = neopixel.NeoPixel(machine.Pin(15), 3)
        for pixel_id in range(0, len(np)):
            red = randint(0, 255)
            green = randint(0, 255)
            blue = randint(0, 255)
            np[pixel_id] = (red, green, blue)
        tones = {
            'c': randint(150,400),
            }
        melody = 'c'
        rhythm = [8]
        for tone, length in zip(melody, rhythm):
            buzzer.freq(tones[tone])
            sleep(randint(0.07,0.10))
        np.write()
    buzzer.deinit()
    for i in range(3):
        np[i] = (0, 0, 0)
    np.write()


# import time

# def accelerate(motor, start_speed, end_speed, time_step):
#     speed = start_speed
#     while speed < end_speed:
#         motor.forward(speed)
#         speed += 1
#         time.sleep(time_step)

# # Beispielaufruf
# accelerate(dc_motor, 0, 20, 0.1)


def auto_mode():
    dc_motor.forward(20)
    print('motor forward auto START')
    while True:
        distance = sensor.distance_cm()
        if distance <= 35:
            # Halt an, fahre ein Stück rückwärts
            dc_motor.stop()
            print('motor backwards auto')
            dc_motor.backwards(30)
            time.sleep(0.8)
            dc_motor.stop()
            time.sleep(0.3)
            # Wähle zufällig eine Richtung zum Ausweichen
            if randint(0,1) == 0:
                dc_motor.left(20)
                print('motor left auto')
                time.sleep(0.5)
            else:
                dc_motor.right(20)
                print('motor right auto')
                time.sleep(0.5)
            dc_motor.stop()
            time.sleep(0.3)
            print('motor STOP AUTO + sleep')
            dc_motor.forward(20)
            print('motor forward auto END')


def web_server():
    html = """<!DOCTYPE html>
    <html>
    <head>
    <title>RoBoT</title>
    <style>
    body {background-color: #1f1f1f}
    h1 {color:#4643ff}

    button {
            color: #4643ff;
            height: 180px;
            font-family: monospace;
            width: 180px;
            background:#000000;
            border: 1px solid #cac253;
            border-radius: 20%;
            font-size: 250%;
            position: center;
    }
    </style>
    </head>
    <body>
    <center><h1>RoBoT</h1>
    <form>
    <div><button name="CMD" value="forward" type="submit">Forward</button></div>
    <div><button name="CMD" value="left" type="submit">Left</button>
    <button name="CMD" value="stop" type="submit">Stop</button>
    <button name="CMD" value="right" type="submit">Right</button></div>
    <div><button name="CMD" value="back" type="submit">Back</button></div>
    <div><button name="CMD" value="buzzer" type="submit">buzzer</button>
    <button name="CMD" value="auto" type="submit">Auto</button></div>
    </form>
    </center>
    </body>
    </html>
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(10)
    print("Listening, connect your browser to http://<this_host>:80/")
    
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Press-Button")
        request = str(request)

        CMD_forward = request.find('/?CMD=forward')
        CMD_back = request.find('/?CMD=back')
        CMD_left = request.find('/?CMD=left')
        CMD_right = request.find('/?CMD=right')
        CMD_stop = request.find('/?CMD=stop')
        CMD_buzzer = request.find('/?CMD=buzzer')
        CMD_auto = request.find('/?CMD=auto')

        if CMD_forward == 6:
            print('+forward')
            dc_motor.forward(40)
        elif CMD_back == 6:
            print('+backwards')
            dc_motor.backwards(40)
        elif CMD_left == 6:
            print('+left')
            dc_motor.left(28)
        elif CMD_right == 6:
            print('+right')
            dc_motor.right(28)
        elif CMD_stop == 6:
            print('+stop')
            dc_motor.stop()
        elif CMD_buzzer == 6:
            print('+buzzer')
            buzzer()
        elif CMD_auto == 6:
            print('+auto')
            auto_mode()
        response = html
        conn.sendall(response)

web_server()
