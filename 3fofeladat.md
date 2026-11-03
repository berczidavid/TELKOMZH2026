Itt a három feladat megoldása magyarázattal. A kódot lefuttattam a saját helyi tesztemmel (5/5, 11/11 és 7/7 ellenőrzés zöld). A valódi `check`-kel még nem próbáltam, ezért azt ma este futtasd le.

## Közös fej (mindhárom fájl elejére)

```python
import select
import socket
import struct
import sys


def recv_exact(sock, size):          # TCP-n a fix méretű üzenet beolvasása
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:                # üres = a másik oldal bontott
            return b""
        data += chunk
    return data
```

Az 1. feladatnál a `select` importra nincs szükség, de nem baj, ha ott van.

---

## 1. feladat: járatfoglalás (`feladat1/client.py`)

**Gondolatmenet:** kliens vagy, ezért te kezdeményezel. Két üzenet megy **ugyanazon a kapcsolaton**: előbb a kérdés (`request`), a válasz alapján a döntés (`reject` vagy `reserve`), a végén a szerver a foglalási azonosítót küldi.

```python
REQ = struct.Struct("6s 8s 7s")   # neptun, járatszám, üzenet típusa
RESP = struct.Struct("i 10s")     # szabad helyek, utazási osztály
BOOK = struct.Struct("12s")       # foglalási azonosító

NEPTUN = b"ABC123"                # <-- a saját neptun kódod (6 karakter)
JARAT = b"LH2048"
OSZTALY = "economy"
MIN_HELY = 3


def main():
    host, port = sys.argv[1], int(sys.argv[2])                     # python client.py localhost 20001
    with socket.create_connection((host, port)) as sock:
        sock.sendall(REQ.pack(NEPTUN, JARAT, b"request"))            # 1. üzenet
        szabad, osztaly = RESP.unpack(recv_exact(sock, RESP.size))   # válasz: pontosan 14 bájt
        osztaly = osztaly.rstrip(b"\x00").decode()                   # bájt -> szöveg, hogy össze tudd hasonlítani
        if osztaly != OSZTALY or szabad < MIN_HELY:                  # "vagy": elég az egyik feltétel
            tipus = b"reject"
        else:
            tipus = b"reserve"
        sock.sendall(REQ.pack(NEPTUN, JARAT, tipus))                 # 2. üzenet, UGYANAZON a kapcsolaton
        (azonosito,) = BOOK.unpack(recv_exact(sock, BOOK.size))      # végső válasz (12 bájt)
        print(tipus.decode(), azonosito.rstrip(b"\x00").decode())


if __name__ == "__main__":
    main()
```

**Miért így:**
- **`recv_exact(sock, RESP.size)`**: a TCP bájtfolyam, a `recv` kevesebbet is adhat. A `.size` 14, ezt soha ne írd be kézzel.
- **`.rstrip(b"\x00").decode()`**: az `s` mező nullákkal van kipótolva, enélkül a `"economy"` nem egyezne.
- **A neptun kód konstans**, így mindkét üzenetben ugyanaz (ez volt az elírás a próbálkozásodban).
- **A 2. üzenet a `with` belül van**, különben a kapcsolat már zárva lenne.
- **A feltétel:** ha az osztály nem economy **vagy** kevesebb mint 3 hely van, akkor `reject`.

---

## 2. feladat: raktárkészlet (`feladat2/server.py`)

**Gondolatmenet:** select-es szerver, az állapot egy **szótár a szótárban** (`raktár -> termék -> darabszám`). A kliens `(3s 6s 8s i)` parancsot küld, a szerver struct `(i)` választ ad.

```python
CMD = struct.Struct("3s 6s 8s i")   # parancs, raktár, termék, mennyiség: 24 bájt (kitöltés miatt)
REPLY = struct.Struct("i")
ADD, GET, TOT = "ADD", "GET", "TOT"


def main():
    port = int(sys.argv[1])                                   # python server.py <port>
    raktar = {}                                               # a ciklus ELŐTT: {raktár: {termék: darab}}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", port))
        server.listen(5)
        inputs = [server]
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:                               # új kliens
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, CMD.size)
                except ConnectionResetError:                  # Windows: hirtelen bontás
                    adat = b""
                if not adat:                                  # a kliens bontott
                    inputs.remove(s)
                    s.close()
                    continue
                nev, w, p, q = CMD.unpack(adat)
                nev, w, p = (x.rstrip(b"\x00").decode() for x in (nev, w, p))
                ertek = 0
                if nev == ADD:
                    termekek = raktar.setdefault(w, {})       # ha nincs ilyen raktár, létrehozza
                    termekek[p] = termekek.get(p, 0) + q      # ha nincs ilyen termék, 0-ról indul
                    ertek = termekek[p]                       # ADD után: a termék darabszáma
                elif nev == GET:
                    ertek = raktar.get(w, {}).get(p, 0)       # nincs raktár/termék: 0
                elif nev == TOT:
                    ertek = sum(raktar.get(w, {}).values())   # a raktár összes termékének összege
                s.sendall(REPLY.pack(ertek))                  # struct válasz, NEM bytesztring


if __name__ == "__main__":
    main()
```

**Miért így:**
- **Az állapot (`raktar`) a ciklus előtt van**, különben minden üzenetnél nullázódna.
- **`setdefault`** létrehozza a belső szótárat, ha még nincs. **`get(w, {}).get(p, 0)`** hiba nélkül ad 0-t, ha valami nincs.
- **A válasz struct (`REPLY.pack`)**: a feladat `(i)`-t kér, ez ellenkezik a minta ZH-val, ahol bytesztring volt.
- **`recv_exact` a select-ben** akkor jó, ha a kliens teljes parancsot küld. A ZH szerint nem küld hibás üzenetet.
- **Az `if not adat` ág** a bontott klienst veszi ki a listából. Ha ezt kihagyod, a szerver végtelen ciklusban pörög.

---

## 3. feladat: azonosítási proxy (`feladat3/proxy.py`)

**Gondolatmenet:** ugyanaz a select-es szerver elöl, mint a 2. feladatban, de nem tárol állapotot, hanem **átfordít és továbbít**: `(i 20s)` jön a klienstől, `(5s 20s)` megy az UDP szervernek, a válasza **változatlanul** megy vissza.

```python
IN = struct.Struct("i 20s")                 # kliens felől: típus, név (24 bájt)
OUT = struct.Struct("5s 20s")               # UDP szerver felé: parancs, név (25 bájt)
PARANCS = {0: b"LOGIN", 1: b"GUEST"}        # típus -> parancs (az átfordítás)


def main():
    port, szerver_port = int(sys.argv[1]), int(sys.argv[2])     # python proxy.py <port> <szerver_port>
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)       # EGY UDP socket, a ciklus előtt
    udp.settimeout(3)                                            # különben lefagy, ha nem jön válasz
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", port))
        server.listen(5)
        inputs = [server]                                        # az UDP socket NEM kerül ide
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, IN.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                tipus, nev = IN.unpack(adat)                     # a nev bájt marad, nem kell dekódolni
                udp.sendto(OUT.pack(PARANCS[tipus], nev), ("localhost", szerver_port))
                valasz, _ = udp.recvfrom(1024)                   # az UDP szerver bytesztring válasza
                s.sendall(valasz)                                # változatlanul vissza a kliensnek


if __name__ == "__main__":
    main()
```

**Miért így:**
- **`PARANCS` szótár** az átfordítás, a feladat magja: 0 megy `LOGIN`-ba, 1 `GUEST`-be.
- **Két különböző formátum**: `IN` (kliens felől, 24 bájt), `OUT` (UDP felé, 25 bájt). A válasz **nem struct**, hanem bytesztring, ezért nem is csomagolod ki.
- **Egy UDP socket a ciklus előtt**, és a `recvfrom` rögtön a `sendto` után: a választ azonnal megvárod, ezért nem kell a select-be.
- **A `settimeout(3)`** nélkül a proxy örökre lefagyna, ha az UDP szerver nem válaszol.
- A bontás kezelése ugyanaz, mint a 2. feladatban.

---

## Holnap erre figyelj

A csoporttárs szerint a paraméterek változnak, a szerkezet nem. Olvasd végig a feladatlapot, és vesd össze:

| Feladat | Mit hasonlíts össze |
|---|---|
| 1. | járatszám, keresett osztály, küszöb (3), mezőszélességek, neptun kódod |
| 2. | parancsnevek, struct szélességek, mit ad vissza a `TOT` |
| 3. | kliens típus számok (0/1), parancsnevek, formátumok, **hány backend van** (egy UDP, vagy TCP és UDP) |

A megoldásokban a változó adatok konstansként a fájlok tetején vannak, ott gyorsan átírhatod.

## Ellenőrzés

```
python tests.py check <KÓD> feladat1      (a kódot a feladatlapról másold, kis/nagybetű számít)
```
A `check` a végén kiírja a kódokat, azokat kell a Moodle kvízbe beírnod. A Docker Desktopnak előtte futnia kell.

**Ami a legjobban segít:** ne csak másold, hanem írd meg a 2. és a 3. feladatot **puska nélkül**, a saját szavaiddal. Ha menet közben valamit nem értesz, kérdezd meg itt, például hogy miért `setdefault`, vagy miért nem kell a select-be az UDP socket.


---
---

# MELLÉKLET: SOR-SOR MAGYARÁZAT (ugyanaz a kód, minden sor kommentelve)

A fenti három megoldás itt még egyszer szerepel, **1:1 ugyanaz a kód**, csak minden sor mellé odaírtam, mit csinál és miért. Nem kell megtanulnod a kommenteket, azok a megértést segítik. A ZH-n a kommentek nélküli változat a gyorsabb.

## Fogalmak röviden (ha egy szót nem ismersz)

| Fogalom | Mit jelent |
|---|---|
| **socket** | a programod "csatlakozója" a hálózathoz; a címe `(gép, port)` |
| **TCP** (`SOCK_STREAM`) | kapcsolatos, megbízható bájtfolyam; van `connect` / `accept`, nincs üzenethatár |
| **UDP** (`SOCK_DGRAM`) | kapcsolat nélküli, különálló csomagok; `sendto` / `recvfrom`, egy hívás = egy csomag |
| **port** | egy szám, amely megmondja, a gépen melyik program kapja az adatot |
| **bind** | a socketet egy címhez és porthoz köti (szerver oldalon) |
| **listen** | a szerver socket elkezd kapcsolatokat fogadni |
| **accept** | elfogad egy csatlakozó klienst, és visszaad egy új socketet hozzá |
| **sendall** | az egész adatot elküldi (a `send` néha csak egy részét küldi) |
| **recv** | a socketből olvas legfeljebb annyi bájtot, amennyit kérsz (kevesebbet is adhat!) |
| **sendto / recvfrom** | UDP küldés és fogadás; a fogadás a feladó címét is megadja |
| **select** | megmondja, melyik socketen van teendő, így egy program több klienst kezel egyszerre |
| **bájt (`b"..."`)** | nyers adat; a hálózaton ez megy, nem a szöveg |
| **encode / decode** | szöveg átalakítása bájtokká, illetve bájtok szöveggé |
| **struct** | modul, amely adatokat meghatározott formátumú bájtokká csomagol, és vissza |
| **`s` és `i` a formátumban** | `s` = fix hosszú bájtsor (pl. `6s` = 6 bájt), `i` = egész szám (4 bájt) |
| **pack / unpack** | csomagolás bájtokká / kicsomagolás; az `unpack` mindig **tuple**-t ad |
| **`.size`** | egy `Struct` mérete bájtban (a kitöltés miatt lehet több, mint az összeg) |
| **`rstrip(b"\x00")`** | a kipótolt nulla bájtok levágása a mező végéről |
| **`with`** | blokk, amely a végén magától lezárja a socketet |
| **szótár (`{}`)** | kulcs-érték tároló; `get` hiba nélkül kérdez, `setdefault` létrehoz, ha nincs |

## Közös fej, minden sor kommentelve

```python
import select                         # a select modul: megmondja, melyik socketen van teendő (több klienshez kell)
import socket                         # a socket modul: hálózati kapcsolatok létrehozása (TCP, UDP)
import struct                         # a struct modul: számok és szövegek bájtokká alakítása és vissza
import sys                            # a sys modul: itt a parancssori argumentumokhoz (sys.argv)


def recv_exact(sock, size):           # függvény: pontosan 'size' bájtot olvas a socketből (a recv kevesebbet is adhat)
    data = b""                        # ide gyűjtjük a bájtokat; üres bájtsorral indulunk (a b"" bájt, nem szöveg)
    while len(data) < size:           # addig ismételünk, amíg meg nincs a kért mennyiség
        chunk = sock.recv(size - len(data))   # a még hiányzó bájtokat kérjük (legfeljebb ennyit)
        if not chunk:                 # üres darab = a másik oldal lezárta a kapcsolatot
            return b""                # jelezzük a hívónak: nincs több adat (bontás)
        data += chunk                 # a kapott darabot hozzáfűzzük az eddigiekhez
    return data                       # megvan a teljes üzenet, visszaadjuk
```

## 1. feladat, minden sor kommentelve

```python
REQ = struct.Struct("6s 8s 7s")       # a kérés formátuma: 6 bájt neptun, 8 bájt járatszám, 7 bájt típus
RESP = struct.Struct("i 10s")         # a szerver válasza: egy egész (szabad helyek) + 10 bájt szöveg (osztály)
BOOK = struct.Struct("12s")           # a végső válasz: 12 bájt szöveg (foglalási azonosító)

NEPTUN = b"ABC123"                    # a saját neptun kódod bájtként (b"..."), pontosan 6 karakter
JARAT = b"LH2048"                     # a keresett járatszám, szintén bájtként
OSZTALY = "economy"                   # a keresett osztály; ez sima szöveg, mert szöveggel hasonlítjuk össze
MIN_HELY = 3                          # legalább ennyi szabad hely kell


def main():                           # a program fő függvénye
    host, port = sys.argv[1], int(sys.argv[2])   # parancssorból: 1. argumentum a gép neve, 2. a port (számmá alakítva)
    with socket.create_connection((host, port)) as sock:   # TCP kapcsolat a szerverhez; a with a végén lezárja a socketet
        sock.sendall(REQ.pack(NEPTUN, JARAT, b"request"))   # az 1. üzenet bájtokká csomagolva, teljes egészében elküldve
        szabad, osztaly = RESP.unpack(recv_exact(sock, RESP.size))   # pontosan 14 bájtot olvasunk, és két értékre bontjuk
        osztaly = osztaly.rstrip(b"\x00").decode()   # a kipótolt nullákat levágjuk, majd a bájtokat szöveggé alakítjuk
        if osztaly != OSZTALY or szabad < MIN_HELY:   # ha az osztály nem a keresett VAGY kevés a hely...
            tipus = b"reject"         # ...elutasítjuk
        else:                         # különben (az osztály jó ÉS elég a hely)
            tipus = b"reserve"        # foglalunk
        sock.sendall(REQ.pack(NEPTUN, JARAT, tipus))   # a 2. üzenet UGYANAZON a kapcsolaton, ugyanazzal a formátummal
        (azonosito,) = BOOK.unpack(recv_exact(sock, BOOK.size))   # a végső válasz (12 bájt); az unpack tuple-t ad, ezért a zárójel
        print(tipus.decode(), azonosito.rstrip(b"\x00").decode())   # kiírjuk a döntést és az azonosítót szövegként


if __name__ == "__main__":            # csak akkor fusson, ha közvetlenül indítják (nem importálják)
    main()                            # a fő függvény indítása
```

## 2. feladat, minden sor kommentelve

```python
CMD = struct.Struct("3s 6s 8s i")     # a kliens parancsa: 3 bájt parancs, 6 bájt raktár, 8 bájt termék, egy egész (mennyiség)
REPLY = struct.Struct("i")            # a válasz: egyetlen egész szám (4 bájt)
ADD, GET, TOT = "ADD", "GET", "TOT"   # a három parancs neve szövegként (így egy helyen átírhatók)


def main():                           # a program fő függvénye
    port = int(sys.argv[1])           # a port a parancssorból jön: python server.py <port>
    raktar = {}                       # az állapot: szótár a szótárban {raktár: {termék: darab}}; a ciklus ELŐTT jön létre
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:   # TCP szerver socket (AF_INET = IPv4, SOCK_STREAM = TCP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # újraindításnál a port azonnal újra használható
        server.bind(("localhost", port))   # a socketet a saját gép adott portjához kötjük
        server.listen(5)              # figyelni kezd; legfeljebb 5 várakozó kapcsolat
        inputs = [server]             # a figyelt socketek listája: az elején csak a figyelő socket
        while True:                   # a szerver örökké fut
            readable, _, _ = select.select(inputs, [], [], 1.0)   # megvárja, melyik socketen van teendő (max. 1 mp); csak az első lista kell
            for s in readable:        # végigmegyünk azokon a socketeken, ahol van teendő
                if s is server:       # ha a figyelő socketen van teendő...
                    kliens, _ = server.accept()   # ...új kliens csatlakozik: elfogadjuk (a címe nem kell)
                    inputs.append(kliens)         # felvesszük a figyeltek közé
                    continue          # ezzel a socketnek végeztünk, jöhet a következő
                try:                  # egy meglévő kliens küldött valamit
                    adat = recv_exact(s, CMD.size)   # pontosan egy parancsnyi (24) bájt beolvasása
                except ConnectionResetError:         # Windowson a hirtelen bontás ilyen hibát dobhat
                    adat = b""        # ezt is bontásnak vesszük
                if not adat:          # üres adat = a kliens lebontotta a kapcsolatot
                    inputs.remove(s)  # kivesszük a figyeltek közül (különben végtelen ciklus lenne)
                    s.close()         # lezárjuk a socketet
                    continue          # tovább a következő socketre
                nev, w, p, q = CMD.unpack(adat)   # a 24 bájtot négy értékre bontjuk: parancs, raktár, termék, mennyiség
                nev, w, p = (x.rstrip(b"\x00").decode() for x in (nev, w, p))   # a három szöveges mezőből levágjuk a nullákat, és szöveggé alakítjuk
                ertek = 0             # a válasz alapértéke
                if nev == ADD:        # ADD parancs: hozzáadás
                    termekek = raktar.setdefault(w, {})   # az adott raktár termékei; ha még nincs ilyen raktár, üres szótárat hoz létre
                    termekek[p] = termekek.get(p, 0) + q  # a termék darabszáma + q; ha még nincs a termék, 0-ról indul
                    ertek = termekek[p]                   # a válasz: a termék új darabszáma
                elif nev == GET:      # GET parancs: lekérdezés
                    ertek = raktar.get(w, {}).get(p, 0)   # a termék darabszáma; ha nincs raktár vagy termék, 0
                elif nev == TOT:      # TOT parancs: a raktár teljes készlete
                    ertek = sum(raktar.get(w, {}).values())   # a raktár összes termékének összege (nincs raktár: 0)
                s.sendall(REPLY.pack(ertek))   # a választ struct-ba csomagoljuk (nem bytesztring), és elküldjük a kliensnek


if __name__ == "__main__":            # csak akkor fusson, ha közvetlenül indítják
    main()                            # a fő függvény indítása
```

## 3. feladat, minden sor kommentelve

```python
IN = struct.Struct("i 20s")           # a kliens felől: egy egész (kliens típusa) + 20 bájt szöveg (felhasználónév), 24 bájt
OUT = struct.Struct("5s 20s")         # az UDP szerver felé: 5 bájt parancs + 20 bájt felhasználónév, 25 bájt
PARANCS = {0: b"LOGIN", 1: b"GUEST"}  # az átfordítás: a 0-s típusból LOGIN lesz, az 1-esből GUEST


def main():                           # a program fő függvénye
    port, szerver_port = int(sys.argv[1]), int(sys.argv[2])   # parancssorból: a proxy portja, és az UDP szerver portja
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # UDP socket az Azonosítási Szerverrel való beszélgetéshez
    udp.settimeout(3)                 # ha 3 mp-ig nem jön válasz, hibát kapunk, ahelyett hogy örökre lefagynánk
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:   # TCP szerver socket a kliensek felé
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # újraindításnál a port azonnal újra használható
        server.bind(("localhost", port))   # a socketet a saját gép adott portjához kötjük
        server.listen(5)              # figyelni kezd; legfeljebb 5 várakozó kapcsolat
        inputs = [server]             # a figyelt socketek listája; az UDP socket NEM kerül ide, mert a választ rögtön megvárjuk
        while True:                   # a proxy örökké fut
            readable, _, _ = select.select(inputs, [], [], 1.0)   # megvárja, melyik socketen van teendő (max. 1 mp)
            for s in readable:        # végigmegyünk azokon a socketeken, ahol van teendő
                if s is server:       # ha a figyelő socketen van teendő...
                    kliens, _ = server.accept()   # ...új kliens csatlakozik: elfogadjuk
                    inputs.append(kliens)         # felvesszük a figyeltek közé
                    continue          # jöhet a következő socket
                try:                  # egy meglévő kliens küldött valamit
                    adat = recv_exact(s, IN.size)   # pontosan egy üzenetnyi (24) bájt beolvasása
                except ConnectionResetError:        # Windowson a hirtelen bontás ilyen hibát dobhat
                    adat = b""        # ezt is bontásnak vesszük
                if not adat:          # üres adat = a kliens lebontotta a kapcsolatot
                    inputs.remove(s)  # kivesszük a figyeltek közül
                    s.close()         # lezárjuk a socketet
                    continue          # tovább a következő socketre
                tipus, nev = IN.unpack(adat)   # két értékre bontjuk: a kliens típusa (szám) és a név (bájt, nem kell dekódolni)
                udp.sendto(OUT.pack(PARANCS[tipus], nev), ("localhost", szerver_port))   # a típusból parancs lesz, újracsomagoljuk (5s 20s), és UDP-n elküldjük
                valasz, _ = udp.recvfrom(1024)   # megvárjuk az UDP szerver válaszát (bytesztring); a feladó címe nem kell
                s.sendall(valasz)     # a választ VÁLTOZATLANUL továbbadjuk a kliensnek (nem csomagoljuk ki)


if __name__ == "__main__":            # csak akkor fusson, ha közvetlenül indítják
    main()                            # a fő függvény indítása
```
