import time
from gpiozero import RotaryEncoder, PWMOutputDevice, DigitalOutputDevice


class Motor():
    def __init__(self, enc_a=27, enc_b=17, motor_enable=12, motor_direc=6):
        self.enc_a = enc_a
        self.enc_b = enc_b
        self.enc = RotaryEncoder(enc_a, enc_b, wrap = False, max_steps = 3412)
        self.motor_power = 0 # motor_power goes -12 to 12 (volts)
        self.enable_pin = PWMOutputDevice(motor_enable, frequency = 2000, initial_value = 0)
        self.direc_pin = DigitalOutputDevice(motor_direc, initial_value = 0)

    def read(self):
        return self.enc.value

    def spin(self):
        self.direc_pin.value = 1
        self.enable_pin.value = 0.5
        time.sleep(3)
        self.enable_pin.value = 0
        self.direc_pin.value = 0 

    def __clean_power(self, rawpower):
        power = rawpower
        if rawpower > 12:
            power =  12
        elif rawpower < -12:
            power = -12
        return power

    def set_power(self, power):
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

