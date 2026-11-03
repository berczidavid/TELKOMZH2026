"""
Helyi tesztek a "Socket ZH A" gyakorláshoz.

FIGYELEM: ez az én utánzatom, NEM a valódi tests.py. A ZH-n a megadott, valódi tests.py-t használd.
Itt nincs Docker, nincs kód. Minden egy Pythonban fut, csak a Python kell hozzá.

  python tests.py check feladat1      lefuttat mindent: elindítja a tesztszervert és a programodat
  python tests.py check feladat2
  python tests.py check feladat3

Kézi mód (két-három ablakkal, mint a ZH-n):
  python tests.py start feladat1      a tesztszerver naplója (Ctrl+C: leáll); más ablakban a kliensed:
                                      python feladat1/client.py localhost 20001
  python tests.py start feladat3      az azonosítási (UDP) tesztszerver a 20002-es porton; más ablakban:
                                      python feladat3/proxy.py 10002 20002
  python tests.py test feladat2 <port>   a saját szervered tesztelése (előbb indítsd el:
                                      python feladat2/server.py <port>)
  python tests.py test feladat3 <port>   a saját proxyd tesztelése (a start feladat3 fusson!)

Más mappából is ellenőrizhetsz (pl. a megoldásokat):  --mappa megoldasok
"""
import os
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
for stream in (sys.stdout, sys.stderr):
    stream.reconfigure(errors="replace")

PROGRAM = {"feladat1": "client.py", "feladat2": "server.py", "feladat3": "proxy.py"}


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def szoveg(b):
    return b.rstrip(b"\x00").decode(errors="replace")


class Jegyzo:
    def __init__(self):
        self.eredmenyek = []
        self.lock = threading.Lock()

    def __call__(self, ok, uzenet):
        with self.lock:
            self.eredmenyek.append(ok)
            print(("  OK   " if ok else "  HIBA ") + uzenet, flush=True)

    def osszegzes(self, cim):
        ok, n = sum(self.eredmenyek), len(self.eredmenyek)
        print(f"\n{cim}: {ok}/{n} ellenőrzés OK" + ("   -> JÓ" if n and ok == n else "   -> még dolgozz rajta"))
        return n > 0 and ok == n


# ===================================================================== 1. feladat
REQ1 = struct.Struct("6s 8s 7s")
RESP1 = struct.Struct("i 10s")
BOOK1 = struct.Struct("12s")
FORGATOKONYVEK = [  # (szabad hely, osztály, ezt kell válaszolnia a kliensnek)
    (5, "economy", "reserve"),
    (2, "economy", "reject"),
    (5, "business", "reject"),
    (3, "economy", "reserve"),
    (0, "economy", "reject"),
]


def foglalas_szerver(port, jegyzo, ready, stop):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("localhost", port))
        srv.listen(5)
        srv.settimeout(0.5)
        ready.set()
        i = 0
        while not stop.is_set():
            try:
                conn, _ = srv.accept()
            except socket.timeout:
                continue
            szabad, osztaly, vart = FORGATOKONYVEK[i % len(FORGATOKONYVEK)]
            cim = f"{szabad} szabad hely, {osztaly}"
            i += 1
            with conn:
                conn.settimeout(5)
                try:
                    d = recv_exact(conn, REQ1.size)
                    if not d:
                        jegyzo(False, f"[{cim}] a kliens nem küldött kérést")
                        continue
                    neptun, jarat, tipus = (szoveg(x) for x in REQ1.unpack(d))
                    hibak = []
                    if not neptun:
                        hibak.append("üres neptun kód")
                    if jarat != "LH2048":
                        hibak.append(f"a járatszám {jarat!r}, LH2048 kell")
                    if tipus != "request":
                        hibak.append(f"az üzenet típusa {tipus!r}, 'request' kell")
                    conn.sendall(RESP1.pack(szabad, osztaly.encode()))
                    d = recv_exact(conn, REQ1.size)
                    if not d:
                        jegyzo(False, f"[{cim}] a kliens nem küldte el a döntését (reject/reserve)")
                        continue
                    neptun2, jarat2, tipus2 = (szoveg(x) for x in REQ1.unpack(d))
                    if (neptun2, jarat2) != (neptun, jarat):
                        hibak.append("a 2. üzenetben más a neptun kód vagy a járatszám")
                    if tipus2 != vart:
                        hibak.append(f"döntés: {tipus2!r}, de {vart!r} kellett volna")
                    conn.sendall(BOOK1.pack(f"FOG{i:09d}".encode()))
                    jegyzo(not hibak, f"[{cim}] " + ("a kliens jól döntött: " + tipus2 if not hibak else "; ".join(hibak)))
                except (socket.timeout, ConnectionError, struct.error) as hiba:
                    jegyzo(False, f"[{cim}] kapcsolati hiba: {type(hiba).__name__}")


# ===================================================================== 2. feladat
CMD2 = struct.Struct("3s 6s 8s i")
REPLY2 = struct.Struct("i")


def teszt_feladat2(port, jegyzo):
    def kerdez(sock, nev, w, p, q):
        sock.sendall(CMD2.pack(nev.encode(), w.encode(), p.encode(), q))
        d = recv_exact(sock, REPLY2.size)
        if not d:
            raise ConnectionError("a szerver nem válaszolt")
        return REPLY2.unpack(d)[0]

    try:
        a = socket.create_connection(("localhost", port), timeout=3)
        b = socket.create_connection(("localhost", port), timeout=3)
    except OSError as hiba:
        jegyzo(False, f"nem tudok csatlakozni a {port}-es portra: {hiba}")
        return
    lepesek = [
        (a, "ADD", "WH001", "Laptop", 10, 10),
        (a, "GET", "WH001", "Laptop", 0, 10),
        (a, "ADD", "WH001", "Mouse", 5, 5),
        (a, "TOT", "WH001", "AAAAAAAA", 0, 15),
        (b, "ADD", "WH002", "Laptop", 3, 3),
        (b, "ADD", "WH001", "Laptop", 5, 15),
        (a, "TOT", "WH001", "AAAAAAAA", 0, 20),
        (b, "TOT", "WH002", "AAAAAAAA", 0, 3),
        (a, "GET", "WH003", "Laptop", 0, 0),
        (a, "TOT", "WH003", "AAAAAAAA", 0, 0),
    ]
    for sock, nev, w, p, q, vart in lepesek:
        try:
            kapott = kerdez(sock, nev, w, p, q)
        except (OSError, struct.error) as hiba:
            jegyzo(False, f"{nev} {w} {p} {q}: nincs válasz ({type(hiba).__name__}), a további lépéseket kihagyom")
            return
        jegyzo(kapott == vart, f"{nev} {w} {p} {q} -> {kapott} (várt: {vart})")
    a.close()
    b.close()
    try:
        with socket.create_connection(("localhost", port), timeout=3) as c:
            kapott = kerdez(c, "TOT", "WH001", "AAAAAAAA", 0)
        jegyzo(kapott == 20, f"új kapcsolat, az állapot megmaradt: TOT WH001 -> {kapott} (várt: 20)")
    except (OSError, struct.error) as hiba:
        jegyzo(False, f"új kapcsolat után: {type(hiba).__name__}")


# ===================================================================== 3. feladat
IN3 = struct.Struct("i 20s")
UDP3 = struct.Struct("5s 20s")


def azonosito_szerver(port, jegyzo, ready, stop):
    """Az Azonosítási Szerver (UDP): LOGIN / GUEST parancsra bytesztringgel válaszol."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("localhost", port))
        sock.settimeout(0.5)
        ready.set()
        while not stop.is_set():
            try:
                adat, kliens = sock.recvfrom(1024)
            except socket.timeout:
                continue
            if len(adat) != UDP3.size:
                jegyzo(False, f"az UDP szerver {len(adat)} bájtot kapott, {UDP3.size} (5s 20s) kellett volna")
                continue
            parancs, nev = (szoveg(x) for x in UDP3.unpack(adat))
            if parancs == "LOGIN":
                valasz = b"LOGIN_OK:" + nev.encode()
            elif parancs == "GUEST":
                valasz = b"GUEST_OK:" + nev.encode()
            else:
                valasz = b"ERROR:" + parancs.encode()
            sock.sendto(valasz, kliens)


def teszt_feladat3(port, jegyzo):
    def kuld(sock, tipus, nev):
        sock.sendall(IN3.pack(tipus, nev.encode()))
        return sock.recv(1024)

    try:
        a = socket.create_connection(("localhost", port), timeout=3)
        b = socket.create_connection(("localhost", port), timeout=3)
    except OSError as hiba:
        jegyzo(False, f"nem tudok csatlakozni a proxyhoz a {port}-es porton: {hiba}")
        return
    lepesek = [
        (a, 0, "anna", b"LOGIN_OK:anna", "Felhasználó kliens"),
        (b, 1, "vendeg1", b"GUEST_OK:vendeg1", "Vendég kliens"),
        (a, 0, "bela", b"LOGIN_OK:bela", "Felhasználó kliens, 2. üzenet ugyanazon a kapcsolaton"),
        (b, 1, "cili", b"GUEST_OK:cili", "Vendég kliens, 2. üzenet"),
        (a, 0, "dora", b"LOGIN_OK:dora", "váltogatás"),
    ]
    for sock, tipus, nev, vart, cim in lepesek:
        try:
            kapott = kuld(sock, tipus, nev)
        except OSError as hiba:
            jegyzo(False, f"{cim}: nincs válasz ({type(hiba).__name__}), a többit kihagyom")
            return
        jegyzo(kapott == vart, f"{cim}: ({tipus}, {nev!r}) -> {kapott!r} (várt: {vart!r})")
    a.close()
    b.close()
    try:
        with socket.create_connection(("localhost", port), timeout=3) as c:
            kapott = kuld(c, 1, "uj")
        jegyzo(kapott == b"GUEST_OK:uj", f"bontás után új kliens: -> {kapott!r} (várt: b'GUEST_OK:uj')")
    except OSError as hiba:
        jegyzo(False, f"bontás után új kliens: {type(hiba).__name__}")


# ===================================================================== segédek
def varj_port(port, proc, mp=5.0):
    vege = time.time() + mp
    while time.time() < vege:
        if proc.poll() is not None:
            return False
        try:
            socket.create_connection(("localhost", port), timeout=0.2).close()
            return True
        except OSError:
            time.sleep(0.1)
    return False


def program_utvonal(feladat, mappa):
    return os.path.join(HERE, mappa, feladat, PROGRAM[feladat])


def inditas(feladat, mappa, args):
    ut = program_utvonal(feladat, mappa)
    if not os.path.exists(ut):
        sys.exit(f"Nem találom: {ut}")
    log = open(os.path.join(tempfile.gettempdir(), f"zhA_{feladat}.log"), "w+", encoding="utf-8")
    proc = subprocess.Popen([sys.executable, ut, *map(str, args)], stdout=log, stderr=subprocess.STDOUT,
                            text=True, cwd=os.path.dirname(ut))
    return proc, log


def log_kiirasa(log, cim):
    log.flush()
    log.seek(0)
    tartalom = log.read().strip()
    if tartalom:
        print(f"--- {cim} kimenete ---")
        print("\n".join(tartalom.splitlines()[-12:]))
        print("---")


def leallit(proc):
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(5)
        except subprocess.TimeoutExpired:
            proc.kill()


# ===================================================================== parancsok
def check(feladat, mappa):
    jegyzo = Jegyzo()
    stop = threading.Event()
    print(f"== {feladat} ellenőrzése ({mappa if mappa else 'saját mappa'}) ==")
    if feladat == "feladat1":
        ready = threading.Event()
        threading.Thread(target=foglalas_szerver, args=(20001, jegyzo, ready, stop), daemon=True).start()
        ready.wait()
        for i in range(len(FORGATOKONYVEK)):
            elotte = len(jegyzo.eredmenyek)
            ut = program_utvonal(feladat, mappa)
            if not os.path.exists(ut):
                sys.exit(f"Nem találom: {ut}")
            try:
                futas = subprocess.run([sys.executable, ut, "localhost", "20001"], capture_output=True, text=True,
                                       timeout=10, cwd=os.path.dirname(ut))
            except subprocess.TimeoutExpired:
                jegyzo(False, f"{i + 1}. futás: a kliens 10 mp alatt nem fejeződött be (blokkol?)")
                time.sleep(0.3)
                continue
            time.sleep(0.3)
            if futas.returncode != 0:
                jegyzo(False, f"{i + 1}. futás: a kliens hibával állt le: {futas.stderr.strip().splitlines()[-1:]}")
            elif len(jegyzo.eredmenyek) == elotte:
                jegyzo(False, f"{i + 1}. futás: a kliens nem csatlakozott a szerverhez (üres a program?)")
    else:
        if feladat == "feladat2":
            port = 21002
            proc, log = inditas(feladat, mappa, [port])
        else:
            ready = threading.Event()
            threading.Thread(target=azonosito_szerver, args=(20002, jegyzo, ready, stop), daemon=True).start()
            ready.wait()
            port = 10002
            proc, log = inditas(feladat, mappa, [port, 20002])
        try:
            if varj_port(port, proc):
                (teszt_feladat2 if feladat == "feladat2" else teszt_feladat3)(port, jegyzo)
            else:
                jegyzo(False, f"a programod nem indult el / nem figyel a {port}-es porton")
        finally:
            leallit(proc)
            if not all(jegyzo.eredmenyek):
                log_kiirasa(log, "a programod")
    stop.set()
    return jegyzo.osszegzes(feladat)


def start(feladat):
    jegyzo = Jegyzo()
    stop = threading.Event()
    ready = threading.Event()
    if feladat == "feladat1":
        print("Foglalási tesztszerver: localhost:20001. A kliensed: python feladat1/client.py localhost 20001")
        threading.Thread(target=foglalas_szerver, args=(20001, jegyzo, ready, stop), daemon=True).start()
    elif feladat == "feladat3":
        print("Azonosítási (UDP) tesztszerver: localhost:20002. A proxyd: python feladat3/proxy.py 10002 20002")
        print("Aztán egy másik ablakban: python tests.py test feladat3 10002")
        threading.Thread(target=azonosito_szerver, args=(20002, jegyzo, ready, stop), daemon=True).start()
    else:
        print("A feladat2-höz nincs tesztszerver. Indítsd a sajátodat: python feladat2/server.py 10001,")
        print("aztán másik ablakban: python tests.py test feladat2 10001")
        return
    ready.wait()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nLeállt.")


def teszt(feladat, port):
    jegyzo = Jegyzo()
    if feladat == "feladat2":
        teszt_feladat2(port, jegyzo)
    elif feladat == "feladat3":
        teszt_feladat3(port, jegyzo)
    else:
        sys.exit("A feladat1-et a 'start feladat1' + a saját klienseddel próbáld, vagy 'check feladat1'.")
    jegyzo.osszegzes(feladat)


def main():
    args = sys.argv[1:]
    mappa = ""
    if "--mappa" in args:
        i = args.index("--mappa")
        mappa = args[i + 1]
        del args[i:i + 2]
    if len(args) >= 2 and args[0] == "check" and args[1] in PROGRAM:
        sys.exit(0 if check(args[1], mappa) else 1)
    if len(args) >= 2 and args[0] == "start" and args[1] in PROGRAM:
        return start(args[1])
    if len(args) == 3 and args[0] == "test" and args[1] in PROGRAM and args[2].isdigit():
        return teszt(args[1], int(args[2]))
    print(__doc__)


if __name__ == "__main__":
    main()
