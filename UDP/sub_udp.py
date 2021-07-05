# sub pi's udp code
import socket
import struct
from contextlib import closing

# ip_setting
host = ""
port = 60000

# socket_settings
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

# main_loop
with closing(sock):
    while True:
        # recv_controller
        data, address = sock.recvfrom(1024)
        t,value,code,index=struct.unpack("<ihbb",data)
        print("t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(t,value,code,index))