"""
P1: TCP / UDP KLIENS struct-tal          (ZH 1. feladat, a) b) c) d) változat)

Mit kell tudni a feladatról:
  - A szervert a ZH-n MEGKAPOD (kész, futó szerver), neked csak a kliens kell.
  - A kliens (szöveg, szám) párt küld "20s i" formátumban.
  - A szerver válasza pontosan <szám> bájt: "<szám>s" formátum.
  - Példa: almafa,4 -> amla     kortefa,3 -> rok

Futtatás:   python3 p1_tcp_kliens.py       (Windowson: python vagy py)
Ez a fájl önállóan fut: elindítja a "megkapott" szervert egy szálban, aztán
lefuttatja a klienseket. Neked a "KLIENS" részt kell megérteni és lemásolni.
"""
import json
import os
import random
import socket
import struct
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
HOST = "localhost"
TCP_PORT = 11001
UDP_PORT = 11002

REQ = struct.Struct("20s i")  # 20 bájt szöveg (nullával kipótolva) + 4 bájt szám = 24 bájt


def recv_exact(sock, size):
    """TCP-nél a recv(24) NEM garantálja, hogy 24 bájtot kapsz: addig olvasunk, amíg meg nincs."""
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:  # a másik oldal bontott
            return b""
        data += chunk
    return data


# =============================================================================
#  EZT A ZH-N MEGKAPOD (kész szerver). Nem kell megírnod, csak tudd, mit csinál.
# =============================================================================
def feldolgoz(text, n):
    return text[:n][::-1]  # az első n karakter, megfordítva: almafa,4 -> amla


def tcp_szerver(ready):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, TCP_PORT))
        srv.listen(5)
        ready.set()
        while True:
            conn, _ = srv.accept()
            with conn:
                data = recv_exact(conn, REQ.size)
                if not data:
                    continue
                text, n = REQ.unpack(data)
                valasz = feldolgoz(text.rstrip(b"\x00").decode(), n)
                conn.sendall(struct.pack(f"{n}s", valasz.encode()))


def udp_szerver(ready):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
        srv.bind((HOST, UDP_PORT))
        ready.set()
        while True:
            data, kliens = srv.recvfrom(1024)
            text, n = REQ.unpack(data)
            valasz = feldolgoz(text.rstrip(b"\x00").decode(), n)
            srv.sendto(struct.pack(f"{n}s", valasz.encode()), kliens)


# =============================================================================
#  KLIENS: EZT KELL MEGÍRNOD
# =============================================================================
def tcp_kliens(text, n):
    """Közös mag: elküldi a (szöveg, szám) párt, visszaadja a választ szövegként."""
    with socket.create_connection((HOST, TCP_PORT)) as sock:
        sock.sendall(REQ.pack(text.encode(), n))  # 1) .encode(): a struct 's' bájtot vár, nem str-t
        valasz = recv_exact(sock, n)  # 2) a válasz hossza pontosan n bájt
    (szoveg,) = struct.unpack(f"{n}s", valasz)  # 3) a formátum a számból épül: "4s", "3s"...
    return szoveg.rstrip(b"\x00").decode()  # 4) kipótolt nullák levágása + vissza szöveggé


def a_valtozat(text):
    """a) a szöveget a felhasználótól kérjük be (input), a számot generáljuk."""
    # a ZH-n: text = input("Szöveg: ")
    n = random.randint(1, len(text))  # a feladat nem ír elő tartományt, ez a biztonságos
    return n, tcp_kliens(text, n)


def b_valtozat():
    """b) input.txt: soronként 'szó szám'; véletlen sor (1..3) kiválasztása."""
    with open(os.path.join(HERE, "input.txt"), encoding="utf-8") as f:
        sorok = f.read().splitlines()
    i = random.randint(1, 3)  # randint: MINDKÉT vége benne van!
    szo, szam = sorok[i - 1].split()  # a sorok 0-tól indexelődnek -> i-1
    n = int(szam)  # a fájlból szöveg jön, át kell alakítani
    return szo, n, tcp_kliens(szo, n)


def c_valtozat():
    """c) input.json: a kulcsok SZÖVEGEK ("1", "2", "3"), az érték [szöveg, szám]."""
    with open(os.path.join(HERE, "input.json"), encoding="utf-8") as f:
        adat = json.load(f)
    kulcs = str(random.randint(1, 3))  # a kulcs szöveg: str(...)
    szo, n = adat[kulcs]
    return szo, n, tcp_kliens(szo, n)


def udp_kliens(text, n):
    """d) UDP: nincs connect, nincs recv_exact: egy datagram oda, egy vissza."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)  # ha elveszne a csomag, ne várjunk örökké
        sock.sendto(REQ.pack(text.encode(), n), (HOST, UDP_PORT))
        data, _ = sock.recvfrom(1024)  # egy recvfrom = egy teljes datagram
    (szoveg,) = struct.unpack(f"{n}s", data)
    return szoveg.rstrip(b"\x00").decode()


# =============================================================================
#  Bemeneti fájlok + indítás + ellenőrzés (ez csak a gyakorláshoz kell)
# =============================================================================
def fajlok_letrehozasa():
    with open(os.path.join(HERE, "input.txt"), "w", encoding="utf-8") as f:
        f.write("almafa 4\nkortefa 3\nbarackfa 5\n")
    with open(os.path.join(HERE, "input.json"), "w", encoding="utf-8") as f:
        json.dump({"1": ["almafa", 4], "2": ["kortefa", 3], "3": ["barackfa", 5]}, f)


if __name__ == "__main__":
    fajlok_letrehozasa()
    for fn in (tcp_szerver, udp_szerver):
        ready = threading.Event()
        threading.Thread(target=fn, args=(ready,), daemon=True).start()
        ready.wait()

    assert tcp_kliens("almafa", 4) == "amla"
    assert tcp_kliens("kortefa", 3) == "rok"
    print("TCP alap:        almafa,4 -> amla   kortefa,3 -> rok   OK")

    n, valasz = a_valtozat("almafa")
    assert valasz == feldolgoz("almafa", n)
    print(f"a) változat:     almafa, n={n} -> {valasz}")

    szo, n, valasz = b_valtozat()
    assert valasz == feldolgoz(szo, n)
    print(f"b) változat:     {szo}, n={n} -> {valasz}")

    szo, n, valasz = c_valtozat()
    assert valasz == feldolgoz(szo, n)
    print(f"c) változat:     {szo}, n={n} -> {valasz}")

    assert udp_kliens("almafa", 4) == "amla"
    print("d) UDP változat: almafa,4 -> amla   OK")
    print("\nMinden rendben. Most nyisd meg a kódot, és olvasd végig a megjegyzéseket!")
