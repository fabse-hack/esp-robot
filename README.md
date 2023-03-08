# Welcome to ESP-Robot written in Micropython
***
## Requirements specification:
- [Welcome to ESP-Robot written in Micropython](#welcome-to-esp-robot-written-in-micropython)
  - [Requirements specification:](#requirements-specification)
  - [1. Overview](#1-overview)
  - [2. Wiring](#2-wiring)
  - [3. Lego Chassis](#3-lego-chassis)
  - [4. Lego DC Motors](#4-lego-dc-motors)
  - [5. Hardware](#5-hardware)
  - [6. Sensors](#6-sensors)
  - [7. Light](#7-light)
  - [8. Sound](#8-sound)
  - [9. the PROGRAMM](#9-the-programm)
  - [10. ESP Robot Self-Driving Logic](#10-esp-robot-self-driving-logic)
  - [11. To-Do's and planning:](#11-to-dos-and-planning)
***
<a name="overview"></a>  
## 1. Overview
![Logo](photos/ESP-Robot-Micropython4.png)

mp-remote commands:  
- this command upload the main.py to the micropython board over com11  
`python.exe -m mpremote connect com11 cp main.py :`  
- this command connects to the python prompt over com11  
`python.exe -m mpremote connect com11`  

***
<br>
<a name="wiring"></a>

## 2. Wiring
***
<br>

## 3. Lego Chassis
Yes, there are a lot of chassis on the market here. If you look closer, they are only made of sheet metal or fall apart just by looking at them. A modular base is needed - Lego!
The Robot is designed with Studio 2.0, here is the download link:
[Bricklink Studio 2.0](https://www.bricklink.com/v3/studio/download.page)
***
<br>

<a name="lego-dc-motors"></a>

## 4. Lego DC Motors
Of course, since the chassis is based on Lego, it's smart to use Lego motors.
2x Power Functions L
Here is the link:  
[Lego Power Functions L](https://www.bricklink.com/v2/catalog/catalogitem.page?S=88003-1)
***
<br>

<a name="hardware"></a>

## 5. Hardware
this is the hardware from the ESP Robot:
- PD-Delivery Board, with 9V for the L298N
	@@ -60,36 +45,23 @@ this is the hardware from the ESP Robot:
- Microcontroller
- Neopixel LED Strip with 3 LEDs

![Logo](photos/USB-CPowerDelivery.png)  
***
<br>

<a name="sensors"></a>

## 6. Sensors
HC-SR04
***
<br>

<a name="light"></a>

## 7. Light
The Robot defentily need some lights. "A robot needs a light to help it see in the dark, just like how humans need a flashlight!"
So the Robot get some wb2812b LEDs, easy to use and found much in the network. The ESP Robot have a 3 LEDs Strip wb2812b.
It's nice to have an adressable LED or high power LED or small Lasers. When they have 5V, it's easy to use them with a microcontroller.
***
<br>
<a name="sounds"></a>

## 8. Sound
Beeeep, Bep, Sound. It's very easy to you a piezo buzzer for make some R2D2 noises.
Some small piezo buzzer are avaiable in all electronic onlinestores.
THe R2D2 Sound from main.py is mixxed with the Neopixel LEDs, there are in the same coding loop, and then the light looks soundactiv.  
![Logo](photos/Buzzer.png)  
***  
<br>
<a name="programm"></a>

## 9. the PROGRAMM
Is the heart of the Robot, without, it's can do nothing!
For some month i learned Python, and so i programmed it in Micropython.
	@@ -99,26 +71,19 @@ dcmotor.py is the library for the DC Motor, there are the movements inside (forw
hcsr04.py is the library for the ultrasonic sensor, the distance is measured in centimeter.  
![Logo](photos/Touch-Controll-HTML.jpg)  
***
<br>
<a name="self-driving"></a>

## 10. ESP Robot Self-Driving Logic
What does the ESP Robot do? 
- Version 1: Forward, >35cm Distance measuring, Stop, Back, Left or Right, Forward again  
![Logo](photos/Auto1.gif)  
- some good links and thinkings:  
  - braitenberg-vehikel -> https://de.wikipedia.org/wiki/Braitenberg-Vehikel  
  - SLAM (with 360° Lidar or Linear Lidar, Jetson Board?)
***  
<br>
<a name="to-dos"></a>

## 11. To-Do's and planning:
- [x] new microcontroller ESP32-S2
- [ ] jetson nano / pi
- [ ] new models of the Lego Chassis, there is no end
- [ ] Programming it better, there is no end
- [ ] add some sensors e.g. ESP-Cam, Cam, one more HC-SR04, 360 Lidar, Linear Lidar
- [ ] new self-driving logic's
- [ ] Visualization and Photos
***