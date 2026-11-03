import builtins
from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select
import sys
import random

#code30passwd419

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)
server_addr1 = ('localhost', 10001)
server_addr2 = ('localhost', 10002)

build = sys.argv[1:]

cars = {}
for i in range(len(build) // 3):
	cars[i] = (build[i*3],build[i*3+1],build[i*3+2])

print(cars)
print(len(cars))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    inputs = [ server ]
    while True:

        readable, writable, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                print('Vásárló érkezett')
            else:
                try:
                    data = s.recv(packer.size)
                    req = packer.unpack(data)
					
                    ask1 = req[0].decode().replace('\x00','')
                    ask2 = req[1].decode().replace('\x00','')
                    print("Vásárló kérése: ", ask1)
                    print("Adat: ", ask2)
                    
                    res = ""
                    if ask1 == "tipus":
                        for i in range(len(cars)):
                            if cars[i][0] == ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    elif ask1 == "kor":
                        for i in range(len(cars)):
                            if cars[i][1] <= ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    elif ask1 == "ar":
                        for i in range(len(cars)):
                            if cars[i][2] <= ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    print('Kérésre válasz:', res)
                    s.send(res.encode())
                except timeout:
                    pass
                except struct.error:
                    inputs.remove(s)
