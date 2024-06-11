import time
import socket

pi_ip = "192.168.4.230"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((pi_ip,70))
