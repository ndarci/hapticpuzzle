import time
from gpiozero import RotaryEncoder, PWMOutputDevice, DigitalOutputDevice
import matplotlib.pyplot as plt 

class Motor():
    def __init__(self, sample_period, enc_a=27, enc_b=17, motor_enable=12, motor_direc=6):
        # encoder
        self.enc_a = enc_a
        self.enc_b = enc_b
        self.enc = RotaryEncoder(enc_a, enc_b, wrap = False, max_steps = 3740)
        # motor voltage
        self.motor_power = 0 # motor_power goes -12 to 12 (volts)
        self.voltlimit = 10
        # motor control
        self.enable_pin = PWMOutputDevice(motor_enable, frequency = 2000, initial_value = 0)
        self.direc_pin = DigitalOutputDevice(motor_direc, initial_value = 0)
        # physics variables
        self.pos = 0
        self.vel = 0
        self.acc = 0
        self.inertia_offset = 0.01
        self.friction_offset = -0.1
        self.sample_period = sample_period
        self.gravity = 1

    def update_vars(self):
        # calculate rates based on previous value
        newpos = self.enc.value * 100
        newvel = (newpos - self.pos) / self.sample_period
        newacc = (newvel - self.vel) / self.sample_period
        # set new position and rates
        self.pos = newpos
        self.vel = newvel
        self.acc = newacc
        print('pos:', self.pos, 'vel:', self.vel, 'acc:', self.acc)

    def threshold(self, power):
        threshx = 0.1
        threshy = 3
        slope = threshy / threshx
        outside_slope = (10 - threshy) / (10 - threshx)
        if abs(power) < threshx:
            voltage = slope * power
        elif power >= threshx:
            voltage = outside_slope * (power - threshx) + threshy
        elif power <= -1 * threshx:
            voltage = outside_slope * (power + threshx) - threshy
        return voltage

    def update_pwm(self):
        # inertia component
        newpower = -1 * self.inertia_offset * self.acc
        # friction component
        newpower += -1 * self.friction_offset * self.vel
        # gravity component
        newpower += self.gravity
        self.set_power(newpower)

    def __clean_power(self, rawpower):
        power = rawpower
        if rawpower > self.voltlimit:
            power =  self.voltlimit
        elif rawpower < -1 * self.voltlimit:
            power = -1 * self.voltlimit
        return power

    def set_power(self, power):
        power = self.threshold(power)
        power = self.__clean_power(power)

        # if changing direction, set pwm pin low to avoid having both high at once
        if power * self.motor_power < 0:
            self.enable_pin.value = 0
        
        if power < 0:
            self.direc_pin.value = 0
        elif power > 0:
            self.direc_pin.value = 1
        
        duty_cycle = abs(power/12)
        self.enable_pin.value = duty_cycle

    def spin(self):
        self.direc_pin.value = 1
        self.enable_pin.value = 0.5
        time.sleep(3)
        self.enable_pin.value = 0
        self.direc_pin.value = 0
