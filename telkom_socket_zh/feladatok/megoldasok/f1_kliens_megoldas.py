r"""
F1: TCP / UDP KLIENS                              (gyakorlás a ZH 1. feladatához)

A szervert megkapod (ref_szerverek.py), TE a klienst írod meg.

A szerver:
  - kérés:  "16s i" formátum: szöveg (16 bájt) + egész szám n
  - válasz: a szöveg UTOLSÓ n karaktere NAGYBETŰSEN, "<n>s" formátumban
  - példa:  ("almafa", 3) -> "AFA"

Írd meg:
  1) kuld_tcp(szoveg, n, port)      -> str   TCP kliens
  2) kuld_fajlbol(fajl, sor, port)  -> str   a fájl sorai "szó;szám" alakúak (pl. "korte;2"),
                                             a sor 1-től számozva; a kiválasztott sort küldd el
                                             a TCP szervernek, és add vissza a választ
  3) kuld_udp(szoveg, n, port)      -> str   ugyanaz, mint az 1), de UDP-vel

Tippek (ha elakadsz: peldak/p1_tcp_kliens.py):
  - REQ = struct.Struct("16s i"),  REQ.pack(szoveg.encode(), n)
  - TCP-nél a választ recv_exact-tal olvasd, UDP-nél recvfrom-mal
  - a válasz formátuma f"{n}s", a végén .rstrip(b"\x00").decode()

Futtatás:  python3 f1_kliens.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import socket
import struct

REQ = struct.Struct("16s i")


def recv_exact(sock, size):  # kész, másold be a saját segédletedbe is
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def kuld_tcp(szoveg, n, port):
    with socket.create_connection(("localhost", port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))
        valasz = recv_exact(sock, n)
    (szoveg_valasz,) = struct.unpack(f"{n}s", valasz)
    return szoveg_valasz.rstrip(b"\x00").decode()


def kuld_fajlbol(fajl, sor, port):
    with open(fajl, encoding="utf-8") as f:
        sorok = f.read().splitlines()
    szoveg, szam = sorok[sor - 1].split(";")
    return kuld_tcp(szoveg, int(szam), port)


def kuld_udp(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), ("localhost", port))
        adat, _ = sock.recvfrom(1024)
    (szoveg_valasz,) = struct.unpack(f"{n}s", adat)
    return szoveg_valasz.rstrip(b"\x00").decode()


# ----------------------------------------------------------------------------
#  Ellenőrzés (ezt ne módosítsd)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import tempfile

    from ref_szerverek import egyezik, f1_tcp_szerver, f1_udp_szerver, futtat, inditas_tcp, inditas_udp

    TCP_PORT, UDP_PORT = 12001, 12002

    def teszt():
        inditas_tcp(f1_tcp_szerver, TCP_PORT, port=TCP_PORT)
        inditas_udp(f1_udp_szerver, UDP_PORT)
        egyezik("kuld_tcp('almafa', 3)", kuld_tcp("almafa", 3, TCP_PORT), "AFA")
        egyezik("kuld_tcp('korte', 5)", kuld_tcp("korte", 5, TCP_PORT), "KORTE")
        fajl = os.path.join(tempfile.gettempdir(), "f1_input.txt")
        with open(fajl, "w", encoding="utf-8") as f:
            f.write("korte;2\nbarack;4\nszilva;3\n")
        egyezik("kuld_fajlbol(2. sor)", kuld_fajlbol(fajl, 2, TCP_PORT), "RACK")
        egyezik("kuld_fajlbol(3. sor)", kuld_fajlbol(fajl, 3, TCP_PORT), "LVA")
        egyezik("kuld_udp('almafa', 3)", kuld_udp("almafa", 3, UDP_PORT), "AFA")

    futtat("F1", teszt)
