# main/client
import socket
import struct
from contextlib import closing

# ip_setting
host = "192.168.11.57"
port = 60000

# socket_setting
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# set_num
mode = 0

with closing(sock):
    with open('/dev/input/js0', 'rb')as f:
        while True:
            data = f.read(8)
            # recv_controller
            t, value, code, index = struct.unpack("<ihbb", data)

            # print_or_send data
            if mode%2 == 0:
                print("t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(t,value,code,index))
            else:
                sock.send(data)
                print("send_a_message_{:010d}".format(t))
            
            if index==10 and code==1 and value==1:
                mode += 1