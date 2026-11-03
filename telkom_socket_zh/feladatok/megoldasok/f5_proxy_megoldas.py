r"""
F5: TCP PROXY, ami UDP szerverhez továbbít           (gyakorlás a ZH 3. feladat c) részéhez)

  kliens --TCP, "5s i"--> PROXY --UDP, "6s i"--> UDP szerver (kész: ref_szerverek.f3_udp_szerver)
  kliens <--bytesztring-- PROXY <--"i" struct---- UDP szerver

A proxy:
  - a kliensek felé select-es TCP szerver, saját értéket NEM tárol
  - a parancsokat átfordítja:  SET -> SETVAL,  ADD -> ADD,  SUB -> SUB,  DBL -> DOUBLE
  - elküldi az UDP szervernek, megvárja a választ, kicsomagolja ("i")
  - a kliensnek bytesztringként küldi vissza: b"24"
  - ismeretlen parancsra b"ERR" a válasz a kliensnek, és nem megy az UDP szerverhez

Írd meg:  proxy(proxy_port, udp_port)

Tippek (ha elakadsz: peldak/p5_tcp_proxy.py):
  - FORDITAS = {"SET": "SETVAL", ...}, FORDITAS.get(nev)
  - EGY UDP socket a ciklus előtt, az UDP socketet NEM kell a select-be tenni
  - TCP oldalon "5s i" (kliens), UDP oldalon "6s i" (szerver), válasz "i"

Futtatás:  python3 f5_proxy.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import select
import socket
import struct

TCP_CMD = struct.Struct("5s i")
UDP_CMD = struct.Struct("6s i")
REPLY = struct.Struct("i")


def recv_exact(sock, size):  # kész, másold be a saját segédletedbe is
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def proxy(proxy_port, udp_port):
    forditas = {"SET": "SETVAL", "ADD": "ADD", "SUB": "SUB", "DBL": "DOUBLE"}
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", proxy_port))
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
                    adat = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = TCP_CMD.unpack(adat)
                udp_nev = forditas.get(nev.rstrip(b"\x00").decode())
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), ("localhost", udp_port))
                valasz, _ = udp.recvfrom(1024)
                (ertek,) = REPLY.unpack(valasz)
                s.sendall(str(ertek).encode())


# ----------------------------------------------------------------------------
#  Ellenőrzés (ezt ne módosítsd)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    from ref_szerverek import egyezik, f3_udp_szerver, futtat, inditas_tcp, inditas_udp

    PROXY_PORT, UDP_PORT = 12010, 12009

    def kuld(sock, nev, x):
        sock.sendall(TCP_CMD.pack(nev.encode(), x))
        return sock.recv(1024)

    def teszt():
        inditas_udp(f3_udp_szerver, UDP_PORT)
        inditas_tcp(proxy, PROXY_PORT, UDP_PORT, port=PROXY_PORT)
        a = socket.create_connection(("localhost", PROXY_PORT), timeout=3)
        b = socket.create_connection(("localhost", PROXY_PORT), timeout=3)
        egyezik("SET 10", kuld(a, "SET", 10), b"10")
        egyezik("ADD 5", kuld(a, "ADD", 5), b"15")
        egyezik("SUB 3 (másik kliens)", kuld(b, "SUB", 3), b"12")
        egyezik("DBL 0", kuld(a, "DBL", 0), b"24")
        egyezik("ismeretlen parancs", kuld(b, "FOO", 1), b"ERR")
        egyezik("ADD 1 (az ERR nem érte el az UDP szervert)", kuld(a, "ADD", 1), b"25")
        a.close()
        b.close()

    futtat("F5", teszt)
