from dcmotor import DCMotor
from machine import Pin, SPI, PWM, SoftI2C
import machine
import neopixel
from time import sleep
import urandom
import hcsr04
import time
import uasyncio as asyncio
import ADXL345
from ili934xnew import ILI9341, color565
import tt32
import network
import gc
#from qmc5883 import QMC5883
#from hmc5883l import HMC5883L

# --- PARAMETERS BEGINNING ---
# -- pin out numbers --
# pin 2: neopixel
# pin 21: buzzer
# pin 40: hc-sr04 trigger
# pin 44: hc-sr04 echo
# pin 39: pin1
# pin 38: pin2
# pin 47: enablea
# pin 43: pin3
# pin 36: pin4
# pin 48: enableb
# pin 12: sck display
# pin 11: mosi display
# pin 3 : dc display
# pin 10: cs display
# pin 8 : rst display
frequency = 15000
# pins for HC-SR04
sensor = hcsr04.HCSR04(40, 44)
# pins for L298N
pin1 = Pin(39, Pin.OUT)    
pin2 = Pin(38, Pin.OUT)     
enablea = PWM(Pin(47), frequency)
pin3 = Pin(43, Pin.OUT)
pin4 = Pin(36, Pin.OUT)
enableb = PWM(Pin(48), frequency)
# dc motor parameter   
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enablea, enableb, 350, 1023)
# pins for display + font
spi = SPI(2, baudrate=80000000, sck=Pin(12), mosi=Pin(11))
display = ILI9341(spi, dc=Pin(3), cs=Pin(10), rst=Pin(8), w=320, h=240, r=3)
# Global Flags
stop_flag = False
# ADXL345
i2c = SoftI2C(scl=Pin(15),sda=Pin(16), freq=400000)
adx = ADXL345.ADXL345(i2c)
# --- PARAMETERS END ---

#compass = HMC5883L(scl=6, sda=7)


def randint(min, max):                                                              # randint (random integer)
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

async def buzzer():
    buzzer = PWM(Pin(21, Pin.OUT), freq=randint(140,400), duty=randint(112,300))    # pin, freq, duty
    for i in range(randint(3,10)):                                                  # buzzer loop
        np = neopixel.NeoPixel(machine.Pin(2), 3)                                   # here is the neopixel in the buzzer loop, Neopixel on pin2 and 3 leds
        np2 = neopixel.NeoPixel(machine.Pin(48), 1)
        for pixel_id in range(0, len(np)):                                          # random color neopixel
            red = randint(0, 255)                                                   # red / green / blue random integer 0 to 255
            green = randint(0, 255)
            blue = randint(0, 255)
            np[pixel_id] = (red, green, blue)                                       # set the color to the neopixel strip
        for pixel_id in range(0, len(np2)):                                          # random color neopixel
            red = randint(0, 255)                                                   # red / green / blue random integer 0 to 255
            green = randint(0, 255)
            blue = randint(0, 255)
            np2[pixel_id] = (red, green, blue)                                       # set the color to the neopixel strip
        buzzer.freq(randint(150,400))
        await asyncio.sleep(randint(0.07,0.10))                                     # sleeping between the tones
        np.write()                                                                  # writing color to the pixel strip
        np2.write()
    buzzer.deinit()
    for i in range(3):
        np[i] = (0, 0, 0)                                                           # turn off Neopixel
    np.write()
    np2[0] = (0, 0, 0)
    np2.write()

# def accelerate(motor, start_speed, end_speed, time_step):                          # accelerate testing / is now in the DC Library from def stop()
#     speed = start_speed
#     while speed < end_speed:
#         motor.forward(speed)
#         speed += 1
#         time.sleep(time_step)

# # Beispielaufruf
# accelerate(dc_motor, 0, 20, 0.1)


async def auto_mode():                                                                    # auto mode
    global stop_flag                                                                # global flag
    stop_flag = False
    dc_motor.forward(60)                                                            # forward without loop
    display_text('FORWARD')
    while not stop_flag:
        await asyncio.sleep(0.5)
        distance = sensor.distance_cm()                                             # check the distance TRUE?
        if distance <= 15:                                                          # 45 cm
            dc_motor.stop(0)                                                         # under 35cm STOP
            display_text('BACKWARD')
            dc_motor.backwards(65)                                                  # backwards
            await asyncio.sleep(0.8)
            dc_motor.stop(0) 	                                                    # stop
            await asyncio.sleep(0.3)
            if randint(0,1) == 0:                                                   # random 0 or 1, when 0
                dc_motor.left(60)                                                   # left
                display_text('LEFT AUTO')
                await asyncio.sleep(0.6)
            else:
                dc_motor.right(60)                                                  # when 1 - right
                display_text('RIGHT AUTO')
                await asyncio.sleep(0.6)
            dc_motor.stop(0)
            await asyncio.sleep(0.5)
            display_text('STOP AUTO')
            dc_motor.forward(60)                                                    # forward again
            display_text('FORWARD')

def stop_auto():                                                                    # stop_auto
    global stop_flag                                                                # global flag
    stop_flag = True

async def handle_connection(reader, writer):                                        # handle connection reader and write from webserver
    with open('robot.html', 'r') as f:
        html = f.read()
    
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
        display_text('FORWARD')                                                      # the display text is still laggy ....
    elif CMD_back == 6:
        print('+backwards')
        stop_auto()
        dc_motor.backwards(70)
        display_text('BACKWARD')
    elif CMD_left == 6:
        print('+left')
        stop_auto()
        print('+auto_stopped')
        dc_motor.left(50)
        display_text('LEFT')
    elif CMD_right == 6:
        print('+right')
        stop_auto()
        print('+auto_stopped')
        dc_motor.right(50)
    elif CMD_stop == 6:
        print('+all_stop')
        dc_motor.stop(0)
        stop_auto()                                                                   # set stop_auto() flag
        display_text('ALL STOP')
    elif CMD_buzzer == 6:
        print('+buzzer')
        display_text('BUZZER')
        asyncio.create_task(buzzer())
    elif CMD_auto == 6:
        print('+auto')
        display_text('AUTOMATIC')
        asyncio.create_task(auto_mode())
        #asyncio.create_task(txt_writing())
    
    output_div = '<div>' + output + '</div>'                                        # create new div with output
    html = html.replace('<div id="output"></div>', output_div)                      # replace empty div with new div
    
    writer.write(html)
    await writer.drain()

    writer.close()
    await writer.wait_closed()

def display_text(text):                                                             # definition for the display text with font
    display.set_font(tt32)
    display.fill_rectangle(x=120, y=50, w=197, h=30)
    display.print2(text, x=120, y=50)
    
def dashboard():
    display.erase()
    display.print2("ESP-Robot", x=80, y=8)
    display.print2("Status:", x=10, y=50)
    display.print2("booting...", x=120, y=50)
    display.print2("Compass", x=5, y=84)
    display.print2("Distance", x=194, y=84)
    display.print2("cm", x=260, y=115)
    display.fill_rectangle(x=0, y=0, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=0, y=0, w=2, h=240, color=0xF800)
    display.fill_rectangle(x=228, y=0, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=0, y=42, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=0, y=46, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=0, y=81, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=0, y=238, w=320, h=2, color=0xF800)
    display.fill_rectangle(x=180, y=81, w=2, h=159, color=0xF800)
    display.fill_rectangle(x=318, y=0, w=2, h=240, color=0xF800)

async def dash_1():
    while True:
        distance1 = int(sensor.distance_cm())
        x = adx.xValue
        y = adx.yValue
        display.print2("x: %d, y: %d" % (x, y), x=2, y=155)
        display.print2('%03d' % distance1, x=194, y=115)
        await asyncio.sleep(0.5)

async def web_server():                                                                 # this is the webserver start
    server = await asyncio.start_server(handle_connection, "0.0.0.0", 80)
    await asyncio.sleep(10)
    await server.wait_closed()

async def txt_writing():
    with open('daten.txt', 'a') as f:
        while True:
            abstand = sensor.distance_cm()
            x = adx.xValue
            y = adx.yValue
            now = time.time()
            seconds = int(now)
            local_time = time.localtime(seconds)
            hour = local_time[3]
            minute = local_time[4]
            second = local_time[5]
            time_string = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
            f.write(time_string + ',' + str(abstand) + ',' + str(x) + ',' + str(y) + '\n')
            await asyncio.sleep(1)

async def main():
    task1 = asyncio.create_task(web_server())
    #task2 = asyncio.create_task(txt_writing())
    task3 = asyncio.create_task(dash_1())
    await asyncio.gather(task1, task3)


def configure_wifi():
    def connect_to_wifi(ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if not wlan.isconnected():
            print('Verbindung zum WLAN herstellen...')
            wlan.connect(ssid, password)
            while not wlan.isconnected():
                pass
        print('Verbunden mit:', ssid)
        print('IP-Adresse:', wlan.ifconfig()[0])

    def create_access_point(ssid, password):
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password)
        print('Access Point erstellt:')
        print('SSID:', ssid)
        print('Passwort:', password)
        print('IP-Adresse:', ap.ifconfig()[0])

    desired_ssid = 'idontknow'
    desired_password = 'dumdidum'
    ap_ssid = 'ESP-Robot'
    ap_password = '12345678'

    try:
        connect_to_wifi(desired_ssid, desired_password)
    except:
        print('Verbindung zum WLAN nicht möglich. Erstelle Access Point...')
        create_access_point(ap_ssid, ap_password)


if __name__ == "__main__":
    configure_wifi()
    dashboard()
    asyncio.run(main())