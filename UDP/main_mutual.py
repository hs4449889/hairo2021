# main_py's udp code
import socket
import struct
from contextlib import closing
from timeout_decorator import timeout, TimeoutError

# ip_setting
send_ip = "192.168.75.45"    # input another pi's IP address
recv_ip = ""              # server's IP (still empty)
port = 60000

# socket_setting
send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv.bind((recv_ip, port))

# num_setting
mode = 0
count = 0
t, value, code, index = 0, 0, 0, 0
data = ""  # do not need?

# receive_controller
@timeout(0.02)
def receive():
    global data
    data = f.read(8)
    print("read")
    _t, _value, _code, _index = struct.unpack("<ihbb", data)
    return _t, _value, _code, _index

# main_loop
with closing(recv), closing(send):
    with open('/dev/input/js0', 'rb')as f:
        while True:
            while True:
                try:
                    # recv_controller
                    t, value, code, index = receive()
                    break
                except:
                    pass
                finally:
                    # recv_sensor
                    sens, addr = recv.recvfrom(1024)
                    sen1, sen2 = struct.unpack("<ff", sens)
                    print(count, sen1, sen2)

            # send_data
            if mode%2 == 0:
                print("t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(t,value,code,index))
            elif mode%2 == 1:
                send.sendto(data, (send_ip, port))
                print("send_a_message")

            # unpacking_sensor
            sen1, sen2 = struct.unpack("<ff", sens)
            print(count,sen1, sen2)
            count += 1

            # change_mode and write_main_code
            if index==10 and code==1 and value==1:
                mode += 1