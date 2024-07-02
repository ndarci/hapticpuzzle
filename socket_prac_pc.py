import socket
from struct import unpack


pi_ip = "192.168.4.230"
toby_ip = "192.168.4.52"
localhost_ip = "127.0.0.1"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = toby_ip, 10000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)
how_many_times_baby = 0
while True:
    # Wait for message
    try:
        message, address = sock.recvfrom(4096)
        how_many_times_baby += 1
        print(f'Received {len(message)} bytes:')
        x, y, z = unpack('3f', message)
        print(f'X: {x}, Y: {y}, Z: {z}')
    except KeyboardInterrupt:
        print("great job ! :0 bye bye!! You got this much data babes: "+str(how_many_times_baby))
        break