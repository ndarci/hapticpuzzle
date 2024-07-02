import matplotlib.pyplot as plt
import numpy as np
import time
from hapticpuzzle_plot import *
import socket
from struct import unpack

#ip stuf
pi_ip = "192.168.4.230"
toby_ip = "192.168.4.52"
localhost_ip = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = toby_ip, 10000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

fig,axs,lines,data = generate_axes(['pos','vel','acc'],100,[(-100,100),(-100,100),(-200,200)])

while True:
    try:
        #idea here is to grab one data point for pos,vel, and acc from the rpi,
        #then send this data into our update plot function to display in real time
        message, address = sock.recvfrom(4096)
        new_data = unpack('3f', message)
        update_plot(lines,data,new_data)
    except KeyboardInterrupt:
        break

print('goodbye')
