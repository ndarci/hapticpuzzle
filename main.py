import time
import busio
from hapticpuzzle_i2c import Slider, LEDStick
from hapticpuzzle_motor import Motor

def main():
    i2c = busio.I2C(sda = 2, scl = 3, frequency = 100000)

    stick = LEDStick(i2c)
    print(stick.bus)    
    slider = Slider(i2c)
    print(slider.bus)
    motor = Motor(0.01)

    stick.off()

    while True:
        try:
            pot_pos = slider.read_potentiometer(2)
            led_to_light = int(pot_pos / 1023 * 10)
            volts_to_motor = ((pot_pos / 1023) - 0.5) * 20

            green = [0x00, 0x0f, 0x00]
            stick.change_led(led_to_light, green)

            motor.set_power(volts_to_motor)

        except KeyboardInterrupt:
            break
    stick.off()
    motor.set_power(0)

if __name__ == '__main__':
    main()