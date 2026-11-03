from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import struct

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    data, client = ("kor".encode(), "1".encode())
    #data = ("tipus".encode(), "k".encode())

    client.sendall(packer.pack(*data))
    
    data = client.recv(packer2.size)
    print(data)
    res = data.decode()
    #cars = res[0].decode().replace('\x00','')
    print("Lekért adat: ", res)
