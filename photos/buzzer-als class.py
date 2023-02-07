from machine import Pin, PWM
import urandom
from time import sleep

class buzzer:

    def randint(min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val


    def buzzer():
        buzzer = PWM(Pin(14, Pin.OUT), freq=randint(140,400), duty=randint(112,300))
        y = randint(3,10)
        for i in range(y):
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
                z = randint(0.07,0.10)
                sleep(z)
            np.write()
    #        time.sleep_ms(100)
        buzzer.deinit()
        for i in range(3):
            np[i] = (0, 0, 0)
        np.write()
        
    def np():
        for i in range(10):
            np = neopixel.NeoPixel(machine.Pin(15), 3)
            for pixel_id in range(0, len(np)):
                red = randint(0, 60)
                green = randint(0, 60)
                blue = randint(0, 60)

                np[pixel_id] = (red, green, blue)
            np.write()
            time.sleep_ms(100)
        for i in range(3):
            np[i] = (0, 0, 0)
        np.write()


    def np_clear():
        np = neopixel.NeoPixel(machine.Pin(15), 3)
        for i in range(3):
            np[i] = (0, 0, 0)
        np.write()
