import select
import socket
import struct
import sys

IN = struct.Struct("i 20s")  # kliens felől: kliens_típus, felhasználónév: 24 bájt
OUT = struct.Struct("5s 20s")  # UDP szerver felé: LOGIN/GUEST, felhasználónév: 25 bájt


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    port, szerver_port = int(sys.argv[1]), int(sys.argv[2])  # python proxy.py <port> <szerver_port>
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # egy UDP socket, a ciklus előtt
    udp.settimeout(3)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", port))
        server.listen(5)
        inputs = [server]
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, IN.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                tipus, nev = IN.unpack(adat)
                parancs = b"LOGIN" if tipus == 0 else b"GUEST"  # 0: Felhasználó, 1: Vendég
                udp.sendto(OUT.pack(parancs, nev), ("localhost", szerver_port))
                valasz, _ = udp.recvfrom(1024)
                s.sendall(valasz)  # a válasz változatlanul megy vissza a kliensnek


if __name__ == "__main__":
    main()
