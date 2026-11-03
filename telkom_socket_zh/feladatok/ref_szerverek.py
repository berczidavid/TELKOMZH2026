"""
Segédfájl a gyakorló feladatokhoz: a "ZH-n megkapott" szerverek itt vannak.
NEM kell megnyitnod, nem kell módosítanod. (Ha megnyitod, spoilerezhetsz magadnak.)
"""
import socket
import struct
import threading
import time


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def egyezik(nev, kapott, vart):
    """Összehasonlít, és érthető hibaüzenetet ad."""
    if kapott != vart:
        raise AssertionError(f"{nev}: kapott {kapott!r}, de {vart!r} kellett volna")


def futtat(cim, teszt):
    """Lefuttat egy tesztet, és barátságosan kiírja az eredményt."""
    try:
        teszt()
        print(f"{cim}: minden teszt OK")
    except NotImplementedError:
        print(f"{cim}: még nincs megírva (raise NotImplementedError)")
    except AssertionError as hiba:
        print(f"{cim}: HIBA: {hiba}")


def _szalban(fuggveny, args):
    hiba = []

    def cel():
        try:
            fuggveny(*args)
        except NotImplementedError:
            hiba.append(True)

    threading.Thread(target=cel, daemon=True).start()
    return hiba


def inditas_tcp(fuggveny, *args, port):
    """Szálban elindítja a függvényt, és megvárja, amíg a TCP port felvesz kapcsolatot."""
    hiba = _szalban(fuggveny, args)
    for _ in range(50):
        if hiba:
            raise NotImplementedError
        try:
            socket.create_connection(("localhost", port), timeout=0.2).close()
            return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"A szerver nem indult el a {port}-es porton (rossz port? kivétel a szerverben?)")


def inditas_udp(fuggveny, *args):
    """UDP-nél nincs mit megvárni, kis szünet a bind-hoz."""
    hiba = _szalban(fuggveny, args)
    time.sleep(0.3)
    if hiba:
        raise NotImplementedError


# ---------------------------------------------------------------- F1 szerverei
F1_REQ = struct.Struct("16s i")


def _f1_valasz(adat):
    szoveg, n = F1_REQ.unpack(adat)
    return struct.pack(f"{n}s", szoveg.rstrip(b"\x00").decode()[-n:].upper().encode())


def f1_tcp_szerver(port):
    with socket.socket() as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("localhost", port))
        srv.listen(5)
        while True:
            conn, _ = srv.accept()
            with conn:
                adat = recv_exact(conn, F1_REQ.size)
                if adat:
                    conn.sendall(_f1_valasz(adat))


def f1_udp_szerver(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as srv:
        srv.bind(("localhost", port))
        while True:
            adat, kliens = srv.recvfrom(1024)
            srv.sendto(_f1_valasz(adat), kliens)


# ------------------------------------------------- F3 szervere (az F5-höz kell)
F3_CMD = struct.Struct("6s i")
F3_REPLY = struct.Struct("i")


def f3_udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("localhost", port))
        while True:
            adat, kliens = sock.recvfrom(1024)
            nev, x = F3_CMD.unpack(adat)
            nev = nev.rstrip(b"\x00").decode()
            if nev == "SETVAL":
                ertek = x
            elif nev == "ADD":
                ertek += x
            elif nev == "SUB":
                ertek -= x
            elif nev == "DOUBLE":
                ertek *= 2
            sock.sendto(F3_REPLY.pack(ertek), kliens)


# ---------------------------------------------------------------- F4 szerverei
ZH_TCP_CMD = struct.Struct("4s i")
ZH_UDP_CMD = struct.Struct("5s i")
ZH_REPLY = struct.Struct("i")


def zh_tcp_szerver(port):
    ertek = 0
    with socket.socket() as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("localhost", port))
        srv.listen(5)
        while True:
            conn, _ = srv.accept()
            with conn:
                while adat := recv_exact(conn, ZH_TCP_CMD.size):
                    nev, x = ZH_TCP_CMD.unpack(adat)
                    nev = nev.rstrip(b"\x00").decode()
                    if nev == "IN":
                        ertek = x
                    elif nev == "INCR":
                        ertek += x
                    elif nev == "DECR":
                        ertek -= x
                    conn.sendall(str(ertek).encode())


def hibas_udp_szerver(port, elteresek):
    """Minden parancsnál a listából a következő eltérést adja a számhoz (körbeforog)."""
    ertek = 0
    i = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("localhost", port))
        while True:
            adat, kliens = sock.recvfrom(1024)
            nev, x = ZH_UDP_CMD.unpack(adat)
            nev = nev.rstrip(b"\x00").decode()
            x += elteresek[i % len(elteresek)]
            i += 1
            if nev == "PUSH":
                ertek = x
            elif nev == "PLUS":
                ertek += x
            elif nev == "MINUS":
                ertek -= x
            sock.sendto(ZH_REPLY.pack(ertek), kliens)
