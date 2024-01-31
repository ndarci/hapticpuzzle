import time
from hapticpuzzle_motor import Motor

motor = Motor()

# motor.set_power(-10)

while True:
    motor.update_vars()
    motor.update_pwm()
    time.sleep(0.05)