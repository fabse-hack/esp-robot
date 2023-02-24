from dcmotor import DCMotor
from machine import Pin, PWM
import neopixel
from time import sleep
import machine
import urandom
import socket
import hcsr04
import time
import uasyncio as asyncio

# --- PARAMETERS BEGINNING ---
# pin out number
# pin 20: neopixel
# pin 21: buzzer
# pin 35: hc-sr04 trigger
# pin 45: hc-sr04 echo
# pin 39: pin1
# pin 38: pin2
# pin 47: enablea
# pin 37: pin3
# pin 36: pin4
# pin 48: enableb

frequency = 15000

# pins to sensor / gadget / activator
sensor = hcsr04.HCSR04(35, 45)
pin1 = Pin(39, Pin.OUT)    
pin2 = Pin(38, Pin.OUT)     
enablea = PWM(Pin(47), frequency)
pin3 = Pin(37, Pin.OUT)
pin4 = Pin(36, Pin.OUT)
enableb = PWM(Pin(48), frequency)

# dc motor parameter   
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enablea, enableb, 350, 1023)


# --- PARAMETERS END ---

# randint (random integer)
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

# buzzer and neopixel
def buzzer():
    buzzer = PWM(Pin(21, Pin.OUT), freq=randint(140,400), duty=randint(112,300))    # pin, freq, duty
    for i in range(randint(3,10)):                                                  # buzzer loop
        np = neopixel.NeoPixel(machine.Pin(2), 3)                                  # here is the neopixel in the buzzer loop
        for pixel_id in range(0, len(np)):                                          # random color neopixel
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
            sleep(randint(0.07,0.10))                                               # sleeping between the tones
        np.write()
    buzzer.deinit()
    for i in range(3):
        np[i] = (0, 0, 0)
    np.write()


# import time

# def accelerate(motor, start_speed, end_speed, time_step):                         # accelerate testing
#     speed = start_speed
#     while speed < end_speed:
#         motor.forward(speed)
#         speed += 1
#         time.sleep(time_step)

# # Beispielaufruf
# accelerate(dc_motor, 0, 20, 0.1)


def auto_mode():                                                                    # auto mode
    dc_motor.forward(20)                                                            # forward without loop
    print('motor forward auto START')
    while True:
        distance = sensor.distance_cm()                                             # check the distance TRUE?
        if distance <= 35:                                                          # 35 cm
            dc_motor.stop()                                                         # under 35cm STOP
            print('motor backwards auto')
            dc_motor.backwards(30)                                                  # backwards
            time.sleep(0.8)
            dc_motor.stop() 	                                                    # stop
            time.sleep(0.3)
            if randint(0,1) == 0:                                                   # random 0 or 1, when 0
                dc_motor.left(20)                                                   # left
                print('motor left auto')
                time.sleep(0.5)
            else:
                dc_motor.right(20)                                                  # when 1 - right
                print('motor right auto')
                time.sleep(0.5)
            dc_motor.stop()
            time.sleep(0.3)
            print('motor STOP AUTO + sleep')
            dc_motor.forward(20)                                                    # forward again
            print('motor forward auto END')


async def web_server():                                                                   # definition web server
    html = """<!DOCTYPE html>
<html>
<head>
<style>
body {
background-color: #1b1b1b;
color: #ffffff
}
.row {
display: flex;
justify-content: center;
font-size: 20px;
padding-top: 10 px;
}
.button {
margin-right: 10px;
background-color: #181818;
color: #ffffff;
font-size: 20px;
border: 0;
}
.button:hover {
background-color: #585858;
}
.button:active {
background-color: #838383;
}
</style>
</head>
<body>
<form class="row">
<div><button class="button">
<pre>
___
 / () \.
_|_____|_
| | === | |
|_|  O  |_|
||  O  ||
||__*__||
|~ \___/ ~|
/=\  /=\  /=\.
</pre>
</button></div>
</form>
<form class="row">
<div><button class="button" name="CMD" value="forward" type="submit">
<pre>
 -*-*-*-*-*-
#           #
#  Forwards #
#           #
 -*-*-*-*-*-
</pre>
</button></div>
</form>
<form class="row">
<div><button class="button" name="CMD" value="left" type="submit">
<pre>
 -*-*-*-*-*-
#           #
#   Left    #
#           #
 -*-*-*-*-*-
</pre>
</button></div>
<div><button class="button" name="CMD" value="stop" type="submit">
<pre>
 -*-*-*-*-*-
#           #
#   Stop    #
#           #
 -*-*-*-*-*-
</pre>
</button></div>
<div><button class="button" name="CMD" value="right" type="submit">
 <pre>
 -*-*-*-*-*-
#           #
#   Right   #
#           #
 -*-*-*-*-*-
</pre>
</button></div>
</form>
<form class="row">
<div><button class="button" name="CMD" value="backward" type="submit">
<pre>
 -*-*-*-*-*-
#           #
# Backwards #
#           #
 -*-*-*-*-*-
</pre>
</button></div>
</form>
<form class="row">
<div><button class="button" name="CMD" value="auto" type="submit">
<pre>
-*-*-*-*-*-
#           #
#   Auto    #
#           #
-*-*-*-*-*-
</pre>
</button></div>
<div><button class="button" name="CMD" value="buzzer" type="submit">
<pre>
-*-*-*-*-*-
#           #
#  Buzzer   #
#           #
-*-*-*-*-*-
</pre>
</button></div>
</form>
</body>
</html>
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(1)
    
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
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
        conn.sendall(html)
        conn.close()

if __name__ == "__main__":
        asyncio.run(web_server())