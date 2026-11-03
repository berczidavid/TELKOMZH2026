"""
SOCKET ZH PUSKA v2   (keretek + minták; a feladat logikáját TE írod be a "<-- ITT" helyekre)

=== A ZH ELSŐ 3 PERCE: ezt írd ki mindegyik feladatnál ===
  1) Melyik programot kell megírni (kliens / szerver / proxy), melyik adott?
  2) TCP vagy UDP? (kliens: create_connection | UDP: SOCK_DGRAM + sendto/recvfrom)
  3) Hány üzenet megy, egy kapcsolaton? (TCP: ugyanazon a socketen, a with-on BELÜL)
  4) Minden üzenet struct formátuma + mérete (Struct(...).size)
  5) A válasz: struct (melyik formátum) vagy bytesztring?
  6) Parancssori argumentumok (sys.argv): mi a sorrend?
  7) Kell-e select (több kliens)? Mi az állapot (egy szám, szótár...) és mi a kulcsa?

=== A KERET 3 DÖNTÉSE ===
  TCP kliens:  socket.create_connection((host, port))
  TCP szerver: socket.socket(AF_INET, SOCK_STREAM) + bind + listen (+ select ciklus)
  UDP:         socket.socket(AF_INET, SOCK_DGRAM)  (nincs listen/accept/connect)

=== STRUCT ===
  - Méretet SOHA ne számolj kézzel: Struct("...").size (a kitöltés miatt más lehet, mint az összeg)
  - Gyors méret: python -c "import struct; print(struct.calcsize('4s 6s i'))"
  - TÖBB MEZŐ: Struct("6s 8s 7s") -> unpack annyi elemű tuple-t ad, ahány mező van:
        a, b, c = S.unpack(adat)
  - s mező: küldés előtt .encode(), fogadás után .rstrip(b"\\x00").decode()
  - i mező: sima egész, nem kell átalakítani
  - ha egy s mezőt csak TOVÁBBADSZ (nem kell megnézned), maradhat bájt, nem kell dekódolni
  - rövid szöveg a mezőben nullával kipótolódik; hosszabbat levág
  - ne tegyél elé !, <, > jelet, ha a feladat nem írja

=== VÁLASZ TÍPUSA ===
  bytesztring: küld: sock.sendall(str(x).encode())   kap: int(sock.recv(1024))
  struct:      küld: REPLY.pack(x)                   kap: REPLY.unpack(recv_exact(sock, REPLY.size))[0]
  szabad hosszú bytesztring továbbítása: valasz = ...recvfrom(1024); s.sendall(valasz)

=== PARANCSSORI ARGUMENTUMOK ===
  python client.py localhost 20001   ->  host, port = sys.argv[1], int(sys.argv[2])
  python server.py 10001             ->  port = int(sys.argv[1])
  python proxy.py 10002 20002        ->  port, szerver_port = int(sys.argv[1]), int(sys.argv[2])
  (a port mindig int(...), az argv szöveg!)

=== ELLENŐRZÉS (a ZH leírása szerint) ===
  python tests.py check <KÓD> feladatN      (a KÓDOT pontosan másold, kis/nagybetű számít;
                                             ez NEM a neptun kódod)
  python tests.py start <KÓD> feladatN      (tesztszerver naplója), másik ablakban a programod
  python tests.py test feladatN <port>      (teszt a saját szerveredre/proxyd-ra)
  A tests mappa kódját nem elemzed, fekete doboz.
  Windowson: python, Macen: python3.

=== TIPIKUS HIBÁK ===
  - a másolt sablonban régi nevek/formátumok maradtak (parancsnevek, HOST, PORT, ready)
  - str-t küldesz bájt helyett (.encode() hiányzik)
  - a struct méretet kézzel írtad be (kitöltés!)
  - unpack tuple, [0] vagy kicsomagolás kell
  - a második üzenet kikerül a with blokkból -> a kapcsolat már zárva
  - a szerver állapota a ciklusban jön létre (nullázódik); a ciklus ELÉ kell
  - bontott kliens (b"") nincs kivéve az inputs-ból -> végtelen ciklus
  - struct választ vársz, de bytesztring jön (vagy fordítva)
  - UDP socket a select listában (nem kell oda)
"""
import json
import os
import random
import select
import socket
import struct
import sys

HOST = "localhost"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def sz(b):
    """s mező -> szöveg."""
    return b.rstrip(b"\x00").decode()


# ====================================================================================
#  A. TCP KLIENS, TÖBB ÜZENET EGY KAPCSOLATON  (kérdés -> válasz -> döntés -> újabb üzenet)
# ====================================================================================
KERES = struct.Struct("6s 8s 7s")  # <-- ITT VÁLTOZIK: a kérés formátuma (több mező!)
VALASZ = struct.Struct("i 10s")  # <-- ITT VÁLTOZIK: a szerver válasza
VEGSO = struct.Struct("12s")  # <-- ITT VÁLTOZIK: az utolsó válasz formátuma


def kliens_beszelgetes():
    host, port = sys.argv[1], int(sys.argv[2])  # python client.py localhost 20001
    with socket.create_connection((host, port)) as sock:
        sock.sendall(KERES.pack(b"mezo1", b"mezo2", b"elso"))  # 1. üzenet (bájtok vagy .encode())
        szam, szoveg = VALASZ.unpack(recv_exact(sock, VALASZ.size))  # a válasz: pontosan .size bájt
        szoveg = sz(szoveg)  # s mező -> szöveg, hogy össze tudd hasonlítani
        # <-- ITT döntesz a kapott mezők alapján (összehasonlítás, "vagy" = or, "és" = and)
        tipus = b"valasztas"  # <-- ITT: az feltétel alapján melyik üzenet megy
        sock.sendall(KERES.pack(b"mezo1", b"mezo2", tipus))  # 2. üzenet UGYANAZON a kapcsolaton
        (vegso,) = VEGSO.unpack(recv_exact(sock, VEGSO.size))
        print(sz(vegso))


# ====================================================================================
#  B. TCP KLIENS: EGY KÉRDÉS (struct küld, "Xs" kap), bemenet-változatok
# ====================================================================================
REQ = struct.Struct("20s i")  # <-- ITT VÁLTOZIK


def tcp_kliens(szoveg, n, port):
    with socket.create_connection((HOST, port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))
        valasz = recv_exact(sock, n)  # <-- válasz mérete: n / .size / recv(1024)
    return struct.unpack(f"{n}s", valasz)[0].rstrip(b"\x00").decode()


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


def udp_kliens(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), (HOST, port))
        adat, _ = sock.recvfrom(1024)  # egy recvfrom = egy teljes válasz
    return struct.unpack(f"{n}s", adat)[0].rstrip(b"\x00").decode()


# ====================================================================================
#  C. ÁLLAPOT TÁROLÁSA SZÓTÁRBAN (minták, nem a feladat megoldása)
# ====================================================================================
#   egy szám:               ertek = 0                 (ciklus ELŐTT)
#   kulcs -> szám:          adatok = {}               adatok[k] = adatok.get(k, 0) + x
#   kulcs -> kulcs -> szám: adatok = {}
#       belso = adatok.setdefault(k1, {})             # ha még nincs k1, létrehozza az üres belső szótárat
#       belso[k2] = belso.get(k2, 0) + x              # hozzáadás (ha nincs, 0-ról indul)
#       adatok.get(k1, {}).get(k2, 0)                 # lekérdezés, hiba nélkül (nincs -> 0)
#       sum(adatok.get(k1, {}).values())              # a belső szótár összes értékének összege


# ====================================================================================
#  D. TCP SZERVER select-tel  (több kliens, közös állapot)
# ====================================================================================
CMD = struct.Struct("4s 6s i")  # <-- ITT VÁLTOZIK: a parancs formátuma (mezők száma is!)
REPLY = struct.Struct("i")  # <-- ITT VÁLTOZIK: struct válasz (i) VAGY bytesztring


def select_szerver(port):  # python server.py <port>  ->  port = int(sys.argv[1])
    allapot = {}  # <-- ITT VÁLTOZIK: egy szám (0) vagy szótár; a ciklus ELŐTT
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
                    adat = recv_exact(s, CMD.size)
                except ConnectionResetError:  # Windows
                    adat = b""
                if not adat:  # bontott kliens
                    inputs.remove(s)
                    s.close()
                    continue
                nev, kulcs, x = CMD.unpack(adat)  # <-- annyi név, ahány mező van
                nev, kulcs = sz(nev), sz(kulcs)
                ertek = 0  # <-- ITT a feladat logikája (parancsonként if/elif)
                s.sendall(REPLY.pack(ertek))  # struct válasz; bytesztring: str(ertek).encode()


# ====================================================================================
#  E. UDP SZERVER
# ====================================================================================
UDP_CMD = struct.Struct("5s i")  # <-- ITT VÁLTOZIK
UDP_REPLY = struct.Struct("i")  # <-- ITT VÁLTOZIK


def udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, port))  # nincs listen, nincs accept
        while True:
            adat, kliens = sock.recvfrom(1024)  # a kliens címe is jön
            nev, x = UDP_CMD.unpack(adat)
            nev = sz(nev)
            # <-- ITT a feladat logikája (parancsonként if/elif)
            sock.sendto(UDP_REPLY.pack(ertek), kliens)  # válasz a feladó címére


# ====================================================================================
#  F. PROXY (TCP elöl, UDP hátul)  - a választ továbbadja
# ====================================================================================
KLIENS_IN = struct.Struct("i 12s")  # <-- ITT VÁLTOZIK: kliens felől
SZERVER_OUT = struct.Struct("4s 12s")  # <-- ITT VÁLTOZIK: szerver felé


def proxy(proxy_port, udp_port):  # python proxy.py <port> <szerver_port>: két int(sys.argv[..])
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # EGY UDP socket, ciklus előtt
    udp.settimeout(3)  # különben lefagy, ha a szerver nem válaszol
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
                    adat = recv_exact(s, KLIENS_IN.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                tipus, nev = KLIENS_IN.unpack(adat)  # nev bájt marad, ha csak továbbadod
                parancs = b"????"  # <-- ITT: a tipus alapján melyik parancs megy (if/else vagy szótár)
                udp.sendto(SZERVER_OUT.pack(parancs, nev), (HOST, udp_port))
                valasz, _ = udp.recvfrom(1024)  # a szerver válasza (bájtok)
                s.sendall(valasz)  # VÁLTOZATLANUL vissza a kliensnek (itt nincs unpack)
                # ha a feladat átalakítást kér: struct -> unpack, bytesztring -> str(x).encode()


# ====================================================================================
#  G. ELLENŐRZŐ KLIENS (két szerver értékének összehasonlítása)
# ====================================================================================
def ellenorzo(tcp_port, udp_port, tcp_cmd, udp_cmd):
    with socket.create_connection((HOST, tcp_port)) as tcp:
        tcp.sendall(tcp_cmd)  # a "0-val növelés" parancs már becsomagolva
        tcp_ertek = int(tcp.recv(1024))  # bytesztring válasz
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2)
        udp.sendto(udp_cmd, (HOST, udp_port))
        adat, _ = udp.recvfrom(1024)
    udp_ertek = UDP_REPLY.unpack(adat)[0]  # struct válasz
    return tcp_ertek != udp_ertek  # True = eltérés
