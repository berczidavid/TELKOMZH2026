"""
1. feladat: járatfoglalás (6 pont)              TCP KLIENS
Indítás:  python client.py localhost 20001      (cím és port a parancssorból: sys.argv)

A kliens egy kapcsolaton, két üzenetet küld a tesztszervernek, mindkettő formátuma: (6s 8s 7s)
   (neptun kód, járatszám, üzenet típusa)

1) Első üzenet: (neptun, "LH2048", "request")
   A szerver válasza: (i 10s) = (szabad helyek száma, utazási osztály)
   Az osztály lehet "economy" vagy "business".

2) Neked legalább 3 szabad helyre van szükséged economy osztályon.
   - ha az osztály nem economy, VAGY a szabad helyek száma kisebb mint 3:
        második üzenet: (neptun, járatszám, "reject")
   - különben:
        második üzenet: (neptun, járatszám, "reserve")

3) A szerver végső válasza ("reject" és "reserve" esetén is): foglalási azonosító, formátum (12s)

Ellenőrzés:  python tests.py check feladat1
"""
import socket
import struct
import sys

KERES = struct.Struct("6s 8s 7s") #(neptun kód, járatszám, üzenet típusa)
VALASZ = struct.Struct("i 10s") #szabad helyek száma, utazási osztály
VEGSO = struct.Struct("12s") #foglalási azonosító

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




# ide írd a megoldást
def feladatA():
    host, port = sys.argv[1], int(sys.argv[2])
    with socket.create_connection((host,port)) as sock:
        sock.sendall(KERES.pack(b"CS8jjc", b"LH2048", b"request"))
        szam, szoveg = VALASZ.unpack(recv_exact(sock, VALASZ.size))
        szoveg = sz(szoveg)
        if(szoveg != "economy" or szam < 3):
            sock.sendall(KERES.pack(b"CS8JJC", b"LH2048", b"reject"))
        else:
            sock.sendall(KERES.pack(b"CS8JJC", b"LH2048", b"reserve"))
        (vegso, ) = VEGSO.unpack(recv_exact(sock, VEGSO.size))
         


if __name__ == "__main__":
    feladatA()
