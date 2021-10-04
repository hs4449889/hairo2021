# sub/server
import socket
import struct
from contextlib import closing

# ip_setting
host = ""    # still_empty(??)
port = 60000

# socket_setting
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(3)
rasp, addr = sock.accept()

# set_num
mode = 0

with closing(sock), closing(rasp):
    while True:
        data = rasp.recv(8)
        # recv_conttroller
        t, value, code, index = struct.unpack("<ihbb", data)

        # print_data
        print("t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(t,value,code,index))