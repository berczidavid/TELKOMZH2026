r"""
F3: UDP SZERVER                                   (gyakorlás a ZH 3. feladat a) részéhez)

Írj UDP szervert, ami egy egész számot tárol (kezdetben 0).

  - A parancsok "6s i" formátumban jönnek (parancs + szám):
        SETVAL x -> az érték legyen x
        ADD x    -> az érték nő x-szel
        SUB x    -> az érték csökken x-szel
        DOUBLE   -> az érték megduplázódik (a szám ilyenkor érdektelen)
  - A válasz: az új érték STRUCT-ban, "i" formátumban (NEM bytesztring!).
  - Ismeretlen parancsra az érték nem változik, de a jelenlegi értéket visszaküldöd.

Tippek (ha elakadsz: peldak/p2_udp_szerver.py):
  - UDP-nél nincs listen/accept: bind, aztán ciklusban recvfrom / sendto
  - a feladó címére válaszolj: sock.sendto(adat, kliens)
  - a parancsnév: nev.rstrip(b"\x00").decode()

Futtatás:  python3 f3_udp_szerver.py
"""
import socket
import struct

CMD = struct.Struct("6s i")
REPLY = struct.Struct("i")


def udp_szerver(port):
    # TODO: ide írd a megoldást
    ertek = 0  # a szerver "állapota": ciklus ELŐTT, különben minden üzenetnél nullázódna
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("localhost", port))
        while True:
            data, kliens = sock.recvfrom(1024)  # a kliens címe is jön: erre válaszolunk
            if len(data) != CMD.size:  # rossz méretű datagram: eldobjuk, ne száljon el a szerver
                continue
            nev, x = CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()  # "PLUS\x00" -> "PLUS"
            if nev == "SETVAL":
                ertek = x
            elif nev == "ADD":
                ertek += x
            elif nev == "SUB":
                ertek -= x
            elif nev == "DOUBLE":
                ertek *= 2
            sock.sendto(REPLY.pack(ertek), kliens)  # a válasz struct, nem str(ertek).encode()!




# ----------------------------------------------------------------------------
#  Ellenőrzés (ezt ne módosítsd)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    from ref_szerverek import egyezik, futtat, inditas_udp

    PORT = 12004

    def kuld(sock, nev, x):
        sock.sendto(CMD.pack(nev.encode(), x), ("localhost", PORT))
        adat, _ = sock.recvfrom(1024)
        return REPLY.unpack(adat)[0]

    def teszt():
        inditas_udp(udp_szerver, PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as a, socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM
        ) as b:
            a.settimeout(2)
            b.settimeout(2)
            egyezik("SETVAL 7", kuld(a, "SETVAL", 7), 7)
            egyezik("ADD 5", kuld(a, "ADD", 5), 12)
            egyezik("SUB 2", kuld(a, "SUB", 2), 10)
            egyezik("DOUBLE", kuld(a, "DOUBLE", 0), 20)
            egyezik("másik kliens: ADD 1", kuld(b, "ADD", 1), 21)
            egyezik("ismeretlen parancs", kuld(b, "FOO", 5), 21)

    futtat("F3", teszt)
