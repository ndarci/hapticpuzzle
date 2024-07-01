import time
from hapticpuzzle_motor import Motor
from struct import pack
import socket

period = 0.01
graph_period = 0.1
motor = Motor(period)

host, port = "192.168.4.52", 10000
server_address = (host,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# motor.set_power(-10)

def update_motor():
    motor.update_vars()
    motor.update_pwm()

def update_graph():
    message = pack('3f',motor.pos,motor.vel,motor.acc)
    sock.sendto(message, server_address)

timer_m = time.time()
timer_g = timer_m
while True:
    now = time.time()
    if now-timer_m > period:
        update_motor()
        timer_m = now
    if now-timer_g > graph_period:
        update_graph()
        timer_g = now