import socket
import random
from time import sleep
from struct import pack

host, port = "192.168.4.52", 10000
server_address = (host,port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# beepis
for i in range(1000):
    x, y, z = random.random(), random.random(), random.random()
    # Pack three 32-bit floats into message and send
    message = pack('3f', x, y, z)
    sock.sendto(message, server_address)

    sleep(.1)
    
