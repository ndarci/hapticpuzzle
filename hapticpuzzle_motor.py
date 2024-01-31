import time
from gpiozero import RotaryEncoder, PWMOutputDevice, DigitalOutputDevice
import matplotlib.pyplot as plt 

class Motor():
    def __init__(self, enc_a=27, enc_b=17, motor_enable=12, motor_direc=6):
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

    def update_vars(self):
        # calculate rates based on previous value
        newpos = self.enc.value * 100
        newvel = newpos - self.pos
        newacc = newvel - self.vel
        # set new position and rates
        self.pos = newpos
        self.vel = newvel
        self.acc = newacc
        # if self.vel != 0:
        print('pos:', self.pos, 'vel:', self.vel, 'acc:', self.acc)

    def threshold(self, power):
        thresh = 1
        slope = 3
        if abs(power) < thresh:
            voltage = slope * power
        else:
            voltage = (power - thresh) + (slope * thresh)
        return voltage

    def update_pwm(self):
        pwm = -10 * self.acc
        pwm += 5*self.vel
        self.set_power(pwm)

    def spin(self):
        self.direc_pin.value = 1
        self.enable_pin.value = 0.5
        time.sleep(3)
        self.enable_pin.value = 0
        self.direc_pin.value = 0 

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

