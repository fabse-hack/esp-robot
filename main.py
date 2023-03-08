from dcmotor import DCMotor
from machine import Pin, SPI, PWM, I2C
import machine
import neopixel
from time import sleep
import urandom
import socket
import hcsr04
import time
import uasyncio as asyncio
import _thread
from ili9341 import Display, color565
from time import sleep
from xglcd_font import XglcdFont
import network

# --- PARAMETERS BEGINNING ---
# -- pin out numbers --
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
sensor = hcsr04.HCSR04(40, 44)

pin1 = Pin(39, Pin.OUT)    
pin2 = Pin(38, Pin.OUT)     
enablea = PWM(Pin(47), frequency)
pin3 = Pin(43, Pin.OUT)
pin4 = Pin(36, Pin.OUT)
enableb = PWM(Pin(48), frequency)

# dc motor parameter   
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enablea, enableb, 350, 1023)

# display + font
spi = SPI(2, baudrate=80000000, sck=Pin(12), mosi=Pin(11))
display = Display(spi, dc=Pin(3), cs=Pin(10), rst=Pin(8))

# Global Flags
stop_flag = False

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
        np = neopixel.NeoPixel(machine.Pin(2), 3)                                   # here is the neopixel in the buzzer loop
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
            sleep(randint(0.07,0.10))                                              # sleeping between the tones
        np.write()
    buzzer.deinit()
    for i in range(3):
        np[i] = (0, 0, 0)
    np.write()


# def accelerate(motor, start_speed, end_speed, time_step):                          # accelerate testing
#     speed = start_speed
#     while speed < end_speed:
#         motor.forward(speed)
#         speed += 1
#         time.sleep(time_step)

# # Beispielaufruf
# accelerate(dc_motor, 0, 20, 0.1)


def auto_mode():                                                                    # auto mode
    global stop_flag
    stop_flag = False
    dc_motor.forward(70)                                                            # forward without loop
    print('motor forward auto START')
    display_text('FORWARD AUTO  ')
    while not stop_flag:
        time.sleep(0.5)
        distance = sensor.distance_cm()                                             # check the distance TRUE?
        if distance <= 45:                                                          # 45 cm
            dc_motor.stop(0)                                                         # under 35cm STOP
            print('motor backwards auto')
            display_text('BACKWARD AUTO  ')
            dc_motor.backwards(70)                                                  # backwards
            time.sleep(0.8)
            dc_motor.stop(0) 	                                                    # stop
            time.sleep(0.3)
            if randint(0,1) == 0:                                                   # random 0 or 1, when 0
                dc_motor.left(50)                                                   # left
                print('auto_mode left')
                display_text('LEFT AUTO      ')
                time.sleep(0.4)
            else:
                dc_motor.right(50)                                                  # when 1 - right
                print('auto_mode right')
                display_text('RIGHT AUTO      ')
                time.sleep(0.4)
            dc_motor.stop(0)
            time.sleep(0.3)
            print('motor STOP AUTO + sleep')
            display_text('STOP AUTO       ')
            dc_motor.forward(70)                                                    # forward again
            display_text('FORWARD AUTO     ')
            print('auto_mode forward 20 end')

def stop_auto():
    global stop_flag
    stop_flag = True

async def handle_connection(reader, writer):                                        # handle connection reader and write from webserver
    html= """<!DOCTYPE html>
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
<div id="output"></div>
</form>


<form class="row">
<div><button class="button">
<pre>
___
 / () \ 
_|_____|_
| | === | |
|_|  O  |_|
||  O  ||
||__*__||
|~ \___/ ~|
 /=\ /=\ /=\ 
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

    request = await reader.read(1024)
    request = str(request)

    CMD_forward = request.find('/?CMD=forward')                                         # CMD Buttons on html site
    CMD_back = request.find('/?CMD=back')
    CMD_left = request.find('/?CMD=left')
    CMD_right = request.find('/?CMD=right')
    CMD_stop = request.find('/?CMD=stop')
    CMD_buzzer = request.find('/?CMD=buzzer')
    CMD_auto = request.find('/?CMD=auto')
    
    output = ''

    if CMD_forward == 6:
        print('+forward')
        stop_auto()
        print('+auto_stopped')
        dc_motor.forward(70)
        #display_text('FORWARD  ')
    elif CMD_back == 6:
        print('+backwards')
        stop_auto()
        dc_motor.backwards(70)
        #display_text('BACKWARD ')
    elif CMD_left == 6:
        print('+left')
        stop_auto()
        print('+auto_stopped')
        dc_motor.left(50)
        #display_text('LEFT     ')
    elif CMD_right == 6:
        print('+right')
        stop_auto()
        print('+auto_stopped')
        dc_motor.right(50)
        #display_text('RIGHT    ')
    elif CMD_stop == 6:
        print('+all_stop')
        dc_motor.stop(0)
        stop_auto()                                                                   # stop_auto() flag wird gesetzt
        #display_text('ALL STOP ')
    elif CMD_buzzer == 6:
        print('+buzzer')
        buzzer()
        display_text('BUZZER      ')
    elif CMD_auto == 6:
        print('+auto')
        display_text('AUTOMATIC   ')
        _thread.start_new_thread(auto_mode, ())
    
    output_div = '<div>' + output + '</div>'  # create new div with output
    html = html.replace('<div id="output"></div>', output_div)  # replace empty div with new div
    
    writer.write(html)
    await writer.drain()

    writer.close()
    await writer.wait_closed()

def display_screen():
    display.draw_text(20, 2, 'ESP ROBOT STATUS', XglcdFont('Code_Bold.c', 27, 28), color565(255, 255, 255))
    display.draw_text(2, 42, station.ifconfig()[0], XglcdFont('Code_Bold.c', 27, 28), color565(255, 255, 255))
    display.fill_hrect(0, 30, 320, 3, color565(128, 128, 128))
    display.draw_text(2, 82, 'BOOTING..     ', XglcdFont('Code_Bold.c', 27, 28), color565(255, 255, 255))

def display_text(text):
    display.draw_text(2, 82, text, XglcdFont('Code_Bold.c', 27, 28), color565(255, 255, 255))

async def web_server():                                                                 # this is the webserver start
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 80)
    await asyncio.sleep(10)
    await server.wait_closed()

if __name__ == "__main__":                                                              # normal python start
    _thread.start_new_thread(asyncio.run, (web_server(),))
    display_screen()