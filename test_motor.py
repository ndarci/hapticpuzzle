import time
from hapticpuzzle_motor import Motor

period = 0.01 
motor = Motor(period)

# motor.set_power(-10)

now = time.time()
while True:
    # diff = time.time() - now
    # print('{:.10f}'.format(diff) + '\t' + ('{:.10f}'.format(diff**2)))
    # now = time.time()
    motor.update_vars()
    motor.update_pwm()
    time.sleep(period)