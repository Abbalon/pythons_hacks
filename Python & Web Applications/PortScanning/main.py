import socket

s = socket.socket()

for i in range(0,65535):
    for j in range(10,64):
        ip = "192.168.10." + str(j)
        print("IP: " + ip)
        result = s.connect_ex((ip, i))
        if(result == 0):
            print(str(i) + ' port is open')