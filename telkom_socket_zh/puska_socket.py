"""
SOCKET ZH PUSKA   (minden sablon ugyanazt a keretet használja)

KERET HÁROM DÖNTÉSE
  1) TCP vagy UDP?   TCP kliens: socket.create_connection((host, port))
                     TCP szerver: socket.socket(AF_INET, SOCK_STREAM)
                     UDP (kliens és szerver): socket.socket(AF_INET, SOCK_DGRAM)
  2) Mi a struct formátum?  Struct("20s i").size a méret, SOHA ne írd be kézzel
                            ("5s i" = 12 bájt!). Ne tegyél elé !, <, > jelet.
  3) Mi a válasz típusa?
       bytesztring:  küld: sock.sendall(str(x).encode())      kap: int(sock.recv(1024))
       struct:       küld: REPLY.pack(x)                      kap: REPLY.unpack(adat)[0]

ALAPSZABÁLYOK
  - szöveg -> bájt: .encode()          s mező -> szöveg: .rstrip(b"\\x00").decode()
  - unpack tuple-t ad: (x,) = ... vagy ...[0]
  - TCP-n fix méretű struct olvasása: recv_exact; UDP-n: recvfrom(1024) elég
  - a szerver állapota (pl. ertek = 0) a ciklus ELŐTT jön létre
  - a recv üres bájtsort ad -> a kliens bontott
"""
import json
import os
import random
import select
import socket
import struct

HOST = "localhost"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


# ============================================================ 1. TCP KLIENS
REQ = struct.Struct("20s i")  # <-- ITT VÁLTOZIK: a feladat struct formátuma


def tcp_kliens(szoveg, n, port):
    with socket.create_connection((HOST, port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))  # <-- ITT VÁLTOZIK: mit küldesz
        valasz = recv_exact(sock, n)  # <-- ITT VÁLTOZIK: válasz mérete ("Xs" -> n; struct -> .size)
    return struct.unpack(f"{n}s", valasz)[0].rstrip(b"\x00").decode()  # <-- válasz formátuma


# bemenet-változatok (csak a bemenet forrása más, a küldés ugyanaz):
def bemenet_txt(fajl):  # sorok: "szo szam"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        sorok = f.read().splitlines()
    szo, szam = sorok[random.randint(1, 3) - 1].split()  # randint: mindkét vége benne van
    return szo, int(szam)


def bemenet_json(fajl):  # {"1": ["almafa", 4], ...}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        adat = json.load(f)
    szo, n = adat[str(random.randint(1, 3))]  # a kulcs szöveg!
    return szo, n


# bemenet_input:  szoveg = input("Szoveg: ");  n = random.randint(1, len(szoveg))


# ============================================================ 2. UDP KLIENS
def udp_kliens(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), (HOST, port))  # <-- ITT VÁLTOZIK
        adat, _ = sock.recvfrom(1024)  # egy recvfrom = egy teljes válasz
    return struct.unpack(f"{n}s", adat)[0].rstrip(b"\x00").decode()  # <-- válasz formátuma


# ============================================== 3. TCP SZERVER select-tel (több kliens)
TCP_CMD = struct.Struct("4s i")  # <-- ITT VÁLTOZIK: parancs formátuma


def select_szerver(port):
    ertek = 0  # közös állapot, a ciklus előtt
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(5)
        inputs = [server]
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:  # új kliens
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:  # Windows
                    adat = b""
                if not adat:  # bontott kliens
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = TCP_CMD.unpack(adat)
                nev = nev.rstrip(b"\x00").decode()
                # ---------- ITT VÁLTOZIK: parancsok ----------
                if nev == "IN":
                    ertek = x
                elif nev == "INCR":
                    ertek += x
                elif nev == "DECR":
                    ertek -= x
                # ---------------------------------------------
                s.sendall(str(ertek).encode())  # <-- ITT VÁLTOZIK: bytesztring VAGY struct


# ============================================================ 4. UDP SZERVER
UDP_CMD = struct.Struct("5s i")  # <-- ITT VÁLTOZIK
REPLY = struct.Struct("i")  # <-- ITT VÁLTOZIK (válasz struct)


def udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, port))  # nincs listen, nincs accept
        while True:
            adat, kliens = sock.recvfrom(1024)  # a kliens címe is jön
            nev, x = UDP_CMD.unpack(adat)
            nev = nev.rstrip(b"\x00").decode()
            # ---------- ITT VÁLTOZIK: parancsok ----------
            if nev == "PUSH":
                ertek = x
            elif nev == "PLUS":
                ertek += x
            elif nev == "MINUS":
                ertek -= x
            # ---------------------------------------------
            sock.sendto(REPLY.pack(ertek), kliens)  # válasz a feladó címére


# ============================================================ 5. ELLENŐRZŐ KLIENS
def ellenorzo(tcp_port, udp_port):
    with socket.create_connection((HOST, tcp_port)) as tcp:
        tcp.sendall(TCP_CMD.pack(b"INCR", 0))  # "0-val növelés" = lekérdezés
        tcp_ertek = int(tcp.recv(1024))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2)
        udp.sendto(UDP_CMD.pack(b"PLUS", 0), (HOST, udp_port))
        adat, _ = udp.recvfrom(1024)
    udp_ertek = REPLY.unpack(adat)[0]
    return tcp_ertek != udp_ertek  # True = az UDP szerver hibázott


# ============================================================ 6. PROXY (TCP -> UDP)
FORDITAS = {"IN": "PUSH", "INCR": "PLUS", "DECR": "MINUS"}  # <-- ITT VÁLTOZIK: átfordítás


def proxy(proxy_port, udp_port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # EGY UDP socket, ciklus előtt
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, proxy_port))
        server.listen(5)
        inputs = [server]  # az UDP socket NEM kerül ide
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = TCP_CMD.unpack(adat)  # 1) kliens formátuma
                udp_nev = FORDITAS.get(nev.rstrip(b"\x00").decode())  # 2) átfordítás
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), (HOST, udp_port))  # 3) UDP formátum
                valasz, _ = udp.recvfrom(1024)  # 4) válasz megvárása
                (ertek,) = REPLY.unpack(valasz)  # 5) kicsomagolás
                s.sendall(str(ertek).encode())  # 6) kliensnek bytesztring
