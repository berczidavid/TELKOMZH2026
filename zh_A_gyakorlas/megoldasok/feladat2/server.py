import select
import socket
import struct
import sys

CMD = struct.Struct("3s 6s 8s i")  # parancs, raktár, termék, mennyiség: 24 bájt (kitöltés miatt)
REPLY = struct.Struct("i")


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    port = int(sys.argv[1])  # python server.py <port>
    raktar = {}  # {raktár: {termék: darab}}, a ciklus előtt
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
                    adat = recv_exact(s, CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                nev, w, p, q = CMD.unpack(adat)
                nev, w, p = (x.rstrip(b"\x00").decode() for x in (nev, w, p))
                ertek = 0
                if nev == "ADD":
                    termekek = raktar.setdefault(w, {})
                    termekek[p] = termekek.get(p, 0) + q
                    ertek = termekek[p]
                elif nev == "GET":
                    ertek = raktar.get(w, {}).get(p, 0)
                elif nev == "TOT":
                    ertek = sum(raktar.get(w, {}).values())
                s.sendall(REPLY.pack(ertek))  # struct válasz, nem bytesztring!


if __name__ == "__main__":
    main()
