# Overview from the programm - written in micropython
🚀 check micropython for more informations: [Micropython](https://micropython.org/)  
🐫 check micropython libraries: [Micropython Libraries](https://docs.micropython.org/en/latest/library/index.html)

The Robot use this python scripts:
1. boot.py  
2. main.py  
3. hcsr04.py  
4. dsmotor.py  
***
## 1. boot.py

```
import network
import gc


ssid = 'your-SSID'                # here is your wifi ssid
password = 'dumdidum'             # here is your wifi password

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)   # connect to wifi

while station.isconnected() == False:
  pass

print('Connection successful')    # if it connected -> success
print(station.ifconfig())

gc.collect()                      # garbage collector
```
to-do:  
- [ ] Wifi connection fallback

***
## 2. main.py
```
from dcmotor import DCMotor       
from machine import Pin, PWM
import neopixel 
from time import sleep
import machine
import urandom
import socket
import hcsr04
import time

# pin out number
# pin 15 neopixel / hcsr04 trigger
# pin 14 buzzer   / hcsr04 echo
# pin 5
# pin 4
# pin 13 enable
# pin 0
# pin 2
# pin 12 enable2

# pins to sensor / gadget / activator
sensor = hcsr04.HCSR04(15, 14)
pin1 = Pin(5, Pin.OUT)    
pin2 = Pin(4, Pin.OUT)     
enable = PWM(Pin(13), frequency)
pin3 = Pin(0, Pin.OUT)
pin4 = Pin(2, Pin.OUT)
enable2 = PWM(Pin(12), frequency)

# dc motor parameter
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enable, enable2)      
dc_motor = DCMotor(pin1, pin2, pin3, pin4, enable, enable2, 350, 1023)

# parameters
frequency = 15000

# randint (random integer)
def randint(min, max):
    span = max - min + 1
    div = 0x3fffffff // span
    offset = urandom.getrandbits(30) // div
    val = min + offset
    return val

# buzzer and neopixel
def buzzer():
    buzzer = PWM(Pin(14, Pin.OUT), freq=randint(140,400), duty=randint(112,300))    # pin, freq, duty
    for i in range(randint(3,10)):                                                  # buzzer loop
        np = neopixel.NeoPixel(machine.Pin(15), 3)                                  # here is the neopixel in the buzzer loop
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


def web_server():                                                                   # definition web server
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
```

***
## 3. hcsr04.py
```
import machine
import time

class HCSR04:
    # Initialisierung des Sensors
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin, machine.Pin.IN)
        self.speed_of_sound = 343  # Schallgeschwindigkeit in cm/s

    # Messung der Distanz
    def distance_cm(self):
        # Senden des Triggersignals
        self.trigger_pin.value(1)
        time.sleep_us(10)
        self.trigger_pin.value(0)

       # Wait for the echo pin to go high
        while self.echo_pin.value() == 0:
            pass
        start_time = time.ticks_us()

        # Wait for the echo pin to go low
        while self.echo_pin.value() == 1:
            pass
        end_time = time.ticks_us()


        pulse_duration = time.ticks_diff(end_time, start_time)

        # Calculate the distance to the object in cm
        distance = pulse_duration * self.speed_of_sound / 2 / 10000

        return distance
 
 ```
 
 ***
 ## 4. dcmotor.py
 
 ```
 class DCMotor:      
  def __init__(self, pin1, pin2, pin3, pin4, enable_pin, enable2_pin, min_duty=750, max_duty=1023):
    self.pin1=pin1
    self.pin2=pin2
    self.pin3=pin3
    self.pin4=pin4
    self.enable_pin=enable_pin
    self.enable_pin2=enable2_pin
    self.min_duty = min_duty
    self.max_duty = max_duty

  def forward(self,speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.enable_pin2.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)
    self.pin3.value(1)
    self.pin4.value(0)

  def right(self,speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.enable_pin2.duty(self.duty_cycle(self.speed))
    self.pin1.value(1)
    self.pin2.value(0)
    self.pin3.value(0)
    self.pin4.value(1)
    
  def left(self,speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.enable_pin2.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)
    self.pin3.value(1)
    self.pin4.value(0)
    
  def backwards(self, speed):
    self.speed = speed
    self.enable_pin.duty(self.duty_cycle(self.speed))
    self.pin1.value(0)
    self.pin2.value(1)
    self.pin3.value(0)
    self.pin4.value(1)

  def stop(self):
    self.enable_pin.duty(0)
    self.pin1.value(0)
    self.pin2.value(0)
    self.pin3.value(0)
    self.pin4.value(0)
    
  def duty_cycle(self, speed):
   if self.speed <= 0 or self.speed > 100:
        duty_cycle = 0
   else:
    duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed-1)/(100-1)))
    return duty_cycle
```
