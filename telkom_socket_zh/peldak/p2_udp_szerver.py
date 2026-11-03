"""
P2: UDP SZERVER, ami egy számot tárol         (ZH 3. feladat a) része)

A feladat:
  - A szerver egy egész számot tárol (kezdetben 0).
  - Parancsok (5s i) formátumban jönnek:  PUSH x (beállít), PLUS x (növel), MINUS x (csökkent)
  - A választ struct formátumban küldi vissza: (i), vagyis 4 bájt, NEM sima bytesztring!

UDP vs TCP, ami most számít:
  - nincs listen / accept / connect: bind, aztán recvfrom / sendto
  - minden datagram a feladó címével együtt érkezik: erre a címre kell válaszolni
  - egy recvfrom = egy teljes üzenet, nem kell recv_exact

Futtatás:  python3 p2_udp_szerver.py
"""
import socket
import struct
import threading

HOST = "localhost"
PORT = 11003

CMD = struct.Struct("5s i")  # parancs (5 bájt) + szám (4 bájt)
REPLY = struct.Struct("i")  # a válasz: egyetlen egész szám


# =============================================================================
#  SZERVER: EZT KELL MEGÍRNOD
# =============================================================================
def udp_szerver(ready=None):
    ertek = 0  # a szerver "állapota": ciklus ELŐTT, különben minden üzenetnél nullázódna
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        if ready:
            ready.set()
        while True:
            data, kliens = sock.recvfrom(1024)  # a kliens címe is jön: erre válaszolunk
            if len(data) != CMD.size:  # rossz méretű datagram: eldobjuk, ne száljon el a szerver
                continue
            nev, x = CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()  # "PLUS\x00" -> "PLUS"
            if nev == "PUSH":
                ertek = x
            elif nev == "PLUS":
                ertek += x
            elif nev == "MINUS":
                ertek -= x
            sock.sendto(REPLY.pack(ertek), kliens)  # a válasz struct, nem str(ertek).encode()!


# =============================================================================
#  Tesztkliens (ezt a ZH-n a tesztkörnyezet adja)
# =============================================================================
def kuld(sock, nev, x):
    sock.sendto(CMD.pack(nev.encode(), x), (HOST, PORT))
    data, _ = sock.recvfrom(1024)
    return REPLY.unpack(data)[0]


if __name__ == "__main__":
    ready = threading.Event()
    threading.Thread(target=udp_szerver, args=(ready,), daemon=True).start()
    ready.wait()

    print("Egy parancs mérete:", CMD.size, "bájt (nem 9! a 5s után 3 kitöltő bájt jön)")
    print("Egy csomagolt parancs:", CMD.pack(b"PLUS", 4))

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        assert kuld(sock, "PUSH", 20) == 20
        assert kuld(sock, "PLUS", 4) == 24
        assert kuld(sock, "MINUS", 5) == 19
        print("PUSH 20 -> 20, PLUS 4 -> 24, MINUS 5 -> 19   OK")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as masik:  # másik kliens, más port
        masik.settimeout(2)
        assert kuld(masik, "PLUS", 1) == 20
        print("Másik kliens is ugyanazt az állapotot látja: PLUS 1 -> 20   OK")
