"""
P3: TCP SZERVER select-tel, több klienst egyszerre kiszolgál      (ZH 2. feladat)

A feladat:
  - A szerver egy egész számot tárol (kezdetben 0), ezen osztozik MINDEN kliens.
  - Parancsok (4s i) formátumban:  IN x (beállít), INCR x (növel), DECR x (csökkent)
  - Minden parancs után visszaküldi az új értéket SIMA BYTESZTRINGKÉNT: b"24"
  - Példa: IN 20 -> b"20", INCR 4 -> b"24", DECR 5 -> b"19"

A select ötlete (ez a lényeg!):
  select.select(inputs, [], [], 1.0)  megmondja, melyik socketen van TEENDŐ:
    - a figyelő (server) socketen teendő = új kliens akar csatlakozni -> accept
    - egy kliens socketen teendő = üzenet jött (vagy bontott) -> recv

Futtatás:  python3 p3_select_tcp_szerver.py
"""
import select
import socket
import struct
import threading

HOST = "localhost"
PORT = 11004

CMD = struct.Struct("4s i")  # "IN\x00\x00", "INCR", "DECR" + szám = 8 bájt


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


# =============================================================================
#  SZERVER: EZT KELL MEGÍRNOD
# =============================================================================
def select_szerver(ready=None):
    ertek = 0  # közös állapot, a ciklus előtt
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # újraindításnál ne akadjon
        server.bind((HOST, PORT))
        server.listen(5)
        if ready:
            ready.set()
        inputs = [server]  # amiket figyelünk: a figyelő socket + az összes kliens
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)  # 1 mp timeout: Ctrl+C-nek is jó
            for s in readable:
                if s is server:  # 1) új kliens
                    kliens, cim = server.accept()
                    inputs.append(kliens)
                    continue
                try:  # 2) meglévő kliens: üzenet vagy bontás
                    data = recv_exact(s, CMD.size)
                except ConnectionResetError:  # Windowson bontáskor előfordulhat ez b"" helyett
                    data = b""
                if not data:  # b"" = a kliens bontott
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = CMD.unpack(data)
                nev = nev.rstrip(b"\x00").decode()
                if nev == "IN":
                    ertek = x
                elif nev == "INCR":
                    ertek += x
                elif nev == "DECR":
                    ertek -= x
                s.sendall(str(ertek).encode())  # bytesztring: b"24"


# =============================================================================
#  Tesztkliensek (a ZH-n a tesztkörnyezet adja)
# =============================================================================
def kuld(sock, nev, x):
    sock.sendall(CMD.pack(nev.encode(), x))
    return sock.recv(1024)


if __name__ == "__main__":
    ready = threading.Event()
    threading.Thread(target=select_szerver, args=(ready,), daemon=True).start()
    ready.wait()

    # Két kliens EGYSZERRE csatlakozik: ezt egy sima (nem select-es) szerver nem bírná
    a = socket.create_connection((HOST, PORT))
    b = socket.create_connection((HOST, PORT))
    assert kuld(a, "IN", 20) == b"20"
    assert kuld(b, "INCR", 4) == b"24"  # a "b" kliens az "a" által beállított értéket látja
    assert kuld(a, "DECR", 5) == b"19"
    print("IN 20 -> 20, INCR 4 -> 24, DECR 5 -> 19 (két kliens váltogatva)   OK")
    a.close()
    b.close()

    with socket.create_connection((HOST, PORT)) as c:  # az érték a kapcsolatok után is megmarad
        assert kuld(c, "INCR", 0) == b"19"
    print("Új kapcsolat is a közös állapotot látja: INCR 0 -> 19   OK")
