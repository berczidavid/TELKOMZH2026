r"""
F2: TCP SZERVER select-tel                        (gyakorlás a ZH 2. feladatához)

Írj olyan TCP szervert, ami select-tel egyszerre több klienst szolgál ki.

  - A szerver egy egész számot tárol (kezdetben 0), ezen osztozik minden kliens.
  - A parancsok "5s i" formátumban jönnek (parancs + szám):
        SET x  -> az érték legyen x
        ADD x  -> az érték nő x-szel
        MUL x  -> az érték szorzódik x-szel
  - Minden parancs után a szerver visszaküldi az új értéket SIMA BYTESZTRINGKÉNT (b"45").
  - Ismeretlen parancsra b"ERR" a válasz, és az érték NEM változik.
  - Ha egy kliens lebontja a kapcsolatot, a szerver menjen tovább.

Tippek (ha elakadsz: peldak/p3_select_tcp_szerver.py):
  - inputs = [server]; select.select(inputs, [], [], 1.0)
  - ha s is server -> accept; különben recv_exact (b"" = bontott)
  - a parancsnév: nev.rstrip(b"\x00").decode()

Futtatás:  python3 f2_select_szerver.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import select
import socket
import struct

CMD = struct.Struct("5s i")


def recv_exact(sock, size):  # kész, másold be a saját segédletedbe is
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", port))
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
                    adat = recv_exact(s, CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = CMD.unpack(adat)
                nev = nev.rstrip(b"\x00").decode()
                if nev == "SET":
                    ertek = x
                elif nev == "ADD":
                    ertek += x
                elif nev == "MUL":
                    ertek *= x
                else:
                    s.sendall(b"ERR")
                    continue
                s.sendall(str(ertek).encode())


# ----------------------------------------------------------------------------
#  Ellenőrzés (ezt ne módosítsd)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    from ref_szerverek import egyezik, futtat, inditas_tcp

    PORT = 12003

    def kuld(sock, nev, x):
        sock.sendall(CMD.pack(nev.encode(), x))
        return sock.recv(1024)

    def teszt():
        inditas_tcp(szerver, PORT, port=PORT)
        a = socket.create_connection(("localhost", PORT), timeout=3)
        b = socket.create_connection(("localhost", PORT), timeout=3)
        egyezik("SET 10", kuld(a, "SET", 10), b"10")
        egyezik("ADD 5 (másik kliens)", kuld(b, "ADD", 5), b"15")
        egyezik("MUL 3", kuld(a, "MUL", 3), b"45")
        egyezik("ismeretlen parancs", kuld(b, "FOO", 1), b"ERR")
        egyezik("ADD 1 (az ERR nem változtathatott)", kuld(a, "ADD", 1), b"46")
        a.close()
        b.close()
        with socket.create_connection(("localhost", PORT), timeout=3) as c:
            egyezik("új kapcsolat, az érték megmaradt", kuld(c, "ADD", 0), b"46")

    futtat("F2", teszt)
