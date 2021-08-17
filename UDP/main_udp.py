# main pi's udp code
import socket
import struct
from contextlib import closing
from timeout_decorator import timeout, TimeoutError

# host_setting
send_ip = "192.168.11.11"    # input another pi's IP address
port = 60000

# socket_setting
send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# num_setting
mode = 0

# main_loop
with closing(send):
    with open('/dev/input/js0', 'rb')as f:
        while True:
            data = f.read(8)
            t,value,code,index=struct.unpack("<ihbb", data)

            # send_data
            if mode%2 == 0:
                print("t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(t,value,code,index))
            elif mode%2 == 1:
                send.sendto(data, (send_ip, port))
                print("send_a_message")
            
            # change_mode
            if index==10 and code==1 and value==1:
                mode += 1