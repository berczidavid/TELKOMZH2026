"""
P5: TCP PROXY, ami UDP szerverhez továbbít            (ZH 3. feladat c) része)

A helyzet:
  kliens --TCP (4s i)--> PROXY --UDP (5s i)--> UDP szerver
  kliens <--bytesztring-- PROXY <--(i)-------- UDP szerver

A proxy:
  - a kliensek felé select-es TCP szerver (mint a P3-ban), de NEM tárol értéket
  - a parancsot ÁTFORDÍTJA:  IN -> PUSH,  INCR -> PLUS,  DECR -> MINUS
  - elküldi az UDP szervernek (sendto), megvárja a választ (recvfrom), kicsomagolja (i)
  - a TCP kliensnek bytesztringként küldi vissza: str(érték).encode()

Futtatás:  python3 p5_tcp_proxy.py
"""
import select
import socket
import struct
import threading

HOST = "localhost"
PROXY_PORT = 11007
UDP_PORT = 11008

TCP_CMD = struct.Struct("4s i")  # kliens -> proxy
UDP_CMD = struct.Struct("5s i")  # proxy -> UDP szerver
REPLY = struct.Struct("i")  # UDP szerver -> proxy

FORDITAS = {"IN": "PUSH", "INCR": "PLUS", "DECR": "MINUS"}  # a "szótár", ez a feladat magja


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


# =============================================================================
#  EZT A ZH-N MEGKAPOD: az UDP szerver (ez tárolja az értéket)
# =============================================================================
def udp_szerver(ready):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, UDP_PORT))
        ready.set()
        while True:
            data, kliens = sock.recvfrom(1024)
            nev, x = UDP_CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()
            if nev == "PUSH":
                ertek = x
            elif nev == "PLUS":
                ertek += x
            elif nev == "MINUS":
                ertek -= x
            sock.sendto(REPLY.pack(ertek), kliens)


# =============================================================================
#  PROXY: EZT KELL MEGÍRNOD
# =============================================================================
def proxy(ready=None):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # EGY UDP socket, a ciklus előtt
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PROXY_PORT))
        server.listen(5)
        if ready:
            ready.set()
        inputs = [server]  # az UDP socket NEM kerül ide: a választ rögtön megvárjuk rajta
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    data = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    data = b""
                if not data:
                    inputs.remove(s)
                    s.close()
                    continue

                nev, x = TCP_CMD.unpack(data)  # 1) kicsomagolás a kliens formátumával (4s i)
                nev = nev.rstrip(b"\x00").decode()
                udp_nev = FORDITAS.get(nev)  # 2) parancs átfordítása
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), (HOST, UDP_PORT))  # 3) újracsomagolás (5s i)
                valasz, _ = udp.recvfrom(1024)  # 4) a válasz megvárása
                (ertek,) = REPLY.unpack(valasz)  # 5) kicsomagolás (i)
                s.sendall(str(ertek).encode())  # 6) a kliens felé bytesztring


# =============================================================================
#  Tesztkliensek (a ZH-n a tesztkörnyezet adja)
# =============================================================================
def kuld(sock, nev, x):
    sock.sendall(TCP_CMD.pack(nev.encode(), x))
    return sock.recv(1024)


if __name__ == "__main__":
    for fn in (udp_szerver, proxy):
        ready = threading.Event()
        threading.Thread(target=fn, args=(ready,), daemon=True).start()
        ready.wait()

    a = socket.create_connection((HOST, PROXY_PORT))
    b = socket.create_connection((HOST, PROXY_PORT))
    assert kuld(a, "IN", 20) == b"20"
    assert kuld(b, "INCR", 4) == b"24"
    assert kuld(a, "DECR", 5) == b"19"
    print("IN 20 -> 20, INCR 4 -> 24, DECR 5 -> 19 (két kliens, a proxyn keresztül)   OK")
    assert kuld(a, "NEMLETEZIK", 1) == b"ERR"
    print("Ismeretlen parancs -> ERR, a proxy tovább él   OK")
    a.close()
    b.close()
