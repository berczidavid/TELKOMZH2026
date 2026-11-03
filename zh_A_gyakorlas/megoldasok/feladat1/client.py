import socket
import struct
import sys

REQ = struct.Struct("6s 8s 7s")  # neptun, járatszám, üzenet típusa: 21 bájt
RESP = struct.Struct("i 10s")  # szabad helyek, utazási osztály: 14 bájt
BOOK = struct.Struct("12s")  # foglalási azonosító

NEPTUN = b"ABC123"  # <-- ide a saját neptun kódod (6 karakter)
JARAT = b"LH2048"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    host, port = sys.argv[1], int(sys.argv[2])  # python client.py localhost 20001
    with socket.create_connection((host, port)) as sock:
        sock.sendall(REQ.pack(NEPTUN, JARAT, b"request"))
        szabad, osztaly = RESP.unpack(recv_exact(sock, RESP.size))
        osztaly = osztaly.rstrip(b"\x00").decode()
        if osztaly != "economy" or szabad < 3:
            tipus = b"reject"
        else:
            tipus = b"reserve"
        sock.sendall(REQ.pack(NEPTUN, JARAT, tipus))
        (azonosito,) = BOOK.unpack(recv_exact(sock, BOOK.size))
        print(tipus.decode(), azonosito.rstrip(b"\x00").decode())


if __name__ == "__main__":
    main()
