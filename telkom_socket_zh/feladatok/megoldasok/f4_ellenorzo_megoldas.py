r"""
F4: ELLENŐRZŐ KLIENS                              (gyakorlás a ZH 3. feladat b) részéhez)

Adott két szerver (ref_szerverek.py):
  - TCP szerver: IN / INCR / DECR, "4s i" formátum, a válasz bytesztring (b"19")
  - UDP szerver: PUSH / PLUS / MINUS, "5s i" formátum, a válasz "i" (struct)
    Az UDP szerver néha hibázik: a kapott számhoz kis eltérést ad.

Írd meg:  ellenorzo(tcp_port, udp_port, kerdesek) -> int
  Ismételd meg a kerdesek-szer: kérdezd le mindkét szervertől az értéket
  (TCP: "INCR 0", UDP: "PLUS 0"), és hasonlítsd össze őket.
  Térj vissza azzal, hányszor TÉRT EL a két érték.

Tippek (ha elakadsz: peldak/p4_ellenorzo_kliens.py):
  - TCP válasz: int(sock.recv(1024))
  - UDP válasz: REPLY.unpack(adat)[0]

Futtatás:  python3 f4_ellenorzo.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import socket
import struct

TCP_CMD = struct.Struct("4s i")
UDP_CMD = struct.Struct("5s i")
REPLY = struct.Struct("i")


def ellenorzo(tcp_port, udp_port, kerdesek):
    elteresek = 0
    for _ in range(kerdesek):
        with socket.create_connection(("localhost", tcp_port)) as tcp:
            tcp.sendall(TCP_CMD.pack(b"INCR", 0))
            tcp_ertek = int(tcp.recv(1024))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.settimeout(2)
            udp.sendto(UDP_CMD.pack(b"PLUS", 0), ("localhost", udp_port))
            adat, _ = udp.recvfrom(1024)
        udp_ertek = REPLY.unpack(adat)[0]
        if tcp_ertek != udp_ertek:
            elteresek += 1
    return elteresek


# ----------------------------------------------------------------------------
#  Ellenőrzés (ezt ne módosítsd)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    from ref_szerverek import egyezik, futtat, hibas_udp_szerver, inditas_tcp, inditas_udp, zh_tcp_szerver

    def teszt():
        # 1. forgatókönyv: az UDP szerver az 1., 2., 3., 4., 5. parancsnál +0, +1, +0, +0, -1 hibát ad
        inditas_tcp(zh_tcp_szerver, 12005, port=12005)
        inditas_udp(hibas_udp_szerver, 12006, [0, 1, 0, 0, -1])
        egyezik("hibás UDP szerver (5 kérdés)", ellenorzo(12005, 12006, 5), 3)
        # 2. forgatókönyv: egy hibátlan UDP szerver
        inditas_tcp(zh_tcp_szerver, 12007, port=12007)
        inditas_udp(hibas_udp_szerver, 12008, [0])
        egyezik("hibátlan UDP szerver (4 kérdés)", ellenorzo(12007, 12008, 4), 0)

    futtat("F4", teszt)
