import machine
import time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo_pin = machine.Pin(echo_pin, machine.Pin.IN)
        self.speed_of_sound = 343
        self.echo_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self._echo_handler)
        self.start_time = 0
        self.end_time = 0
        self.pulse_duration = 0
        self.measurement_complete = False

    def _echo_handler(self, pin):
        if self.echo_pin.value():
            self.start_time = time.ticks_us()
        else:
            self.end_time = time.ticks_us()
            self.pulse_duration = time.ticks_diff(self.end_time, self.start_time)
            self.measurement_complete = True

    def distance_cm(self):
        self.trigger_pin.value(1)
        time.sleep_us(10)
        self.trigger_pin.value(0)
        while not self.measurement_complete:
            pass
        distance = self.pulse_duration * self.speed_of_sound / 2 / 10000
        distance = min(round(distance, 2), 999)
        self.start_time = 0
        self.end_time = 0
        self.pulse_duration = 0
        self.measurement_complete = False
        
        return distance
