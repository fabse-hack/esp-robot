import machine
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin, machine.Pin.IN)
        self.speed_of_sound = 343  # Schallgeschwindigkeit in cm/s

    # Messung der Distanz in cm
    def distance_cm(self):
        self.trigger_pin.value(1)
        time.sleep_us(10)
        self.trigger_pin.value(0)

        while self.echo_pin.value() == 0:
            pass
        start_time = time.ticks_us()

        while self.echo_pin.value() == 1:
            pass
        end_time = time.ticks_us()

        pulse_duration = time.ticks_diff(end_time, start_time)

        distance = pulse_duration * self.speed_of_sound / 2 / 10000

        return distance
