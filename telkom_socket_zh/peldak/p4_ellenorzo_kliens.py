"""
P4: ELLENŐRZŐ KLIENS                          (ZH 3. feladat b) része)

A helyzet:
  - Van egy TCP szerver (IN / INCR / DECR, (4s i), válasz: bytesztring)  -> ez megbízható
  - Van egy UDP szerver (PUSH / PLUS / MINUS, (5s i), válasz: (i))        -> ez néha HIBÁZIK:
    minden parancsnál a kapott számhoz véletlenszerűen hozzáad -1, 0 vagy 1 értéket.
  - Az ellenőrző kliens mindkét szervertől lekérdezi az értéket ("0-val való növelés"),
    és a két érték összehasonlításából megmondja, hibázott-e az UDP szerver.

Lépések (ez a feladat teljes váza):
  1) TCP szervernek:  INCR 0  -> b"19"       -> int(...)
  2) UDP szervernek:  PLUS 0  -> (i) válasz    -> unpack
  3) tcp_ertek != udp_ertek  ->  az UDP szerver hibázott

Futtatás:  python3 p4_ellenorzo_kliens.py
"""
import random
import socket
import struct
import threading

HOST = "localhost"
TCP_PORT = 11005
UDP_PORT = 11006

TCP_CMD = struct.Struct("4s i")
UDP_CMD = struct.Struct("5s i")
REPLY = struct.Struct("i")


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


# =============================================================================
#  EZT A ZH-N MEGKAPOD: a megbízható TCP szerver és a hibás UDP szerver
# =============================================================================
def tcp_szerver(ready):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, TCP_PORT))
        srv.listen(5)
        ready.set()
        while True:
            conn, _ = srv.accept()
            with conn:
                while data := recv_exact(conn, TCP_CMD.size):
                    nev, x = TCP_CMD.unpack(data)
                    nev = nev.rstrip(b"\x00").decode()
                    if nev == "IN":
                        ertek = x
                    elif nev == "INCR":
                        ertek += x
                    elif nev == "DECR":
                        ertek -= x
                    conn.sendall(str(ertek).encode())


def hibas_udp_szerver(ready):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, UDP_PORT))
        ready.set()
        while True:
            data, kliens = sock.recvfrom(1024)
            nev, x = UDP_CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()
            x += random.choice([-1, 0, 1])  # <- itt "hibázik"
            if nev == "PUSH":
                ertek = x
            elif nev == "PLUS":
                ertek += x
            elif nev == "MINUS":
                ertek -= x
            sock.sendto(REPLY.pack(ertek), kliens)


# =============================================================================
#  ELLENŐRZŐ KLIENS: EZT KELL MEGÍRNOD
# =============================================================================
def tcp_ertek():
    with socket.create_connection((HOST, TCP_PORT)) as sock:
        sock.sendall(TCP_CMD.pack(b"INCR", 0))  # "0-val való növelés" = lekérdezés
        return int(sock.recv(1024))  # b"19" -> 19 (az int() bájtot is elfogad)


def udp_ertek():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(UDP_CMD.pack(b"PLUS", 0), (HOST, UDP_PORT))
        data, _ = sock.recvfrom(1024)
    return REPLY.unpack(data)[0]  # a struct válasz egy 1 elemű tuple: [0] kell


def hibazott_e():
    t = tcp_ertek()
    u = udp_ertek()
    return t != u, t, u


# =============================================================================
#  Előkészítés + próba (csak a gyakorláshoz)
# =============================================================================
def beallit(ertek):
    """Mindkét szervert ugyanarra az értékre állítja (az UDP ezt is elronthatja!)."""
    with socket.create_connection((HOST, TCP_PORT)) as sock:
        sock.sendall(TCP_CMD.pack(b"IN", ertek))
        sock.recv(1024)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(UDP_CMD.pack(b"PUSH", ertek), (HOST, UDP_PORT))
        sock.recvfrom(1024)


if __name__ == "__main__":
    random.seed(7)  # hogy minden futás ugyanazt mutassa
    for fn in (tcp_szerver, hibas_udp_szerver):
        ready = threading.Event()
        threading.Thread(target=fn, args=(ready,), daemon=True).start()
        ready.wait()

    beallit(100)
    print("Ellenőrzések (TCP érték, UDP érték, hibázott-e):")
    for i in range(1, 9):
        hibas, t, u = hibazott_e()
        print(f"  {i}. kérdés: TCP={t:4d}  UDP={u:4d}  -> {'HIBÁZOTT' if hibas else 'egyezik'}")
    print("\nMegfigyelés: ha az UDP egyszer elcsúszik, az eltérés megmarad (az érték tárolt).")
