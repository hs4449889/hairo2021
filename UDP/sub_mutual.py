# sub pi's udp code
import socket
import struct
from contextlib import closing

# ip_setting
send_ip = "192.168.75.58"    # input another pi's IP address
recv_ip = ""              # server's IP (still empty)
port = 60000

# socket_setting
send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv.bind((recv_ip, port))
recv.settimeout(0.02)

# num_setting
count = 0

# main_loop
with closing(recv), closing(send):
    while True:
        try:
            # controller
            data, addr = recv.recvfrom(1024)
            t,value,code,index=struct.unpack("<ihbb", data)
            print("c: {:10d},t: {:10d}ms,value:{:6d},code:{:1d},index{:1d}".format(count,t,value,code,index))
        except socket.timeout:
            pass
        finally:
            # sensor(must_change)
            sen1 = 196.2 * 10
            sen2 = 195.3 * 10
            sens = struct.pack("ff", sen1, sen2)
            # send_sensor
            send.sendto(sens, (send_ip, port))
	    print("{}send_data".format(count))
        count += 1