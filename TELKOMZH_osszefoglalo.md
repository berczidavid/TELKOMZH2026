# Socket ZH – Teljes összefoglaló (Telekommunikáció, 8. óra)

Ez a dokumentum a `ZH 8. ora` mappa **teljes, rekurzív tartalmát** gyűjti össze: minden olvasható szöveges fájlt (`.py`, `.txt`, `README.txt`) és mindkét PDF-et (`Socket_ZH_magyarazat.pdf`, `zhpdf.pdf`) szó szerint vagy hűen összefoglalva. A bináris / nem-informatív fájlokat (`.DS_Store`, `pyarmor_runtime.so`, `__pycache__/*.pyc`, `kep.png`) csak megemlítjük, tartalmukat nem lehet (és nem is érdemes) kiolvasni.

**A cél:** a `zh/` mappa a **valódi ZH-csomag** (Moodle-ről letöltött, zh_A.zip) – ez kapja a legtöbb hangsúlyt. A többi mappa gyakorló/magyarázó anyag ugyanehhez a témához.

---

## Tartalomjegyzék

1. [`zh/` – A VALÓDI ZH CSOMAG (legfontosabb rész)](#1-zh--a-valódi-zh-csomag)
   - 1.1 A ZH szövege (zhpdf.pdf teljes transzkripció)
   - 1.2 feladat1 / feladat2 / feladat3 README.txt fájlok
   - 1.3 valtozat.txt
   - 1.4 tests.py (a tesztfuttató keret)
   - 1.5 tesztek/ mappa (obfuszkált, "fekete doboz")
   - 1.6 Feladat-áttekintő táblázat
2. [`telkom_socket_zh/` – Magyarázó + gyakorló csomag](#2-telkom_socket_zh)
   - 2.1 00_OLVASD_EL.txt
   - 2.2 magyarazat/Socket_ZH_magyarazat.pdf (teljes transzkripció)
   - 2.3 feladatok/ (f1–f5, üres vázak)
   - 2.4 feladatok/megoldasok/ (kész megoldások)
   - 2.5 feladatok/ref_szerverek.py
   - 2.6 peldak/ (p1–p5, kommentelt minták)
   - 2.7 puska_socket.py (a végső "puska")
3. [`zh_A_gyakorlas/` – ZH A gyakorló keret](#3-zh_a_gyakorlas)
   - 3.1 00_OLVASD_EL.txt
   - 3.2 feladat1/2/3 (üres vázak, részleges megoldáskísérlettel)
   - 3.3 megoldasok/ (kész megoldások)
   - 3.4 puska_socket_v2.py
   - 3.5 tests.py (helyi tesztelő keret)
4. [Heti gyakorlati csomagok (röviden)](#4-heti-gyakorlati-csomagok)
   - 4.1 `5_gyakorlat_csomag (1)/`
   - 4.2 `6_gyakorlat_csomag-2/`
   - 4.3 `7_gyakorlat_csomag-2/`
5. [Top-level fájlok](#5-top-level-fájlok)
6. [`ujak/` – korábban kihagyott mappa](#6-ujak--korábban-kihagyott-mappa)
   - 6.1 `ujak/zh/` és `ujak/zhpdf.pdf`
   - 6.2 `ujak/Minta_ZH/` – ZH_1 (beteg/orvos/patika) és ZH_2 (bid/licit/log)
   - 6.3 `ujak/PotZH/` – autókereskedés (1,2,3 és 4 variáns)

---

# 1. `zh/` – A VALÓDI ZH CSOMAG

**Ez a mappa a legfontosabb: ez a ténylegesen kiadott zárthelyi dolgozat (zh_A.zip) tartalma.** A `zhpdf.pdf` a hivatalos feladatlap, a `feladatN/README.txt` fájlok a megoldások helyét írják le, a `tesztek/` mappa pedig a (részben obfuszkált) automatikus ellenőrző rendszer.

## 1.1 A ZH szövege (`zh/zhpdf.pdf` – TELJES transzkripció)

> **Socket ZH**
> Összesen 20 pont (6 + 6 + 8). A 2. és 3. feladatban a program a `localhost` címen figyeljen. A tesztszerverek is a `localhost` címen érhetők el. A csomag: `zh_A.zip`.

### 1. feladat: járatfoglalás (6 pont)

Készítsünk egy TCP klienst! A megoldás helye: `feladat1/client.py`, indítása: `python client.py localhost 20001`

A kliens küldje el az Ön neptun kódját, a járatszámot és az üzenet típusát ("request") egy üzenetben a tesztszervernek, ahol a formátum: `(6s 8s 7s)`
A keresett járatszám: `LH2048`.

A szerver válaszüzenete a szabad helyek száma és az utazási osztály, formátum: `(i 10s)`
Az utazási osztály értékei lehetnek: `"economy"`, `"business"`.

Önnek legalább 3 szabad helyre van szüksége economy osztályon.

Ha a visszakapott osztály nem economy, vagy a szabad helyek száma kisebb mint 3, akkor a kliens válaszüzenete: (neptun kód, járatszám, `"reject"`), formátum: `(6s 8s 7s)`

Ha a feltételek teljesülnek, akkor a kliens válaszüzenete: (neptun kód, járatszám, `"reserve"`), formátum: `(6s 8s 7s)`

A szerver végső válasza ("reject" és "reserve" esetén is) egy foglalási azonosító, formátum: `(12s)`
Ha hiba van a megoldásában, a válaszüzenetben egy-két esetben jelezve van, hogy mi a probléma; a részleteket a tesztszerver naplója mutatja.

**Ellenőrzés.** Töltse le és csomagolja ki a zárthelyi csomagját (zip), a feladatot a kicsomagolt mappájában oldja meg! A Docker Desktopnak futnia kell. A csomag mappájában (ahol a `tests.py` van):

```
python tests.py check t8gNJ6rNm3ST feladat1
```

A következő kód (`t8gNJ6rNm3ST`) ennek a feladatnak a saját kódja: pontosan másolja ki (a kis- és nagybetű számít)! A `check` elindítja a programját, lefuttatja a teszteket, és a végén kiírja a kódokat: ezeket őrizze meg. Kézi mód fejlesztéshez: `python tests.py start t8gNJ6rNm3ST feladat1` (ez az ablak a tesztek naplója), és egy másik ablakban saját programja: `python feladat1/client.py localhost 20001`.

**Fontos:** a `tesztek` mappa obfuszkált kódját "fekete dobozként" kell kezelni, a rá alkalmazott kódvisszafejtés ("reverse engineering") csalásnak minősül.

### 2. feladat: raktárkészlet (6 pont)

Készítsünk egy TCP szervert, amely `select` segítségével egyszerre több kliens kiszolgálására is képes! A megoldás helye: `feladat2/server.py`, indítása: `python server.py <port>`

A szerver különböző raktárak készletadatait tárolja. A kliensek háromféle parancsot küldhetnek a szervernek:

- `ADD W P Q` – adjon hozzá Q darabot a W raktárban a P termékhez
- `GET W P Q` – kérdezze le a W raktárban a P termék aktuális darabszámát (a Q nem releváns, 0-ra van állítva)
- `TOT W P Q` – számítsa ki a W raktár teljes készletét, azaz a benne lévő termékek összdarabszámát (a P, Q nem releváns, P `"AAAAAAAA"`-ra, Q 0-ra van állítva)

A parancsokat a kliensek struct formátumban küldik: `(3s 6s 8s i)`
A szerver minden parancs után egy egész számot ad vissza `(i)`, amely ADD és GET után a termék aktuális darabszáma (az adott raktárban), TOT után a raktár teljes készlete.

**Példa:**
```
"ADD", "WH001", "Laptop", 10   → a szerver hozzáad 10 darab Laptop terméket a WH001 raktárhoz és visszaküldi a 10-et
"GET", "WH001", "Laptop", 0    → a szerver visszaküldi a Laptop aktuális darabszámát, a 10-et
"ADD", "WH001", "Mouse", 5     → a szerver hozzáad 5 darab Mouse terméket és visszaküldi az 5-öt
"TOT", "WH001", "AAAAAAAA", 0  → a szerver visszaküldi a WH001 raktár teljes készletét, a 15-öt
```

A kliens nem fog szándékosan helytelen üzenetet (pl. érvénytelen parancsot stb.) küldeni.

**Ellenőrzés.** Töltse le és csomagolja ki a zárthelyi csomagját (zip), a feladatot a kicsomagolt mappájában oldja meg! A Docker Desktopnak futnia kell. A csomag mappájában (ahol a `tests.py` van):

```
python tests.py check k7m2x9p4qw8r feladat2
```

A következő kód (`k7m2x9p4qw8r`) ennek a feladatnak a saját kódja: pontosan másolja ki (a kis- és nagybetű számít)! A `check` elindítja a programját, lefuttatja a teszteket, és a végén kiírja a kódokat: ezeket őrizze meg. Kézi mód fejlesztéshez: `python tests.py start k7m2x9p4qw8r feladat2` (ez az ablak a tesztek naplója), és egy másik ablakban saját programja, majd egy harmadik ablakban: `python tests.py test feladat2 <port>`.

**Fontos:** a `tesztek` mappa obfuszkált kódját "fekete dobozként" kell kezelni, a rá alkalmazott kódvisszafejtés ("reverse engineering") csalásnak minősül.

### 3. feladat: azonosítási proxy (8 pont)

Készítsünk egy proxy programot, amely kétféle kliens kéréseit kezeli és továbbítja az Azonosítási Szerver felé! A megoldás helye: `feladat3/proxy.py`, indítása: `python proxy.py <port> <szerver_port>`. Az Azonosítási Szervert és a klienseket a tesztprogram futtatja, a szerver az UDP 20002-es porton figyel: `python proxy.py 10002 20002`

- A Felhasználó Kliens bejelentkezési kérelmet küld.
- A Vendég Kliens információlekérési kérelmet küld.
- A Proxy az Azonosítási Szerver válaszát a megfelelő kliensnek küldi vissza.

A kliensek mindig TCP-n kapcsolódnak a Proxyhoz. Mindkét kliens esetén a Proxyhoz menő üzenet formátuma: `kliens_típus, felhasználónév`, formátum: `(i 20s)`. A `kliens_típus` értékei: 0 = Felhasználó Kliens, 1 = Vendég Kliens.

A Proxy `select` segítségével egyszerre több kliens kiszolgálására is képes. A Proxy az Azonosítási Szerver felé más formátumban továbbítja az üzeneteket:

- Felhasználó Kliens esetén: `("LOGIN", felhasználónév)`, formátum: `(5s 20s)`
- Vendég Kliens esetén: `("GUEST", felhasználónév)`, formátum: `(5s 20s)`

A Proxy az Azonosítási Szerverrel UDP-n keresztül kommunikál, és minden kliens kérését ezen keresztül továbbítja. A szerver bytesztring válasza változatlanul visszakerül a megfelelő klienshez.

```
+--------------+    TCP   +----------+    UDP   +--------------+
| Felhasználó  |<-------->|          |<-------->| Azonosítási  |
|   Kliens     |          |  Proxy   |          |   Szerver    |
+--------------+          |          |          +--------------+
                          |          |
+--------------+    TCP   |          |
|   Vendég     |<-------->|          |
|   Kliens     |          +----------+
+--------------+
```

**Ellenőrzés.** Töltse le és csomagolja ki a zárthelyi csomagját (zip), a feladatot a kicsomagolt mappájában oldja meg! A Docker Desktopnak futnia kell. A csomag mappájában (ahol a `tests.py` van):

```
python tests.py check R8mK2vX7pQ4n feladat3
```

A következő kód (`R8mK2vX7pQ4n`) ennek a feladatnak a saját kódja: pontosan másolja ki (a kis- és nagybetű számít)! A `check` elindítja a programját, lefuttatja a teszteket, és a végén kiírja a kódokat: ezeket őrizze meg. Kézi mód fejlesztéshez: `python tests.py start R8mK2vX7pQ4n feladat3` (ez az ablak a tesztek naplója), és egy másik ablakban a saját programja, majd egy harmadik ablakban: `python tests.py test feladat3 <port>`.

**Fontos:** a `tesztek` mappa obfuszkált kódját "fekete dobozként" kell kezelni, a rá alkalmazott kódvisszafejtés ("reverse engineering") csalásnak minősül.

> **Megjegyzés:** a `t8gNJ6rNm3ST`, `k7m2x9p4qw8r`, `R8mK2vX7pQ4n` kódok a MINTA zh_A.zip-hez tartoznak (ez a mintapélda PDF-je); az éles ZH-n saját, a Moodle kérdésben megadott kódot kell használni (lásd `zh/feladat1/2/3/README.txt`, ahol `<KÓD>` szerepel helyette).

## 1.2 `feladat1/README.txt`, `feladat2/README.txt`, `feladat3/README.txt` (teljes szöveg)

**`zh/feladat1/README.txt`:**
```
Ide kerül az 1. feladat megoldása, ezzel a fájlnévvel:

  client.py        indítás: python client.py <host> <port>   (a tesztszerver: localhost 20001)

Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <KÓD> feladat1        (a <KÓD> a feladat Moodle kérdésében szerepel)

A kliens minden adatot parancssori paraméterként kap (sys.argv), input() nélkül.
```

**`zh/feladat2/README.txt`:**
```
Ide kerül a 2. feladat megoldása, ezzel a fájlnévvel:

  server.py        indítás: python server.py <port>

Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <KÓD> feladat2        (a <KÓD> a feladat Moodle kérdésében szerepel)

A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`zh/feladat3/README.txt`:**
```
Ide kerül a 3. feladat megoldása, ezzel a fájlnévvel:

  proxy.py         indítás: python proxy.py <port> <szerver_port>       (az azonosítási szerver: UDP 20002)

Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <KÓD> feladat3        (a <KÓD> a feladat Moodle kérdésében szerepel)

A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

Azaz a megoldásokat **pontosan** ide kell elhelyezni:
- `zh/feladat1/client.py`
- `zh/feladat2/server.py`
- `zh/feladat3/proxy.py`

## 1.3 `zh/tesztek/valtozat.txt`

Tartalma: **`A`**

Ez jelzi, hogy ez a ZH-csomag az **"A" változat**. A `tests.py` ez alapján választja ki a `CHECKS["A"]` vagy `CHECKS["B"]` konfigurációt (lásd lent). A "B" változatban a 3. feladat (proxy) kicsit bővebb: két portot kap (`{port}`, `20002`, `20003`), és a "ready" üzenetei is mások ("feladat3 TCP szerver", "feladat3 UDP szerver" vs. az "A" változat "feladat3 azonosítási szerver" üzenete). Mivel ez a csomag "A" változat, csak egy Azonosítási Szerver van (UDP 20002), ahogy a PDF is írja.

## 1.4 `zh/tests.py` – a tesztfuttató keret (TELJES leírás)

Ez a hivatalos ellenőrző szkript, amelyet a hallgatónak **nem kell módosítania**, csak futtatnia. A fájl teteje egy részletes `__doc__` sztringet tartalmaz, amely a használatot írja le:

```
python tests.py check <KÓD> <feladat>          EGY parancs: elindítja a programját, lefuttat minden
                                              tesztet, és kiírja az összes kódot.

Kézi mód, lépésenkénti fejlesztéshez:
  python tests.py start <KÓD> <feladat>          elindítja a teszteket, és ebben az ablakban mutatja
                                              a tesztszerverek naplóját; Ctrl+C: a tesztek leállnak.
  python tests.py test <feladat> <port>          (egy MÁSIK ablakban) a feladat tesztkliense az Ön
                                              szerverét teszteli
  python tests.py log                            a napló újra megnyitása, ha bezárta (kilépés: Ctrl+C)
  python tests.py stop                           leállítja a teszteket (ha az ablakot Ctrl+C nélkül zárta be)

Feladatok és a programok helye (a tests.py mellett):
  feladat1     feladat1/client.py   (python client.py localhost 20001)
  feladat2     feladat2/server.py   (python server.py <port>)
  feladat3     feladat3/proxy.py    (az indítását lásd a feladat szövegében)
Más fájlnév esetén: python tests.py check <KÓD> <feladat> --server <fájl> --client <fájl>
```

**Technikai működés (a forráskód alapján):**
- A rendszer **Docker**-t használ: egy `python:3.12-slim` image-ből (`IMAGE`) indít egy `telkom-zh` nevű konténert (`CONTAINER`), amely a `tesztek/` mappát (`TESTS_DIR`) csak-olvashatóan (`:ro`) csatolja be `/tesztek` alá, és ott futtatja a (titkosított/obfuszkált) `run.py`-t `servers <feladatok>` paranccsal.
- A tesztszerverek a **20001–20010** (`PORTS`) porttartományban figyelnek a konténerben.
- A `CHECKS` szótár variánsonként (A/B) és feladatonként megadja, melyik fájlt kell elindítani (`client`/`server`), milyen porton, és milyen parancssori argumentumokkal:
  ```python
  CHECKS = {
      "A": {
          "feladat1": {"client": "feladat1/client.py", "port": 20001, "runs": [[]]},
          "feladat2": {"server": "feladat2/server.py"},
          "feladat3": {"server": "feladat3/proxy.py", "server_args": ["{port}", "20002"],
                       "ready": ["feladat3 azonosítási szerver"]},
      },
      "B": {
          "feladat1": {"client": "feladat1/client.py", "port": 20001, "runs": [[]]},
          "feladat2": {"server": "feladat2/server.py"},
          "feladat3": {"server": "feladat3/proxy.py", "server_args": ["{port}", "20002", "20003"],
                       "ready": ["feladat3 TCP szerver", "feladat3 UDP szerver"]},
      },
  }
  ```
- `check(token, task, server_file, client_file)` a teljes folyamatot egy lépésben futtatja: ellenőrzi a 12 karakteres, alfanumerikus tokent (`valid_token`), elindítja a Docker konténert a megfelelő feladat tesztszervereivel (`launch`), megvárja, amíg a napló jelzi, hogy a tesztszerver készen áll (`wait_ready`), majd:
  - ha a feladatnak van `server` kulcsa: elindítja a hallgató szerverét egy szabad porton (`check_server`), figyeli, hogy elindul-e időben (`SERVER_START = 5` mp), majd a konténerben lefuttatja ellene a tesztklienst (`run.py test <task> <port>`), és a naplóból kódokat gyűjt (`RENDBEN, kód: (\w+)` mintára).
  - ha a feladatnak van `client` kulcsa: lefuttatja a hallgató kliensét (`check_client`, timeout `CLIENT_RUN = 10` mp) a megadott host/port ellen, és a tesztszerver naplójából olvassa ki a kódokat (`kód a kvízhez: ([\w-]+)` mintára).
- A `start`/`log`/`test`/`stop` parancsok manuális, lépésenkénti fejlesztést tesznek lehetővé (külön ablakban a napló, külön ablakban a hallgató programja).
- Platformspecifikus trükkök: Apple Silicon Macen `--platform linux/amd64` + Rosetta kell (az obfuszkált pyarmor runtime csak x86-64-en fut); natív Linux Docker Engine-nél `--network host`-ot használ, Docker Desktopnál portmappelést.
- A kódokat a hallgatónak kell beírnia a Moodle kvízbe (`"A kódok a Moodle kvízhez: ..."`).

## 1.5 `zh/tesztek/` mappa – OBFUSZKÁLT, "fekete doboz"

A mappa tartalma:
- `common.py`
- `feladat1.py`
- `feladat2.py`
- `feladat3.py`
- `run.py`
- `valtozat.txt` (lásd fent: `A`)
- `pyarmor_runtime_000000/__init__.py` és `pyarmor_runtime_000000/pyarmor_runtime.so`

Mind az öt `.py` fájl (`common.py`, `feladat1.py`, `feladat2.py`, `feladat3.py`, `run.py`) a **Pyarmor 9.1.9** eszközzel van titkosítva/obfuszkálva. Minden ilyen fájl ténylegesen csak ennyit tartalmaz olvasható forrásként:

```python
# Pyarmor 9.1.9 (trial), 000000, non-profits, 2026-10-30T10:25:08.xxxxxx
from pyarmor_runtime_000000 import __pyarmor__
__pyarmor__(__name__, __file__, b'PY000000\x00...')  # a tényleges logika bájtkódba van zárva
```

Ezek **nem olvashatók / nem visszafejthetők** emberi szemmel – a feladatleírás és a PDF is kifejezetten leszögezi, hogy ennek visszafejtése ("reverse engineering") **csalásnak minősül**. A `pyarmor_runtime.so` egy natív (x86-64) megosztott library, bináris, nem szöveges tartalom.

**Amit a tesztek logikájáról a feladatleírásokból és a `tests.py`-ból tudni lehet (nem a fájlok feltörésével, hanem a dokumentált viselkedésből):**
- `feladat1.py`: a tesztszerver a `zhpdf.pdf`-ben leírt járatfoglalási logikát valósítja meg (5 forgatókönyv, különböző szabad hely / osztály kombinációkkal, ellenőrzi a kliens döntését és a kért formátumokat).
- `feladat2.py`: a tesztkliens a raktárkészlet-parancsokat (ADD/GET/TOT) küldi több "raktár" és "termék" kombinációval, ellenőrzi az állapot megőrzését több kapcsolat között is.
- `feladat3.py`: az Azonosítási Szerver és a tesztkliensek (Felhasználó / Vendég) szimulálása, ellenőrzi a proxy helyes átfordítását és a válasz változatlan továbbítását.
- `common.py`: feltehetően közös segédfüggvények (pl. `recv_exact`, naplózás, eredmény-összegzés) – hasonló szerepű, mint a `zh_A_gyakorlas/tests.py`-ban látható `Jegyzo` osztály és segédfüggvények (amelyek a *saját, nem hivatalos* gyakorló verzióban nyíltan olvashatók, lásd 3.5. pont).
- `run.py`: a konténerben induló belépési pont, ami a `servers <feladatok>` és `test <feladat> <port>` parancsokat értelmezi (ezt hívja a `tests.py` `docker exec`-kel).

## 1.6 Feladat-áttekintő táblázat (zh/)

| # | Feladat | Mit kell írni | Fájl | Pont | Formátumok | Válasz |
|---|---------|---------------|------|------|------------|--------|
| 1 | Járatfoglalás | TCP kliens | `feladat1/client.py` | 6 | kérés `(6s 8s 7s)`, válasz `(i 10s)`, 2. kérés `(6s 8s 7s)` | végső `(12s)` |
| 2 | Raktárkészlet | TCP szerver, `select` | `feladat2/server.py` | 6 | parancs `(3s 6s 8s i)` | `(i)` struct |
| 3 | Azonosítási proxy | TCP→UDP proxy, `select` | `feladat3/proxy.py` | 8 | kliens felől `(i 20s)`, UDP felé `(5s 20s)` | bytesztring (változatlanul továbbítva) |

Indítási parancsok:
```
python client.py localhost 20001
python server.py <port>
python proxy.py <port> <szerver_port>      # pl. python proxy.py 10002 20002
```

---

# 2. `telkom_socket_zh/`

Ez egy **önálló, offline magyarázó + gyakorló csomag**, amely ugyanazt az öt socket-mintát tanítja meg, mint amire a ZH épül (lásd 1. fejezet). Nincs hozzá szükség Dockerre vagy internetre, csak Python 3.8+-ra.

## 2.1 `00_OLVASD_EL.txt` (teljes szöveg)

```
TELKOM 2. ZH (SOCKET): MAGYARAZO + GYAKORLO CSOMAG
===================================================

Kell hozza: Python 3.8 vagy ujabb. Semmi mas (nem kell internet, Docker, telepites).

MAPPAK
  magyarazat/                 Socket_ZH_magyarazat.pdf  (ezzel kezdd)
  peldak/                     p1..p5: futtathato, kommentelt peldak (megnezed, lefuttatod)
  feladatok/                  f1..f5: ures vazak + onellenorzo teszt (te irod meg)
  feladatok/megoldasok/       a kesz megoldasok (csak ha tenyleg elakadtal)

HOGYAN FUTTASD
  Mac / Linux:   python3 peldak/p1_tcp_kliens.py
  Windows:       python peldak\p1_tcp_kliens.py      (vagy: py peldak\p1_tcp_kliens.py)

  A feladatokat a feladatok mappabol futtasd:
  cd feladatok
  python3 f1_kliens.py
  Amig nincs kesz: "F1: meg nincs megirva". Ha jo: "F1: minden teszt OK".
  Ha rossz, a teszt megmondja, mit kapott es mit kellett volna.

AJANLOTT SORREND
  p1 -> f1 | p3 -> f2 | p2 -> f3 | p4 -> f4 | p5 -> f5

FONTOS
  A ZH-n AI-t nem lehet hasznalni. Hogy AI-val keszult segedletet be szabad-e vinni,
  azt kerdezd meg a gyakvezetot. A biztos ut: a segedletedet a SAJAT, kezzel megirt
  megoldasaidbol allitsd ossze.
```

## 2.2 `magyarazat/Socket_ZH_magyarazat.pdf` (TELJES transzkripció)

> Ez a fájl **tartalmilag megegyezik** a mappa tetején (top-level) elhelyezett `Socket_ZH_magyarazat.pdf`-fel – ugyanaz a 11 oldalas dokumentum, két helyen tárolva.

### Telkom 2. ZH: Socket — Magyarázó + offline gyakorló csomag

*Python, TCP, UDP, struct, select, proxy*

**Röviden:** a ZH egy kis számú, sablonos feladat. Nem kitalálni kell, hanem öt mintát gépiesen, hibamentesen megírni. Ez a csomag mind az öt mintát külön futtatható példán mutatja meg, utána te írod meg újra őket üres vázból, a gép pedig ellenőrzi.

**Mi van a csomagban:**

| Mappa | Tartalom | Mire jó |
|---|---|---|
| `magyarazat/` | ez a PDF | megérteni a lényeget, utánanézni, ha elakadsz |
| `peldak/` | p1 ... p5 (futtatható, kommentelt) | megnézed, lefuttatod, megérted |
| `feladatok/` | f1 ... f5 (üres vázak + önellenőrző teszt) | te írod meg, a teszt azonnal szól, ha jó |
| `feladatok/megoldasok/` | kész megoldások | csak akkor nézd, ha tényleg elakadtál |

**Javasolt menet (pomodoro blokkok, kb. 25 perc + 5 perc szünet):**

| Blokk | Mit csinálsz | Fájl |
|---|---|---|
| 1 | PDF 1-3. fejezet: alapok, struct, recv_exact | futtasd: p1 |
| 2 | PDF 4. fejezet, majd írd meg magadtól az 1. feladatot | f1 |
| 3 | PDF 5. fejezet (select), majd a select-es szerver | p3, f2 |
| 4 | PDF 6/a és 6/b: UDP szerver, ellenőrző kliens | p2, p4, f3, f4 |
| 5 | PDF 6/c: proxy | p5, f5 |
| 6 | Saját segédlet összeállítása a saját megoldásaidból (9. fejezet), hibaüzenet-kereső átfutása | - |

**TIPP** Ha csak 1 órád van: 1-3. fejezet, p1 és p3, majd f1 és f2. A 3. feladat ezekre épül (a proxy egy select-es szerver + egy UDP kliens kombinációja), ezért ez az alap.

**FONTOS** A ZH nyílt könyves, de az AI használata tilos. Az, hogy AI-val készült segédletet be szabad-e vinni, **nincs benne a feltöltött anyagban**: kérdezd meg a gyakvezetőt. A biztos út, hogy a segédletedet a saját, kézzel megírt megoldásaidból állítod össze (lásd 9. fejezet). Ez tanulásnak is jobb. Ezt a csomagot tanuláshoz használd.

#### 0. A ZH egy oldalon

Forrás: a Moodle-ről mentett Minta ZH (Socket). A ZH-n a konkrét feladatok ennek változatai lehetnek, ezért ne a számokat és parancsneveket magold, hanem a mintákat.

| Feladat | Mit kell írni | Formátumok | Példa | Nehézség |
|---|---|---|---|---|
| 1. TCP kliens | kliens; a szerver adott. a) input, b) txt, c) json, d) UDP | `20s i` küld, `Xs` kap | p1 | könnyű |
| 2. select szerver | TCP szerver több kliensel; IN / INCR / DECR | `4s i` kap, bytesztringet küld | p3 | **a legnehezebb alap** |
| 3/a UDP szerver | PUSH / PLUS / MINUS | `5s i` kap, `i` küld | p2 | könnyű-közepes |
| 3/b ellenőrző kliens | TCP és UDP értéket összehasonlít | mindkettő | p4 | könnyű |
| 3/c proxy | TCP szerver, ami UDP szerverhez továbbít | `4s i` → `5s i` → `i` | p5 | közepes-nehéz |

**Mi nincs az anyagban (kérdezz rá):**
- a pontozás és az időkeret (nincs a Moodle-oldalon),
- a ZH konkrét paraméterei (parancsnevek, formátumok, portok változhatnak),
- hogyan éred el a ZH-s tesztkörnyezetet (melyik porton, melyik címen hívja a szerveredet).

A félév áttekintésed szerint a gyakorlati ZH-knál mindegyikből legalább 50% kell, a célszint 3-4-es (Félév áttekintés, TKH szakasz).

**A ZH első 3 perce: ezt írd ki magadnak minden feladatnál**
- Ki a szerver, ki a kliens? Melyiket kell megírni, melyik adott?
- TCP vagy UDP? (ettől függ: connect/accept vagy sendto/recvfrom)
- Mit küld a kliens? Struct formátum, és hány bájt (`Struct(...).size`).
- Mit kap vissza? Bytesztring (`b"24"`) vagy struct (melyik formátum)?
- Kell-e select? (több kliens egyszerre)

Először mindig a legkisebb működő változatot (egy kliens, egy parancs) írd meg, és futtasd. Utána jöhet a többi.

#### 1. Alapok: mit csinál egy socket?

- A **socket** a programod "csatlakozója" a hálózathoz. A címe két dolog: **(host, port)**.
- **host**: melyik gép. Gyakorláskor `"localhost"` (a saját géped).
- **port**: egy szám (pl. 10000). Egy gépen belül ez dönti el, melyik program kapja az adatot.
- Két fajta socket van, ezt a ZH mindkettővel használja: **TCP** és **UDP**.

| | TCP (SOCK_STREAM) | UDP (SOCK_DGRAM) |
|---|---|---|
| kapcsolat | van: connect / accept | nincs |
| adat | bájtfolyam, nincs üzenethatár | különálló datagramok: egy `recvfrom` = egy teljes üzenet |
| megbízhatóság | sorrend és teljesség garantált | elveszhet, felcserélődhet (localhoston ritka) |
| szerver hívásai | bind, listen, accept, recv, sendall | bind, recvfrom, sendto |
| kliens hívásai | create_connection, sendall, recv | sendto, recvfrom |

TCP folyamat: `socket·bind·listen` → `connect()/accept()` → `sendall(struct csomag)` → `recv_exact(Struct.size)` → `sendall(válasz)` → `recv_exact/recv`.

UDP folyamat: `socket(SOCK_DGRAM)·bind` → `sendto(adat,(host,port))` → `recvfrom()` ad adat+kliens címet → `sendto(válasz, kliens_címe)` → `recvfrom()`.

Legkisebb példa (órai demó: `blocking_client.py`):
```python
import socket
with socket.create_connection(("localhost", 10000)) as sock:   # connect
    sock.sendall(b"Hello server")                               # küldés: BÁJTOK, nem str
    print(sock.recv(1024))                                      # a válasz bájtokban jön
```

**TIPP** A `sendall` és `recv` mindig bájtokat (bytes) kezel. Szöveget a `.encode()` alakít bájtokká, a `.decode()` vissza.

#### 2. struct: bájtok összeállítása és kibontása

A hálózaton bájtok mennek, nem számok vagy szövegek. A `struct` modul adott formátum szerint bájtokká csomagol (**pack**), majd visszabontja őket (**unpack**). A kliens és a szerver ugyanazt a formátumot használja, így értik egymást.

| Jel | Jelentése | Mérete |
|---|---|---|
| `s` | bájtsor fix hosszal: `20s` = pontosan 20 bájt | a szám szerint |
| `i` | egész szám (int) | 4 bájt |
| `c` | egyetlen bájt | 1 bájt |

```python
import struct
REQ = struct.Struct("20s i")             # 20 bájt szöveg + 4 bájt szám
csomag = REQ.pack(b"almafa", 4)          # a szöveg bájt kell: "almafa".encode() vagy b"almafa"
print(len(csomag), csomag[:10])          # 24  b'almafa\x00\x00\x00\x00' <- nullákkal kipótolta
szoveg, n = REQ.unpack(csomag)           # unpack mindig TUPLE-t ad vissza
print(szoveg, n)                         # b'almafa\x00\x00 ...' (összesen 20 bájt)  4
print(szoveg.rstrip(b"\x00").decode())   # almafa  <- nullák levágása + vissza szöveggé
```

**A négy dolog, amit minden alkalommal meg kell csinálnod:**
- Küldés előtt: szöveg → bájt: `szoveg.encode()`.
- Fogadás után: `s` mező → `.rstrip(b"\x00").decode()` (a kipótolt nullák miatt).
- Az unpack tuple-t ad: `(x,) = Struct('i').unpack(adat)` vagy `...unpack(adat)[0]`.
- Dinamikus formátum: ha a hossz változik, `f"{n}s"` (pl. `"4s"`, `"3s"`).

**CSAPDA** A méret nem az, aminek gondolod. `struct.Struct("5s i").size` = **12**, nem 9: az 5 bájt szöveg után 3 kitöltő bájt kerül, hogy az `i` 4-gyel osztható helyen kezdődjön. Ezért soha ne írd be kézzel a számot, mindig `Struct.size`. Ráadásul ha elé írsz egy `!`, `<` vagy `>` jelet, a méret megváltozik (`"!5s i"` = 9 bájt), és a szerver nem értené. A ZH-n pontosan azt a formátumot írd, amit a feladat ad.

| Formátum | Méret | Miért |
|---|---|---|
| `"20s i"` | 24 | 20 + 4 (a 20 osztható 4-gyel, nincs kitöltés) |
| `"4s i"` | 8 | 4 + 4 |
| `"5s i"` | 12 | 5 + 3 kitöltés + 4 |
| `"10s i"` | 16 | 10 + 2 kitöltés + 4 (órai tcp_proxy.py) |
| `"i i c"` | 9 | 4 + 4 + 1 (órai select_server.py) |

#### 3. recv_exact: miért nem elég a recv?

A TCP bájtfolyam: nincs benne üzenethatár. Ha a kliens két darab 8 bájtos csomagot küld, a szerver `recv(8)` hívása kaphat 8 bájtot, de 5-öt vagy 16-ot is. A megoldás: addig olvasunk, amíg a **pontos** méret meg nem jön:

```python
def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:          # üres = a másik oldal bontott
            return b""
        data += chunk
    return data
```

| Mit olvasol | Mit használj |
|---|---|
| fix méretű struct (pl. 8 vagy 12 bájt) | `recv_exact(sock, CMD.size)` |
| rövid sima bytesztring válasz (pl. `b"24"`) | `sock.recv(1024)` elég, mert kérdés-válasz sorban megy |
| UDP-n bármi | `recvfrom(1024)`: egy hívás = egy teljes datagram, nem kell recv_exact |

**TIPP** A `recv_exact`-et írd be a segédletedbe készen. Ez az a 8 sor, amit a ZH-n a legjobb nem újra kitalálni.

#### 4. feladat: TCP kliens (p1_tcp_kliens.py)

Adott: a szerver. Neked: a kliens. A kliens egy (szöveg, szám) párt küld `20s i` formátumban, a szerver pontosan *szám* bájtos választ ad (formátuma: `Xs`).

```python
def tcp_kliens(text, n):
    with socket.create_connection(("localhost", PORT)) as sock:   # 1) kapcsolódás
        sock.sendall(REQ.pack(text.encode(), n))                  # 2) csomagolás + küldés
        valasz = recv_exact(sock, n)                               # 3) pontosan n bájt jön vissza
    (szoveg,) = struct.unpack(f"{n}s", valasz)                     # 4) kicsomagolás: "4s", "3s"...
    return szoveg.rstrip(b"\x00").decode()                         # 5) nullák le, vissza szöveggé
```

**CSAPDA** A feladat szövege szerint a szerver "levág a szöveg elejéről X karaktert", de a példák (almafa,4 -> amla, kortefa,3 -> rok) azt mutatják: az **első X karaktert** tartja meg, és **megfordítja**. A szerver adott, ezt neked nem kell megírni, csak azt tudd, hogy a válasz hossza pontosan X.

A négy változat: csak a bemenet forrása különbözik:

| Változat | Bemenet | Mire figyelj |
|---|---|---|
| a) | `input()` + `random.randint(1, len(text))` | a feladat nem ad tartományt; a `len(text)` a biztonságos |
| b) | `input.txt`: soronként `szó szám` | `.read().splitlines()`, `randint(1,3)` (mindkét vége benne van), `sorok[i-1].split()`, a szám `int(...)`! |
| c) | `input.json`: `{"1": ["almafa", 4], ...}` | a kulcs szöveg: `str(random.randint(1,3))`, `json.load(f)` |
| d) | UDP kliens | `SOCK_DGRAM`, `sendto`/`recvfrom(1024)`, nincs connect, nincs recv_exact; `settimeout(2)` |

**Tipikus hibák:** elfelejtett `.encode()`; a válaszban ott maradnak a `\x00` bájtok (nincs rstrip); a fájlból olvasott szám szöveg marad (nincs `int()`); a fájl útvonala rossz (a program abból a mappából keresi, ahonnan indítod); UDP-nél `recv_exact`-et használsz (UDP-n nincs ilyen, `recvfrom` kell).

#### 5. feladat: TCP szerver select-tel (p3_select_tcp_szerver.py)

Feladat: a szerver egy egész számot tárol (kezdetben 0). Parancsok `4s i` formátumban: `IN x` (beállít), `INCR x` (növel), `DECR x` (csökkent). Minden parancs után az új értéket **sima bytesztringként** küldi vissza. Példa: `IN 20 → b"20"`, `INCR 4 → b"24"`, `DECR 5 → b"19"`.

**Miért kell a select?** Az órai blokkoló szerver (`blocking_server.py`) egyszerre egy klienst szolgál ki: accept → recv → válasz → következő. Ha három kliens egyszerre jön, a többi sorban áll. A `select` azt mondja meg: "melyik socketen van most teendő?" Így egy szál egyszerre sok klienst kezel.

```python
ertek = 0                                            # KÖZÖS állapot, a ciklus ELŐTT
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", PORT)); server.listen(5)
    inputs = [server]                                 # a figyelt socketek listája
    while True:
        readable, _, _ = select.select(inputs, [], [], 1.0)
        for s in readable:
            if s is server:                            # 1) új kliens
                kliens, cim = server.accept()
                inputs.append(kliens)
                continue
            try:                                        # 2) meglévő kliens
                data = recv_exact(s, CMD.size)
            except ConnectionResetError:                # Windowson előfordulhat bontáskor
                data = b""
            if not data:                                 # üres = a kliens bontott
                inputs.remove(s); s.close()
                continue
            nev, x = CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()           # b"IN\x00\x00" -> "IN"
            if nev == "IN": ertek = x
            elif nev == "INCR": ertek += x
            elif nev == "DECR": ertek -= x
            s.sendall(str(ertek).encode())               # bytesztring: b"24"
```

**Soronként, mit miért:**
- `inputs = [server]`: amit a select figyel. A figyelő socket mindig benne van, az új kliensek bekerülnek.
- `select(inputs, [], [], 1.0)`: a *readable* azokat adja vissza, amelyeken van olvasnivaló. Az 1.0 timeout miatt a ciklus nem ragad be örökre.
- `s is server`: a figyelő socketen "olvasnivaló" = új kapcsolat érkezett, ezért accept.
- üres adat (`b""`) = a kliens bontott: ki kell venni a listából és be kell zárni.
- az érték a cikluson **kívül** él, így minden kliens ugyanazt látja.

**Tipikus hibák:** `inputs.remove(s)` elfelejtése (a bontott socket örökre "olvasható" marad, a szerver végtelen ciklusban pörög); `ertek = 0` a ciklusban (minden üzenetnél nullázódik); a parancsnévnek nincs rstrip; `sendall(str(ertek))` (encode hiányzik); a figyelő socketen recv-et hívsz accept helyett.

#### 6. feladat: UDP szerver, ellenőrző kliens, proxy

**6/a UDP szerver (p2_udp_szerver.py)** — ugyanaz az ötlet, mint a select-es szervernél (egy tárolt szám), de más parancsnevekkel (PUSH, PLUS, MINUS), `5s i` kéréssel, és a válasz itt **struct (i)**, nem bytesztring.

```python
CMD = struct.Struct("5s i")        # 12 bájt! (5 + 3 kitöltés + 4)
REPLY = struct.Struct("i")
ertek = 0                          # a ciklus előtt
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(("localhost", PORT))                 # nincs listen, nincs accept
    while True:
        data, kliens = sock.recvfrom(1024)          # a kliens címe is jön
        nev, x = CMD.unpack(data)
        nev = nev.rstrip(b"\x00").decode()
        if nev == "PUSH": ertek = x
        elif nev == "PLUS": ertek += x
        elif nev == "MINUS": ertek -= x
        sock.sendto(REPLY.pack(ertek), kliens)       # struct válasz, a kliens címére
```

**CSAPDA** UDP-nél a válasz a feladó címére megy (`kliens`), nem egy korábban megnyitott kapcsolatra. A választ `REPLY.pack(ertek)`-vel kell csomagolni, nem `str(ertek).encode()`-dal.

**6/b Ellenőrző kliens (p4_ellenorzo_kliens.py)** — az UDP szerver néha hibázik: minden parancsnál a kapott számhoz hozzáad -1, 0 vagy 1 értéket. Az ellenőrző kliens mindkét szervertől lekérdezi az értéket, és összehasonlítja őket. "0-val való növelés" = lekérdezés: `INCR 0` a TCP szervernek, `PLUS 0` az UDP szervernek.

```python
def tcp_ertek():
    with socket.create_connection(("localhost", TCP_PORT)) as sock:
        sock.sendall(TCP_CMD.pack(b"INCR", 0))
        return int(sock.recv(1024))                 # b"19" -> 19

def udp_ertek():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(UDP_CMD.pack(b"PLUS", 0), ("localhost", UDP_PORT))
        data, _ = sock.recvfrom(1024)
    return REPLY.unpack(data)[0]                    # tuple! kell a [0]

hibazott = tcp_ertek() != udp_ertek()
```

**6/c Proxy (p5_tcp_proxy.py)** — a TCP szerver most nem tárol értéket: a kliensek parancsait átfordítja, továbbítja az UDP szervernek, és az UDP szerver válaszát küldi vissza a kliensnek.

```
Kliens --TCP (4s i) INCR 4--> Proxy --unpack, INCR->PLUS (szótár)--> UDP (5s i) PLUS 4 --> UDP szerver (érték += 4)
Kliens <--TCP b"24"-- Proxy <--unpack, str(24).encode()-- UDP (i) 24 <-- UDP szerver
```

```python
FORDITAS = {"IN": "PUSH", "INCR": "PLUS", "DECR": "MINUS"}   # a feladat magja
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # EGY UDP socket, ciklus előtt
udp.settimeout(2)
# ... select-es TCP szerver, mint a P3-ban; a kliens üzenetének feldolgozása:
nev, x = TCP_CMD.unpack(data)                                  # 1) kliens formátuma (4s i)
udp_nev = FORDITAS.get(nev.rstrip(b"\x00").decode())            # 2) átfordítás
udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), UDP_ADDR)         # 3) UDP formátum (5s i)
valasz, _ = udp.recvfrom(1024)                                  # 4) válasz megvárása
(ertek,) = REPLY.unpack(valasz)                                 # 5) kicsomagolás (i)
s.sendall(str(ertek).encode())                                  # 6) a kliensnek bytesztring
```

**Tipikus hibák:** három különböző formátum (4s i kliens felől, 5s i UDP felé, i UDP válasz – bytesztring csak a kliens felé megy); az UDP socketet nem kell a select listába tenni; az UDP socket a ciklus előtt jön létre, nem minden üzenetnél újra; `.get()` hiányában KeyError ismeretlen parancsnál; `settimeout` nélkül a proxy örökre lefagyhat.

#### 7. Hibaüzenet-kereső

| Mit látsz | Valószínű ok | Teendő |
|---|---|---|
| `struct.error: unpack requires a buffer of 12 bytes` | rossz méretet olvastál vagy kézzel írtad be | mindig `Struct.size`; TCP-n `recv_exact`; kitöltés miatt `5s i` = 12 |
| `struct.error: argument for 's' must be a bytes object` | str-t adtál a pack-nek | `.encode()` |
| `TypeError: a bytes-like object is required, not 'str'` | str-t küldtél a sendall-nak | `.encode()`, pl. `str(ertek).encode()` |
| `ConnectionRefusedError` / WinError 10061 | nem fut a szerver, rossz port, vagy még nem indult el | indítsd előbb a szervert; ellenőrizd a portot |
| `OSError: Address already in use` (Linux 98, Mac 48, Win 10048) | a port még foglalt (régi futás) | `SO_REUSEADDR`; zárd be a régi folyamatot |
| a program megáll, nem történik semmi | a recv választ vár, ami nem jön | rossz méret? rossz formátum? UDP-nél `settimeout` |
| `socket.timeout` | nem jött válasz időben | futott a szerver? jó porton? megkapta a kérést? |
| `ConnectionResetError` / WinError 10054 | a másik oldal hirtelen bontott | `try/except ConnectionResetError`, kezeld bontásként |
| a válasz tele van `\x00` bájtokkal | kipótolt s mező | `.rstrip(b"\x00")` |
| `UnicodeDecodeError` | olyan bájtokat dekódolsz, amik nem szöveg | csak az s mezőt `.decode()`-old |
| a szerver 100%-on pörög, "bontott kliens"-t ír | a bontott socket benne maradt az inputs-ban | `inputs.remove(s) + s.close()` |
| `KeyError: 'XYZ'` | ismeretlen parancs a szótárban | `FORDITAS.get(nev)` + ERR válasz |
| az érték minden kérésnél újra 0 | az állapotváltozót a ciklusban hoztad létre | a ciklus elé tedd |

#### 8. Macen gyakorolsz, Windowson írod a ZH-t

| Téma | Mac | Windows (ZH) |
|---|---|---|
| Python indítása | `python3 fajl.py` | `python fajl.py` vagy `py fajl.py` |
| Ctrl+C megszakítja a blokkoló hívást | igen | az accept-et/recv-et nem mindig szakítja meg: ezért `settimeout(1.0)`; a select ciklus 1.0 timeout-ja ugyanezt oldja meg |
| Bontó kliens | üres adat (`b""`) | néha `ConnectionResetError`: fogd el, kezeld bontásként |
| `SO_REUSEADDR` | újraindításkor feloldja a foglalt portot | másképp működik: két szerver is bindolhat ugyanarra a portra. Furcsa válaszoknál nézd meg, nem fut-e még egy régi python.exe |
| Sorvég a fájlokban | `\n` | `\r\n`: használj `.splitlines()` vagy `.strip()`-et, ne `.split("\n")`-t |
| Fájl megnyitása | `open(fajl, encoding="utf-8")` | ugyanez; az útvonal a futtatás mappájához (cwd) képest értendő |
| Tűzfal | - | első indításkor rákérdezhet: Engedélyezés. Localhoston általában nem kell |
| Ékezetes print | rendben | a konzol néha gondot okoz: tartsd ékezetmentesen |

**TIPP** A kódod két ponton ugyanúgy működik mindkét rendszeren, ha betartod: nem írsz be kézzel méreteket (`Struct.size`), a fájlokat `encoding="utf-8"`-tel nyitod meg, és a szerverciklusban mindig van timeout.

#### 9. A saját segédleted: mi kerüljön bele?

Ajánlott felépítés (1-2 oldal):
- **struct kisokos**: formátumjelek, méretek táblázata, a kitöltés-csapda (`"5s i"` = 12), encode / rstrip / decode.
- **recv_exact**: a 8 soros függvény készen.
- **5 sablon**, mindegyik a saját megoldásodból: TCP kliens, UDP kliens, select-es TCP szerver, UDP szerver, proxy.
- **A ZH-s ellenőrzőlista** (0. fejezet, első 3 perc): ki a szerver, TCP/UDP, formátumok, válasz típusa.
- **Hibaüzenet-kereső**: a 7. fejezet leglényegesebb 5 sora.

**FONTOS** Az AI-val készült segédlet engedélyezése nincs az anyagban: kérdezd meg a gyakvezetőt. A biztonságos megoldás, hogy az F1-F5 feladatokat te magad írod meg, és ezekből a saját kódjaidból állítod össze a segédletet: ez a legjobb tanulás is.

#### 10. Önellenőrző kérdések

1. **Mekkora a `struct.Struct("5s i").size`?** Válasz: 12 (5 + 3 kitöltő bájt + 4).
2. **Mi a baj ezzel: `sock.sendall("IN")`?** Válasz: str-t küldesz, bájt kell. `.encode()` vagy `b"IN"`.
3. **Miért kell TCP-nél recv_exact?** Válasz: a TCP bájtfolyam, nincs üzenethatár: `recv(n)` kevesebbet is adhat n-nél.
4. **Mely hívásokat NEM használod UDP-nél a TCP-hez képest?** Válasz: `listen`, `accept`, `connect` (és a `recv_exact`-et).
5. **A select visszaadja a figyelő (server) socketet. Mit jelent ez?** Válasz: új kliens akar csatlakozni, `accept` jön, bekerül az `inputs` listába.
6. **Mit jelent, ha recv_exact üres bájtsort ad vissza?** Válasz: a kliens bontott: `inputs.remove(s)` és `s.close()`.
7. **Mit ad a `struct.unpack("4s", b"amla")`?** Válasz: `(b'amla',)`, egy tuple.
8. **A proxynál miért nem kell az UDP socketet a select listába tenni?** Válasz: a választ rögtön a kérés után megvárjuk (`recvfrom`).
9. **Mi megy a TCP kliensnek a select-es szerverből (IN 20 után), és mi az UDP kliensnek (PUSH 20 után)?** Válasz: TCP: bytesztring `b"20"`. UDP: struct `i` (4 bájt).

## 2.3 `feladatok/` – üres vázak + önellenőrző teszt (f1–f5, TELJES kód)

Minden `fN_*.py` fájl **futtatható önmagában** (`if __name__ == "__main__":` lefuttatja a saját önellenőrző tesztjét), és a megoldandó rész a `# TODO: ide írd a megoldást` komment alatt van. A letöltött fájlokban a feladatok **már meg vannak oldva** (ez a felhasználó saját gyakorlás közben kitöltött változata, nem üres váz többé).

### `feladatok/f1_kliens.py` – F1: TCP / UDP KLIENS (ZH 1. feladatához)

```python
r"""
F1: TCP / UDP KLIENS                              (gyakorlás a ZH 1. feladatához)

A szervert megkapod (ref_szerverek.py), TE a klienst írod meg.

A szerver:
  - kérés:  "16s i" formátum: szöveg (16 bájt) + egész szám n
  - válasz: a szöveg UTOLSÓ n karaktere NAGYBETŰSEN, "<n>s" formátumban
  - példa:  ("almafa", 3) -> "AFA"

Írd meg:
  1) kuld_tcp(szoveg, n, port)      -> str   TCP kliens
  2) kuld_fajlbol(fajl, sor, port)  -> str   a fájl sorai "szó;szám" alakúak (pl. "korte;2"),
                                             a sor 1-től számozva; a kiválasztott sort küldd el
                                             a TCP szervernek, és add vissza a választ
  3) kuld_udp(szoveg, n, port)      -> str   ugyanaz, mint az 1), de UDP-vel
"""
import random
import socket
import struct

REQ = struct.Struct("16s i")


def recv_exact(sock, size):  # kész, másold be a saját segédletedbe is
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def kuld_tcp(szoveg, n, port):
    with socket.create_connection(("localhost", port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))
        valasz = recv_exact(sock, n)
    return struct.unpack(f"{n}s", valasz)[0].rstrip(b"\x00").decode()


def kuld_fajlbol(fajl, sor, port):
    with open(fajl, encoding="utf-8") as f:
        sorok = f.read().splitlines()
    szoveg, szam = sorok[sor-1].split(";")
    return kuld_tcp(szoveg, int(szam), port)


def kuld_udp(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), ("localhost", port))
        adat, _ = sock.recvfrom(1024)
    return struct.unpack(f"{n}s", adat)[0].rstrip(b"\x00").decode()


# ---- Ellenőrzés (ezt ne módosítsd) ----
if __name__ == "__main__":
    import os, tempfile
    from ref_szerverek import egyezik, f1_tcp_szerver, f1_udp_szerver, futtat, inditas_tcp, inditas_udp

    TCP_PORT, UDP_PORT = 12001, 12002

    def teszt():
        inditas_tcp(f1_tcp_szerver, TCP_PORT, port=TCP_PORT)
        inditas_udp(f1_udp_szerver, UDP_PORT)
        egyezik("kuld_tcp('almafa', 3)", kuld_tcp("almafa", 3, TCP_PORT), "AFA")
        egyezik("kuld_tcp('korte', 5)", kuld_tcp("korte", 5, TCP_PORT), "KORTE")
        fajl = os.path.join(tempfile.gettempdir(), "f1_input.txt")
        with open(fajl, "w", encoding="utf-8") as f:
            f.write("korte;2\nbarack;4\nszilva;3\n")
        egyezik("kuld_fajlbol(2. sor)", kuld_fajlbol(fajl, 2, TCP_PORT), "RACK")
        egyezik("kuld_fajlbol(3. sor)", kuld_fajlbol(fajl, 3, TCP_PORT), "LVA")
        egyezik("kuld_udp('almafa', 3)", kuld_udp("almafa", 3, UDP_PORT), "AFA")

    futtat("F1", teszt)
```

### `feladatok/f2_select_szerver.py` – F2: TCP SZERVER select-tel (ZH 2. feladatához)

```python
r"""
F2: TCP SZERVER select-tel                        (gyakorlás a ZH 2. feladatához)

  - A szerver egy egész számot tárol (kezdetben 0), ezen osztozik minden kliens.
  - A parancsok "5s i" formátumban jönnek: SET x / ADD x / MUL x
  - Minden parancs után a szerver visszaküldi az új értéket SIMA BYTESZTRINGKÉNT (b"45").
  - Ismeretlen parancsra b"ERR" a válasz, és az érték NEM változik.
  - Ha egy kliens lebontja a kapcsolatot, a szerver menjen tovább.
"""
import select
import socket
import struct

CMD = struct.Struct("5s i")


def recv_exact(sock, size):
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


# ---- Ellenőrzés (ezt ne módosítsd) ----
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
        a.close(); b.close()
        with socket.create_connection(("localhost", PORT), timeout=3) as c:
            egyezik("új kapcsolat, az érték megmaradt", kuld(c, "ADD", 0), b"46")

    futtat("F2", teszt)
```

### `feladatok/f3_udp_szerver.py` – F3: UDP SZERVER (ZH 3/a feladatához)

```python
r"""
F3: UDP SZERVER                                   (gyakorlás a ZH 3. feladat a) részéhez)

  - A parancsok "6s i" formátumban jönnek: SETVAL x / ADD x / SUB x / DOUBLE
  - A válasz: az új érték STRUCT-ban, "i" formátumban (NEM bytesztring!).
  - Ismeretlen parancsra az érték nem változik, de a jelenlegi értéket visszaküldöd.
"""
import socket
import struct

CMD = struct.Struct("6s i")
REPLY = struct.Struct("i")


def udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("localhost", port))
        while True:
            data, kliens = sock.recvfrom(1024)
            if len(data) != CMD.size:
                continue
            nev, x = CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()
            if nev == "SETVAL":
                ertek = x
            elif nev == "ADD":
                ertek += x
            elif nev == "SUB":
                ertek -= x
            elif nev == "DOUBLE":
                ertek *= 2
            sock.sendto(REPLY.pack(ertek), kliens)


# ---- Ellenőrzés (ezt ne módosítsd) ----
if __name__ == "__main__":
    from ref_szerverek import egyezik, futtat, inditas_udp

    PORT = 12004

    def kuld(sock, nev, x):
        sock.sendto(CMD.pack(nev.encode(), x), ("localhost", PORT))
        adat, _ = sock.recvfrom(1024)
        return REPLY.unpack(adat)[0]

    def teszt():
        inditas_udp(udp_szerver, PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as a, \
             socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as b:
            a.settimeout(2); b.settimeout(2)
            egyezik("SETVAL 7", kuld(a, "SETVAL", 7), 7)
            egyezik("ADD 5", kuld(a, "ADD", 5), 12)
            egyezik("SUB 2", kuld(a, "SUB", 2), 10)
            egyezik("DOUBLE", kuld(a, "DOUBLE", 0), 20)
            egyezik("másik kliens: ADD 1", kuld(b, "ADD", 1), 21)
            egyezik("ismeretlen parancs", kuld(b, "FOO", 5), 21)

    futtat("F3", teszt)
```

### `feladatok/f4_ellenorzo.py` – F4: ELLENŐRZŐ KLIENS (ZH 3/b feladatához)

```python
r"""
F4: ELLENŐRZŐ KLIENS                              (gyakorlás a ZH 3. feladat b) részéhez)

Adott két szerver (ref_szerverek.py):
  - TCP szerver: IN / INCR / DECR, "4s i" formátum, a válasz bytesztring (b"19")
  - UDP szerver: PUSH / PLUS / MINUS, "5s i" formátum, a válasz "i" (struct). Néha hibázik.

Írd meg:  ellenorzo(tcp_port, udp_port, kerdesek) -> int
  Ismételd meg a kerdesek-szer: kérdezd le mindkét szervertől az értéket
  (TCP: "INCR 0", UDP: "PLUS 0"), hasonlítsd össze. Térj vissza az eltérések számával.
"""
import socket
import struct

TCP_CMD = struct.Struct("4s i")
UDP_CMD = struct.Struct("5s i")
REPLY = struct.Struct("i")


def ellenorzo(tcp_port, udp_port, kerdesek):
    ertek = 0
    for _ in range(kerdesek):
        with socket.create_connection(("localhost", tcp_port)) as tcp:
            tcp.sendall(TCP_CMD.pack(b"INCR", 0))
            tcp_ertek = int(tcp.recv(1024))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
            udp.settimeout(2)
            udp.sendto(UDP_CMD.pack(b"PLUS", 0), ("localhost", udp_port))
            adat, _ = udp.recvfrom(1024)
        udp_ertek = REPLY.unpack(adat)[0]
        if tcp_ertek != udp_ertek:
            ertek += 1
    return ertek


# ---- Ellenőrzés (ezt ne módosítsd) ----
if __name__ == "__main__":
    from ref_szerverek import egyezik, futtat, hibas_udp_szerver, inditas_tcp, inditas_udp, zh_tcp_szerver

    def teszt():
        inditas_tcp(zh_tcp_szerver, 12005, port=12005)
        inditas_udp(hibas_udp_szerver, 12006, [0, 1, 0, 0, -1])
        egyezik("hibás UDP szerver (5 kérdés)", ellenorzo(12005, 12006, 5), 3)
        inditas_tcp(zh_tcp_szerver, 12007, port=12007)
        inditas_udp(hibas_udp_szerver, 12008, [0])
        egyezik("hibátlan UDP szerver (4 kérdés)", ellenorzo(12007, 12008, 4), 0)

    futtat("F4", teszt)
```

### `feladatok/f5_proxy.py` – F5: TCP PROXY → UDP szerver (ZH 3/c feladatához)

```python
r"""
F5: TCP PROXY, ami UDP szerverhez továbbít           (gyakorlás a ZH 3. feladat c) részéhez)

  kliens --TCP, "5s i"--> PROXY --UDP, "6s i"--> UDP szerver (kész: ref_szerverek.f3_udp_szerver)
  kliens <--bytesztring-- PROXY <--"i" struct---- UDP szerver

  - a proxy a kliensek felé select-es TCP szerver, saját értéket NEM tárol
  - a parancsokat átfordítja:  SET -> SETVAL,  ADD -> ADD,  SUB -> SUB,  DBL -> DOUBLE
  - ismeretlen parancsra b"ERR" a válasz a kliensnek, és nem megy az UDP szerverhez
"""
import select
import socket
import struct

FORDITAS = {"SET": "SETVAL", "ADD": "ADD", "SUB": "SUB", "DBL": "DOUBLE"}

TCP_CMD = struct.Struct("5s i")
UDP_CMD = struct.Struct("6s i")
REPLY = struct.Struct("i")


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def proxy(proxy_port, udp_port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", proxy_port))
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
                    data = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    data = b""
                if not data:
                    inputs.remove(s)
                    s.close()
                    continue
                nev, x = TCP_CMD.unpack(data)
                nev = nev.rstrip(b"\x00").decode()
                udp_nev = FORDITAS.get(nev)
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), ("localhost", udp_port))
                valasz, _ = udp.recvfrom(1024)
                (ertek,) = REPLY.unpack(valasz)
                s.sendall(str(ertek).encode())


# ---- Ellenőrzés (ezt ne módosítsd) ----
if __name__ == "__main__":
    from ref_szerverek import egyezik, f3_udp_szerver, futtat, inditas_tcp, inditas_udp

    PROXY_PORT, UDP_PORT = 12010, 12009

    def kuld(sock, nev, x):
        sock.sendall(TCP_CMD.pack(nev.encode(), x))
        return sock.recv(1024)

    def teszt():
        inditas_udp(f3_udp_szerver, UDP_PORT)
        inditas_tcp(proxy, PROXY_PORT, UDP_PORT, port=PROXY_PORT)
        a = socket.create_connection(("localhost", PROXY_PORT), timeout=3)
        b = socket.create_connection(("localhost", PROXY_PORT), timeout=3)
        egyezik("SET 10", kuld(a, "SET", 10), b"10")
        egyezik("ADD 5", kuld(a, "ADD", 5), b"15")
        egyezik("SUB 3 (másik kliens)", kuld(b, "SUB", 3), b"12")
        egyezik("DBL 0", kuld(a, "DBL", 0), b"24")
        egyezik("ismeretlen parancs", kuld(b, "FOO", 1), b"ERR")
        egyezik("ADD 1 (az ERR nem érte el az UDP szervert)", kuld(a, "ADD", 1), b"25")
        a.close(); b.close()

    futtat("F5", teszt)
```

## 2.4 `feladatok/megoldasok/` – kész megoldások

Ezek a referencia-megoldások **lényegében megegyeznek** a fenti f1–f5 fájlok megírt (TODO nélküli) állapotával — csak a kódolási stílusban van apró eltérés (pl. `(szoveg_valasz,) = struct.unpack(...)` forma a tuple-unpackhez közvetlen `struct.unpack(...)[0]` helyett), és a `sys.path.insert(...)` sorral kiegészülnek, hogy önállóan a `megoldasok/` mappából is futtathatók legyenek és elérjék a `ref_szerverek.py`-t:

```python
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
```

Fájlnevek: `f1_kliens_megoldas.py`, `f2_select_szerver_megoldas.py`, `f3_udp_szerver_megoldas.py`, `f4_ellenorzo_megoldas.py`, `f5_proxy_megoldas.py`. A logikájuk funkcionálisan **azonos** a 2.3 pontban bemutatott f1–f5 kódokkal, ezért itt nem ismételjük meg sor szerint – a lényegi különbség csak az import-elérési út kiegészítése.

## 2.5 `feladatok/ref_szerverek.py` – a "ZH-n megkapott" szerverek (segédfájl, TELJES kód)

```python
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


# ---- F1 szerverei ----
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


# ---- F3 szervere (az F5-höz kell) ----
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
            if nev == "SETVAL": ertek = x
            elif nev == "ADD": ertek += x
            elif nev == "SUB": ertek -= x
            elif nev == "DOUBLE": ertek *= 2
            sock.sendto(F3_REPLY.pack(ertek), kliens)


# ---- F4 szerverei ----
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
                    if nev == "IN": ertek = x
                    elif nev == "INCR": ertek += x
                    elif nev == "DECR": ertek -= x
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
            if nev == "PUSH": ertek = x
            elif nev == "PLUS": ertek += x
            elif nev == "MINUS": ertek -= x
            sock.sendto(ZH_REPLY.pack(ertek), kliens)
```

## 2.6 `peldak/` – futtatható, kommentelt minták (p1–p5, TELJES kód)

Mind az öt fájl **önállóan futtatható** (saját szerveret indít szálban, majd lefuttatja és ellenőrzi a klienst/szervert), és bőséges kommentárt tartalmaz.

### `peldak/p1_tcp_kliens.py` – TCP/UDP KLIENS struct-tal (ZH 1. feladat a-b-c-d változat)

Kulcs: a szervert megkapod ("EZT A ZH-N MEGKAPOD" blokk: `tcp_szerver`, `udp_szerver`, amelyek `feldolgoz(text, n) = text[:n][::-1]` — az első n karaktert megfordítva adják vissza), a klienst te írod. `REQ = struct.Struct("20s i")`.

```python
def tcp_kliens(text, n):
    """Közös mag: elküldi a (szöveg, szám) párt, visszaadja a választ szövegként."""
    with socket.create_connection((HOST, TCP_PORT)) as sock:
        sock.sendall(REQ.pack(text.encode(), n))      # 1) .encode(): a struct 's' bájtot vár
        valasz = recv_exact(sock, n)                   # 2) a válasz hossza pontosan n bájt
    (szoveg,) = struct.unpack(f"{n}s", valasz)          # 3) a formátum a számból épül
    return szoveg.rstrip(b"\x00").decode()               # 4) kipótolt nullák levágása

def a_valtozat(text):
    """a) a szöveget a felhasználótól kérjük be (input), a számot generáljuk."""
    n = random.randint(1, len(text))
    return n, tcp_kliens(text, n)

def b_valtozat():
    """b) input.txt: soronként 'szó szám'; véletlen sor (1..3) kiválasztása."""
    with open(os.path.join(HERE, "input.txt"), encoding="utf-8") as f:
        sorok = f.read().splitlines()
    i = random.randint(1, 3)
    szo, szam = sorok[i - 1].split()
    n = int(szam)
    return szo, n, tcp_kliens(szo, n)

def c_valtozat():
    """c) input.json: a kulcsok SZÖVEGEK ("1","2","3"), az érték [szöveg, szám]."""
    with open(os.path.join(HERE, "input.json"), encoding="utf-8") as f:
        adat = json.load(f)
    kulcs = str(random.randint(1, 3))
    szo, n = adat[kulcs]
    return szo, n, tcp_kliens(szo, n)

def udp_kliens(text, n):
    """d) UDP: nincs connect, nincs recv_exact: egy datagram oda, egy vissza."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(text.encode(), n), (HOST, UDP_PORT))
        data, _ = sock.recvfrom(1024)
    (szoveg,) = struct.unpack(f"{n}s", data)
    return szoveg.rstrip(b"\x00").decode()
```
Önteszt (indításkor `input.txt`/`input.json` is létrejön): `tcp_kliens("almafa", 4) == "amla"`, `tcp_kliens("kortefa", 3) == "rok"`, stb.

### `peldak/p2_udp_szerver.py` – UDP SZERVER, ami egy számot tárol (ZH 3/a feladat)

`CMD = struct.Struct("5s i")` (PUSH/PLUS/MINUS), `REPLY = struct.Struct("i")`.

```python
def udp_szerver(ready=None):
    ertek = 0                       # a szerver "állapota": ciklus ELŐTT
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        if ready: ready.set()
        while True:
            data, kliens = sock.recvfrom(1024)
            if len(data) != CMD.size:
                continue
            nev, x = CMD.unpack(data)
            nev = nev.rstrip(b"\x00").decode()
            if nev == "PUSH": ertek = x
            elif nev == "PLUS": ertek += x
            elif nev == "MINUS": ertek -= x
            sock.sendto(REPLY.pack(ertek), kliens)
```
Önteszt: `PUSH 20 -> 20, PLUS 4 -> 24, MINUS 5 -> 19`; másik kliens (más port) is ugyanazt az állapotot látja.

### `peldak/p3_select_tcp_szerver.py` – TCP SZERVER select-tel, több klienst egyszerre (ZH 2. feladat)

`CMD = struct.Struct("4s i")` (IN/INCR/DECR), válasz: sima bytesztring.

```python
def select_szerver(ready=None):
    ertek = 0  # közös állapot, a ciklus előtt
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT)); server.listen(5)
        if ready: ready.set()
        inputs = [server]
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, cim = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    data = recv_exact(s, CMD.size)
                except ConnectionResetError:
                    data = b""
                if not data:
                    inputs.remove(s); s.close()
                    continue
                nev, x = CMD.unpack(data)
                nev = nev.rstrip(b"\x00").decode()
                if nev == "IN": ertek = x
                elif nev == "INCR": ertek += x
                elif nev == "DECR": ertek -= x
                s.sendall(str(ertek).encode())
```
Önteszt: két kliens egyszerre csatlakozik (ezt egy sima, nem select-es szerver nem bírná); `IN 20 -> 20, INCR 4 -> 24, DECR 5 -> 19`; új kapcsolat is a közös állapotot látja.

### `peldak/p4_ellenorzo_kliens.py` – ELLENŐRZŐ KLIENS (ZH 3/b feladat)

Adott egy megbízható TCP szerver (IN/INCR/DECR) és egy hibás UDP szerver (PUSH/PLUS/MINUS, minden parancsnál `random.choice([-1,0,1])` hibát ad hozzá).

```python
def tcp_ertek():
    with socket.create_connection((HOST, TCP_PORT)) as sock:
        sock.sendall(TCP_CMD.pack(b"INCR", 0))
        return int(sock.recv(1024))

def udp_ertek():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(UDP_CMD.pack(b"PLUS", 0), (HOST, UDP_PORT))
        data, _ = sock.recvfrom(1024)
    return REPLY.unpack(data)[0]

def hibazott_e():
    t = tcp_ertek(); u = udp_ertek()
    return t != u, t, u
```
Önteszt: `random.seed(7)`, mindkét szervert 100-ra állítja, majd 8 ellenőrzést futtat és kiírja, melyik hibázott. Megfigyelés: ha az UDP egyszer elcsúszik, az eltérés megmarad (az érték tárolt).

### `peldak/p5_tcp_proxy.py` – TCP PROXY, ami UDP szerverhez továbbít (ZH 3/c feladat)

`FORDITAS = {"IN": "PUSH", "INCR": "PLUS", "DECR": "MINUS"}` — logikája azonos a 2.2 fejezet 6/c mintájával és a `feladatok/f5_proxy.py`-val (csak a parancsnevek mások: IN/INCR/DECR helyett SET/ADD/SUB/DBL az f5-ben).

```python
def proxy(ready=None):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # EGY UDP socket, a ciklus előtt
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PROXY_PORT)); server.listen(5)
        if ready: ready.set()
        inputs = [server]           # az UDP socket NEM kerül ide
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    data = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    data = b""
                if not data:
                    inputs.remove(s); s.close()
                    continue
                nev, x = TCP_CMD.unpack(data)
                nev = nev.rstrip(b"\x00").decode()
                udp_nev = FORDITAS.get(nev)
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), (HOST, UDP_PORT))
                valasz, _ = udp.recvfrom(1024)
                (ertek,) = REPLY.unpack(valasz)
                s.sendall(str(ertek).encode())
```
Önteszt: `IN 20 -> 20, INCR 4 -> 24, DECR 5 -> 19` (két kliens, a proxyn keresztül); ismeretlen parancs -> `ERR`, a proxy tovább él.

## 2.7 `puska_socket.py` – a végső "puska" (TELJES kód)

Ez a fájl a csomag csúcspontja: egyetlen, jól kommentelt fájlban tartalmazza mind a **6 sablont** (TCP kliens, UDP kliens, select-es TCP szerver, UDP szerver, ellenőrző kliens, proxy), `<-- ITT VÁLTOZIK` jelölésekkel, hogy mit kell a konkrét ZH-feladathoz igazítani.

```python
"""
SOCKET ZH PUSKA   (minden sablon ugyanazt a keretet használja)

KERET HÁROM DÖNTÉSE
  1) TCP vagy UDP?   TCP kliens: socket.create_connection((host, port))
                     TCP szerver: socket.socket(AF_INET, SOCK_STREAM)
                     UDP (kliens és szerver): socket.socket(AF_INET, SOCK_DGRAM)
  2) Mi a struct formátum?  Struct("20s i").size a méret, SOHA ne írd be kézzel
                            ("5s i" = 12 bájt!). Ne tegyél elé !, <, > jelet.
  3) Mi a válasz típusa?
       bytesztring:  küld: sock.sendall(str(x).encode())      kap: int(sock.recv(1024))
       struct:       küld: REPLY.pack(x)                      kap: REPLY.unpack(adat)[0]

ALAPSZABÁLYOK
  - szöveg -> bájt: .encode()          s mező -> szöveg: .rstrip(b"\\x00").decode()
  - unpack tuple-t ad: (x,) = ... vagy ...[0]
  - TCP-n fix méretű struct olvasása: recv_exact; UDP-n: recvfrom(1024) elég
  - a szerver állapota (pl. ertek = 0) a ciklus ELŐTT jön létre
  - a recv üres bájtsort ad -> a kliens bontott
"""
import json, os, random, select, socket, struct

HOST = "localhost"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


# ============================================================ 1. TCP KLIENS
REQ = struct.Struct("20s i")  # <-- ITT VÁLTOZIK: a feladat struct formátuma

def tcp_kliens(szoveg, n, port):
    with socket.create_connection((HOST, port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))      # <-- ITT VÁLTOZIK: mit küldesz
        valasz = recv_exact(sock, n)                      # <-- ITT VÁLTOZIK: válasz mérete
    return struct.unpack(f"{n}s", valasz)[0].rstrip(b"\x00").decode()

# bemenet-változatok (csak a bemenet forrása más, a küldés ugyanaz):
def bemenet_txt(fajl):  # sorok: "szo szam"
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        sorok = f.read().splitlines()
    szo, szam = sorok[random.randint(1, 3) - 1].split()
    return szo, int(szam)

def bemenet_json(fajl):  # {"1": ["almafa", 4], ...}
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        adat = json.load(f)
    szo, n = adat[str(random.randint(1, 3))]
    return szo, n
# bemenet_input:  szoveg = input("Szoveg: ");  n = random.randint(1, len(szoveg))


# ============================================================ 2. UDP KLIENS
def udp_kliens(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), (HOST, port))
        adat, _ = sock.recvfrom(1024)
    return struct.unpack(f"{n}s", adat)[0].rstrip(b"\x00").decode()


# ============================================== 3. TCP SZERVER select-tel (több kliens)
TCP_CMD = struct.Struct("4s i")  # <-- ITT VÁLTOZIK: parancs formátuma

def select_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port)); server.listen(5)
        inputs = [server]
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s); s.close()
                    continue
                nev, x = TCP_CMD.unpack(adat)
                nev = nev.rstrip(b"\x00").decode()
                if nev == "IN": ertek = x
                elif nev == "INCR": ertek += x
                elif nev == "DECR": ertek -= x
                s.sendall(str(ertek).encode())  # <-- bytesztring VAGY struct


# ============================================================ 4. UDP SZERVER
UDP_CMD = struct.Struct("5s i")  # <-- ITT VÁLTOZIK
REPLY = struct.Struct("i")       # <-- ITT VÁLTOZIK

def udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, port))
        while True:
            adat, kliens = sock.recvfrom(1024)
            nev, x = UDP_CMD.unpack(adat)
            nev = nev.rstrip(b"\x00").decode()
            if nev == "PUSH": ertek = x
            elif nev == "PLUS": ertek += x
            elif nev == "MINUS": ertek -= x
            sock.sendto(REPLY.pack(ertek), kliens)


# ============================================================ 5. ELLENŐRZŐ KLIENS
def ellenorzo(tcp_port, udp_port):
    with socket.create_connection((HOST, tcp_port)) as tcp:
        tcp.sendall(TCP_CMD.pack(b"INCR", 0))
        tcp_ertek = int(tcp.recv(1024))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2)
        udp.sendto(UDP_CMD.pack(b"PLUS", 0), (HOST, udp_port))
        adat, _ = udp.recvfrom(1024)
    udp_ertek = REPLY.unpack(adat)[0]
    return tcp_ertek != udp_ertek  # True = az UDP szerver hibázott


# ============================================================ 6. PROXY (TCP -> UDP)
FORDITAS = {"IN": "PUSH", "INCR": "PLUS", "DECR": "MINUS"}  # <-- ITT VÁLTOZIK

def proxy(proxy_port, udp_port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.settimeout(2)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, proxy_port)); server.listen(5)
        inputs = [server]  # az UDP socket NEM kerül ide
        while True:
            readable, _, _ = select.select(inputs, [], [], 1.0)
            for s in readable:
                if s is server:
                    kliens, _ = server.accept()
                    inputs.append(kliens)
                    continue
                try:
                    adat = recv_exact(s, TCP_CMD.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s); s.close()
                    continue
                nev, x = TCP_CMD.unpack(adat)
                udp_nev = FORDITAS.get(nev.rstrip(b"\x00").decode())
                if udp_nev is None:
                    s.sendall(b"ERR")
                    continue
                udp.sendto(UDP_CMD.pack(udp_nev.encode(), x), (HOST, udp_port))
                valasz, _ = udp.recvfrom(1024)
                (ertek,) = REPLY.unpack(valasz)
                s.sendall(str(ertek).encode())
```

---

# 3. `zh_A_gyakorlas/`

Ez egy **ZH-szerű** (nem hivatalos, saját gyakorló-) keret, amely **szó szerint ugyanazokat a feladatokat** másolja le, mint amik a `zhpdf.pdf`-ben szerepelnek (lásd 1.1), de helyi (Docker nélküli) teszteléssel.

## 3.1 `00_OLVASD_EL.txt` (teljes szöveg)

```
SOCKET ZH A: GYAKORLO KERET (ugy, mint a ZH-n)
==============================================

Kell hozza: Python 3.8 vagy ujabb. Semmi mas (nincs Docker, nincs internet).

FELEPITES (ugyanaz, mint a ZH csomagban)
  feladat1/client.py     1. feladat: jaratfoglalas (TCP kliens)          6 pont
  feladat2/server.py     2. feladat: raktarkeszlet (select szerver)      6 pont
  feladat3/proxy.py      3. feladat: azonositasi proxy (TCP -> UDP)      8 pont
  tests.py               helyi tesztelo (az en utanzatom, NEM a valodi)
  megoldasok/            a kesz megoldasok (csak ha tenyleg elakadtal)

Minden vaz tetejen ott a feladat leirasa. Csak a "# ide ird a megoldast" alatt dolgozz.

ELLENORZES
  python tests.py check feladat1
  python tests.py check feladat2
  python tests.py check feladat3
(Mac: python3.) A teszt kiirja soronkent, mi volt jo (OK) es mi nem (HIBA), mit kapott es mit varna.

KEZI MOD (a ZH-s start/test mintajara, ket ablakkal)
  python tests.py start feladat1   -> masik ablakban: python feladat1/client.py localhost 20001
  python tests.py start feladat3   -> masik ablakban: python feladat3/proxy.py 10002 20002
                                      harmadikban:    python tests.py test feladat3 10002
  feladat2: python feladat2/server.py 10001  ->  masik ablakban: python tests.py test feladat2 10001

JAVASOLT GYAKORLAS
  1) Idozitett kor: feladatonkent max 25 perc, puska nelkul. Utana check.
  2) Ami elbukott, azt javitsd ki, aztan nezd meg a megoldast, ha kell.
  3) Masodik kor: a puskaval, hogy lasd, mennyit gyorsit.

FONTOS
  A tests.py itt csak egy utanzat: a ZH-n a valodi tesztet futtasd. A valodi teszt reszletei
  (pl. hogy a 2 uzenet ugyanazon a kapcsolaton megy-e az 1. feladatban) eltérhetnek az enyemtol.
```

## 3.2 `feladat1/client.py`, `feladat2/server.py`, `feladat3/proxy.py` – vázak (a letöltött állapotban RÉSZBEN kitöltve)

> Ezek a fájlok a feltöltéskori állapotban találhatók: a **feladatleírás** a docstringben szerepel (szó szerint megegyezik a `zhpdf.pdf` 1–3. feladatával), és a felhasználó **feladat1/client.py**-t már részben (hibásan/próba jelleggel) kitöltötte; **feladat2/server.py** és **feladat3/proxy.py** üres váz maradt (csak az importok és a docstring).

### `feladat1/client.py` (a mappában talált, részlegesen kitöltött állapot, TELJES tartalom)

```python
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
```

**Megjegyzés / hibalehetőség ebben a próbálkozásban** (hasznos tanulság, mert a hivatalos megoldás ezt javítja — lásd 3.3):
- az első üzenetben `b"CS8jjc"` (kisbetűs neptun kód), a másodikban `b"CS8JJC"` (nagybetűs) szerepel — **ellentmondás**, a két üzenetnek ugyanazt a neptun kódot kellene küldenie.
- a végén a `vegso` (foglalási azonosító) változót **nem írja ki és nem ad vissza semmit** (`print` vagy `return` hiányzik) — a hivatalos megoldás ezt kiírja.

### `feladat2/server.py` (üres váz, TELJES tartalom)

```python
"""
2. feladat: raktárkészlet (6 pont)              TCP SZERVER select-tel
Indítás:  python server.py <port>               (a szerver a localhost címen figyeljen)

A szerver KÜLÖNBÖZŐ RAKTÁRAK készletadatait tárolja (raktár -> termék -> darabszám).
A kliensek háromféle parancsot küldhetnek, struct formátum: (3s 6s 8s i) = (parancs, W, P, Q)
   ADD W P Q   adj hozzá Q darabot a W raktárban a P termékhez
   GET W P Q   kérdezd le a W raktárban a P termék aktuális darabszámát (Q nem releváns, 0)
   TOT W P Q   számítsd ki a W raktár teljes készletét, azaz a benne lévő termékek összdarabszámát
               (P, Q nem releváns; P "AAAAAAAA", Q 0)

A szerver minden parancs után egy egész számot ad vissza (i):
   ADD és GET után: a termék aktuális darabszáma (az adott raktárban)
   TOT után: a raktár teljes készlete

Példa:
   "ADD", "WH001", "Laptop", 10   -> 10
   "GET", "WH001", "Laptop", 0    -> 10
   "ADD", "WH001", "Mouse", 5     -> 5
   "TOT", "WH001", "AAAAAAAA", 0  -> 15

A kliens nem fog szándékosan helytelen üzenetet küldeni.
Több kliens egyszerre csatlakozhat (select), az állapot közös.

Ellenőrzés:  python tests.py check feladat2
"""
import select
import socket
import struct
import sys

# ide írd a megoldást
```

### `feladat3/proxy.py` (üres váz, TELJES tartalom)

```python
"""
3. feladat: azonosítási proxy (8 pont)          PROXY (TCP -> UDP)
Indítás:  python proxy.py <port> <szerver_port>   pl.: python proxy.py 10002 20002
          (a proxy a localhost címen figyeljen; az Azonosítási Szerver UDP-n a szerver_port-on figyel)

Kétféle kliens csatlakozik a proxyhoz TCP-n:
   - Felhasználó Kliens: bejelentkezési kérelmet küld
   - Vendég Kliens: információlekérési kérelmet küld
A Proxy az Azonosítási Szerver válaszát a megfelelő kliensnek küldi vissza.

A kliensek üzenete a proxyhoz: (i 20s) = (kliens_típus, felhasználónév)
   kliens_típus: 0 = Felhasználó Kliens, 1 = Vendég Kliens

A proxy select-tel egyszerre több klienst szolgál ki, és az Azonosítási Szerver felé (UDP) ezt küldi:
   Felhasználó Kliens esetén: ("LOGIN", felhasználónév)   formátum: (5s 20s)
   Vendég Kliens esetén:      ("GUEST", felhasználónév)   formátum: (5s 20s)

A szerver bytesztring válasza VÁLTOZATLANUL megy vissza a megfelelő klienshez.

   Kliens ---TCP---> Proxy ---UDP---> Azonosítási Szerver

Ellenőrzés:  python tests.py check feladat3
"""
import select
import socket
import struct
import sys

# ide írd a megoldást
```

## 3.3 `megoldasok/` – kész megoldások (TELJES kód)

### `megoldasok/feladat1/client.py`

```python
import socket
import struct
import sys

REQ = struct.Struct("6s 8s 7s")  # neptun, járatszám, üzenet típusa: 21 bájt
RESP = struct.Struct("i 10s")    # szabad helyek, utazási osztály: 14 bájt
BOOK = struct.Struct("12s")      # foglalási azonosító

NEPTUN = b"ABC123"  # <-- ide a saját neptun kódod (6 karakter)
JARAT = b"LH2048"


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    host, port = sys.argv[1], int(sys.argv[2])  # python client.py localhost 20001
    with socket.create_connection((host, port)) as sock:
        sock.sendall(REQ.pack(NEPTUN, JARAT, b"request"))
        szabad, osztaly = RESP.unpack(recv_exact(sock, RESP.size))
        osztaly = osztaly.rstrip(b"\x00").decode()
        if osztaly != "economy" or szabad < 3:
            tipus = b"reject"
        else:
            tipus = b"reserve"
        sock.sendall(REQ.pack(NEPTUN, JARAT, tipus))
        (azonosito,) = BOOK.unpack(recv_exact(sock, BOOK.size))
        print(tipus.decode(), azonosito.rstrip(b"\x00").decode())


if __name__ == "__main__":
    main()
```

### `megoldasok/feladat2/server.py`

```python
import select
import socket
import struct
import sys

CMD = struct.Struct("3s 6s 8s i")  # parancs, raktár, termék, mennyiség: 24 bájt (kitöltés miatt)
REPLY = struct.Struct("i")


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    port = int(sys.argv[1])  # python server.py <port>
    raktar = {}  # {raktár: {termék: darab}}, a ciklus előtt
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
                nev, w, p, q = CMD.unpack(adat)
                nev, w, p = (x.rstrip(b"\x00").decode() for x in (nev, w, p))
                ertek = 0
                if nev == "ADD":
                    termekek = raktar.setdefault(w, {})
                    termekek[p] = termekek.get(p, 0) + q
                    ertek = termekek[p]
                elif nev == "GET":
                    ertek = raktar.get(w, {}).get(p, 0)
                elif nev == "TOT":
                    ertek = sum(raktar.get(w, {}).values())
                s.sendall(REPLY.pack(ertek))  # struct válasz, nem bytesztring!


if __name__ == "__main__":
    main()
```

### `megoldasok/feladat3/proxy.py`

```python
import select
import socket
import struct
import sys

IN = struct.Struct("i 20s")     # kliens felől: kliens_típus, felhasználónév: 24 bájt
OUT = struct.Struct("5s 20s")   # UDP szerver felé: LOGIN/GUEST, felhasználónév: 25 bájt


def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data


def main():
    port, szerver_port = int(sys.argv[1]), int(sys.argv[2])  # python proxy.py <port> <szerver_port>
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # egy UDP socket, a ciklus előtt
    udp.settimeout(3)
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
                    adat = recv_exact(s, IN.size)
                except ConnectionResetError:
                    adat = b""
                if not adat:
                    inputs.remove(s)
                    s.close()
                    continue
                tipus, nev = IN.unpack(adat)
                parancs = b"LOGIN" if tipus == 0 else b"GUEST"  # 0: Felhasználó, 1: Vendég
                udp.sendto(OUT.pack(parancs, nev), ("localhost", szerver_port))
                valasz, _ = udp.recvfrom(1024)
                s.sendall(valasz)  # a válasz változatlanul megy vissza a kliensnek


if __name__ == "__main__":
    main()
```

## 3.4 `puska_socket_v2.py` – gyorsabb, keret-alapú "puska" (TELJES kód)

Ez egy **általánosabb**, nem az 5 konkrét feladatra, hanem a mögöttes **mintákra** fókuszáló segédlet: minden rész `<-- ITT VÁLTOZIK` jelöléssel mutatja, mit kell a ZH konkrét feladatához igazítani. Hét blokkból áll: A) TCP kliens, több üzenet egy kapcsolaton; B) TCP/UDP kliens, egy kérdés, bemenet-változatokkal; C) állapot tárolása szótárban (minta-kommentek, nem futtatható kód); D) select-es TCP szerver; E) UDP szerver; F) proxy; G) ellenőrző kliens.

```python
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
  - Méretet SOHA ne számolj kézzel: Struct("...").size
  - Gyors méret: python -c "import struct; print(struct.calcsize('4s 6s i'))"
  - TÖBB MEZŐ: Struct("6s 8s 7s") -> unpack annyi elemű tuple-t ad, ahány mező van: a, b, c = S.unpack(adat)
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

=== ELLENŐRZÉS (a ZH leírása szerint) ===
  python tests.py check <KÓD> feladatN
  python tests.py start <KÓD> feladatN
  python tests.py test feladatN <port>
  A tests mappa kódját nem elemzed, fekete doboz. Windowson: python, Macen: python3.

=== TIPIKUS HIBÁK ===
  - a másolt sablonban régi nevek/formátumok maradtak
  - str-t küldesz bájt helyett (.encode() hiányzik)
  - a struct méretet kézzel írtad be (kitöltés!)
  - unpack tuple, [0] vagy kicsomagolás kell
  - a második üzenet kikerül a with blokkból -> a kapcsolat már zárva
  - a szerver állapota a ciklusban jön létre (nullázódik); a ciklus ELÉ kell
  - bontott kliens (b"") nincs kivéve az inputs-ból -> végtelen ciklus
  - struct választ vársz, de bytesztring jön (vagy fordítva)
  - UDP socket a select listában (nem kell oda)
"""
import json, os, random, select, socket, struct, sys

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


# ==== A. TCP KLIENS, TÖBB ÜZENET EGY KAPCSOLATON (kérdés -> válasz -> döntés -> újabb üzenet) ====
KERES = struct.Struct("6s 8s 7s")   # <-- ITT VÁLTOZIK: a kérés formátuma
VALASZ = struct.Struct("i 10s")     # <-- ITT VÁLTOZIK: a szerver válasza
VEGSO = struct.Struct("12s")        # <-- ITT VÁLTOZIK: az utolsó válasz formátuma

def kliens_beszelgetes():
    host, port = sys.argv[1], int(sys.argv[2])
    with socket.create_connection((host, port)) as sock:
        sock.sendall(KERES.pack(b"mezo1", b"mezo2", b"elso"))
        szam, szoveg = VALASZ.unpack(recv_exact(sock, VALASZ.size))
        szoveg = sz(szoveg)
        # <-- ITT döntesz a kapott mezők alapján
        tipus = b"valasztas"  # <-- ITT: a feltétel alapján melyik üzenet megy
        sock.sendall(KERES.pack(b"mezo1", b"mezo2", tipus))  # UGYANAZON a kapcsolaton
        (vegso,) = VEGSO.unpack(recv_exact(sock, VEGSO.size))
        print(sz(vegso))


# ==== B. TCP KLIENS: EGY KÉRDÉS (struct küld, "Xs" kap), bemenet-változatok ====
REQ = struct.Struct("20s i")  # <-- ITT VÁLTOZIK

def tcp_kliens(szoveg, n, port):
    with socket.create_connection((HOST, port)) as sock:
        sock.sendall(REQ.pack(szoveg.encode(), n))
        valasz = recv_exact(sock, n)
    return struct.unpack(f"{n}s", valasz)[0].rstrip(b"\x00").decode()

def bemenet_txt(fajl):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        sorok = f.read().splitlines()
    szo, szam = sorok[random.randint(1, 3) - 1].split()
    return szo, int(szam)

def bemenet_json(fajl):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), fajl), encoding="utf-8") as f:
        adat = json.load(f)
    szo, n = adat[str(random.randint(1, 3))]
    return szo, n

def udp_kliens(szoveg, n, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        sock.sendto(REQ.pack(szoveg.encode(), n), (HOST, port))
        adat, _ = sock.recvfrom(1024)
    return struct.unpack(f"{n}s", adat)[0].rstrip(b"\x00").decode()


# ==== C. ÁLLAPOT TÁROLÁSA SZÓTÁRBAN (minták, nem a feladat megoldása) ====
#   egy szám:               ertek = 0                 (ciklus ELŐTT)
#   kulcs -> szám:          adatok = {}               adatok[k] = adatok.get(k, 0) + x
#   kulcs -> kulcs -> szám: adatok = {}
#       belso = adatok.setdefault(k1, {})             # ha még nincs k1, létrehozza az üres belső szótárat
#       belso[k2] = belso.get(k2, 0) + x              # hozzáadás (ha nincs, 0-ról indul)
#       adatok.get(k1, {}).get(k2, 0)                 # lekérdezés, hiba nélkül (nincs -> 0)
#       sum(adatok.get(k1, {}).values())              # a belső szótár összes értékének összege


# ==== D. TCP SZERVER select-tel (több kliens, közös állapot) ====
CMD = struct.Struct("4s 6s i")  # <-- ITT VÁLTOZIK
REPLY = struct.Struct("i")      # <-- ITT VÁLTOZIK

def select_szerver(port):
    allapot = {}  # <-- ITT VÁLTOZIK: egy szám (0) vagy szótár; a ciklus ELŐTT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port)); server.listen(5)
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
                    inputs.remove(s); s.close()
                    continue
                nev, kulcs, x = CMD.unpack(adat)  # <-- annyi név, ahány mező van
                nev, kulcs = sz(nev), sz(kulcs)
                ertek = 0  # <-- ITT a feladat logikája (parancsonként if/elif)
                s.sendall(REPLY.pack(ertek))  # struct válasz; bytesztring: str(ertek).encode()


# ==== E. UDP SZERVER ====
UDP_CMD = struct.Struct("5s i")    # <-- ITT VÁLTOZIK
UDP_REPLY = struct.Struct("i")     # <-- ITT VÁLTOZIK

def udp_szerver(port):
    ertek = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, port))
        while True:
            adat, kliens = sock.recvfrom(1024)
            nev, x = UDP_CMD.unpack(adat)
            nev = sz(nev)
            # <-- ITT a feladat logikája (parancsonként if/elif)
            sock.sendto(UDP_REPLY.pack(ertek), kliens)


# ==== F. PROXY (TCP elöl, UDP hátul) - a választ továbbadja ====
KLIENS_IN = struct.Struct("i 12s")     # <-- ITT VÁLTOZIK
SZERVER_OUT = struct.Struct("4s 12s")  # <-- ITT VÁLTOZIK

def proxy(proxy_port, udp_port):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # EGY UDP socket, ciklus előtt
    udp.settimeout(3)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, proxy_port)); server.listen(5)
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
                    inputs.remove(s); s.close()
                    continue
                tipus, nev = KLIENS_IN.unpack(adat)  # nev bájt marad, ha csak továbbadod
                parancs = b"????"  # <-- ITT: a tipus alapján melyik parancs megy
                udp.sendto(SZERVER_OUT.pack(parancs, nev), (HOST, udp_port))
                valasz, _ = udp.recvfrom(1024)
                s.sendall(valasz)  # VÁLTOZATLANUL vissza a kliensnek
                # ha a feladat átalakítást kér: struct -> unpack, bytesztring -> str(x).encode()


# ==== G. ELLENŐRZŐ KLIENS (két szerver értékének összehasonlítása) ====
def ellenorzo(tcp_port, udp_port, tcp_cmd, udp_cmd):
    with socket.create_connection((HOST, tcp_port)) as tcp:
        tcp.sendall(tcp_cmd)
        tcp_ertek = int(tcp.recv(1024))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2)
        udp.sendto(udp_cmd, (HOST, udp_port))
        adat, _ = udp.recvfrom(1024)
    udp_ertek = UDP_REPLY.unpack(adat)[0]
    return tcp_ertek != udp_ertek
```

## 3.5 `tests.py` – helyi tesztelő keret (saját utánzat, TELJES leírás + kulcsrészletek)

A docstring kiemeli: **"FIGYELEM: ez az én utánzatom, NEM a valódi tests.py. A ZH-n a megadott, valódi tests.py-t használd."** Docker és internet nélkül, tisztán Pythonban fut.

Fő elemek:
- `PROGRAM = {"feladat1": "client.py", "feladat2": "server.py", "feladat3": "proxy.py"}`
- `Jegyzo` osztály: szálbiztos eredménygyűjtő és kiíró (`OK`/`HIBA` soronként, majd összegzés).
- **1. feladat tesztje (`foglalas_szerver`)**: 5 forgatókönyvet futtat végig körforgásban:
  ```python
  FORGATOKONYVEK = [  # (szabad hely, osztály, ezt kell válaszolnia a kliensnek)
      (5, "economy", "reserve"),
      (2, "economy", "reject"),
      (5, "business", "reject"),
      (3, "economy", "reserve"),
      (0, "economy", "reject"),
  ]
  ```
  Minden kapcsolatnál ellenőrzi a neptun kód nem-üres voltát, a járatszámot (`LH2048`), az üzenettípust (`request`), majd a kliens második üzenetében a döntést (`reject`/`reserve`) a várt forgatókönyv szerint, és végül egy `FOG{sorszám:09d}` foglalási azonosítót küld vissza.
- **2. feladat tesztje (`teszt_feladat2`)**: két klienssel (`a`, `b`) 10 lépéses forgatókönyvet futtat (ADD/GET/TOT, több raktár/termék kombináció), majd egy új kapcsolattal ellenőrzi, hogy az állapot megmaradt-e.
- **3. feladat tesztje (`azonosito_szerver` + `teszt_feladat3`)**: az Azonosítási Szerver `LOGIN`/`GUEST` parancsra `b"LOGIN_OK:"+nev` / `b"GUEST_OK:"+nev` választ ad (ismeretlen parancsra `b"ERROR:"+parancs`); a tesztkliensek 5+1 lépéses forgatókönyvet futtatnak két kliensen (Felhasználó/Vendég), majd ellenőrzik, hogy bontás után egy új kliens is helyesen működik.
- Parancsok: `check <feladat>` (minden egyben), `start <feladat>` (tesztszerver naplója, kézi módhoz), `test <feladat> <port>` (saját szerver/proxy tesztelése), `--mappa <mappa>` opció (pl. a `megoldasok` mappa tesztelésére).

---

# 4. Heti gyakorlati csomagok

Ezek a hallgató **féléves gyakorlati óráinak** anyagai (5., 6., 7. gyakorlat), amelyek lépésről lépésre vezetik be a socket programozás témaköreit. Minden csomag azonos felépítésű: `demo/` (bemutató kód), `start/` (gyakorló váz), tematikus feladat-mappák (`README.txt`-vel), `tesztek/` (pyarmor-obfuszkált, Docker-alapú ellenőrzés — azonos mintájú, mint a `zh/tests.py`, de más NEPTUN-kód alapú azonosítással: `python tests.py check <NEPTUN> <feladat>`), és egy `tests.py` a csomag gyökerében (ugyanaz a harness-minta, mint a `zh/tests.py`-ban leírt, csak más `CHECKS` bejegyzésekkel az adott heti feladatokhoz).

## 4.1 `5_gyakorlat_csomag (1)/` — Socket alapok, hello world, struct, DNS, barkóba, számológép

### Feladat-README-k (teljes szöveg)

**`barkoba/README.txt`:**
```
Ide kerül a barkóba megoldása, ezekkel a fájlnevekkel:
  client.py      indítás: python client.py <host> <port> <NEPTUN>
Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <NEPTUN> barkoba
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`dns/README.txt`:**
```
Ide kerül a DNS kézzel kihívás megoldása, ezekkel a fájlnevekkel:
  client.py      indítás: python client.py <host> <port> <név>   (a kapott IP-címet írja ki)
Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <NEPTUN> dns
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`szamologep/README.txt`:**
```
Ide kerül a számológép (Gyakorlás III.) megoldása, ezekkel a fájlnevekkel:
  server.py      indítás: python server.py <port>
  client.py      indítás: python client.py <host> <port> <a> <op> <b>
Ellenőrzés egy paranccsal, a csomag mappájából (ahol a tests.py van):
  python tests.py check <NEPTUN> szamologep
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

### `demo/hello/` – legelső TCP kliens-szerver példa (TELJES kód)

`hello_client.py`:
```python
import socket
import sys

server_addr = (sys.argv[1], int(sys.argv[2]))   # pl. python hello_client.py localhost 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(server_addr)
    client.sendall("Hello server".encode())
    data = client.recv(16)
    print("Received:", data.decode())
```

`hello_server.py`:
```python
import socket
import sys

server_addr = ("localhost", int(sys.argv[1]))   # pl. python hello_server.py 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_addr)
    sock.listen(1)
    sock.settimeout(1.0)     # Windowson a Ctrl+C csak igy szakitja meg az accept-et

    try:
        while True:
            try:
                client, client_addr = sock.accept()
                with client:
                    print("Connected:", client_addr)
                    data = client.recv(16)
                    print("Received:", data.decode())
                    client.sendall("Hello client".encode())
            except TimeoutError:
                pass
    except KeyboardInterrupt:
        print("Server stopped")
```

### `demo/socket_basics.py` – interaktív bemutató (összefoglalva, kulcs kódrészletekkel)

Lépésenkénti (`input()`-ra váró) oktató szkript 5 blokkal:
1. **Hostnév és IP-cím**: `socket.gethostname()`, `socket.gethostbyname("www.example.org")`, `socket.gethostbyname_ex(...)` (hostnév+aliasok+címek), `socket.gethostbyaddr(ip)` (reverse DNS, `socket.herror` kezelés).
2. **Portok és szolgáltatásnevek**: az 1–100 TCP portot végigpróbálja `socket.getservbyport(port, "tcp")`-vel, kiírja az ismert szolgáltatásneveket.
3. **htons()/ntohs()**: byte-sorrend konverzió bemutatása (`socket.htons(543)`, majd vissza `ntohs`).
4. **struct pack/unpack**: `struct.Struct("i 2s f")` példán mutatja a `pack`/`unpack`/`.size`-t, és a hálózati byte-sorrendet (`"!i 2s f"`).
5. **String ↔ bytes ↔ struct**: `"hello".encode()`, `struct.pack("8s", ...)` (nullával kipótolás bemutatása), `.decode()`, `.strip("\x00")`.

### `start/hello_id/` – azonosítós "hello" gyakorlófeladat (TELJES kód, részben kitöltött állapotban)

`client.py`:
```python
import socket
import struct
import sys

packer = struct.Struct("12s")                    # egyelore csak a 'Hello server' uzenet
server_addr = (sys.argv[1], int(sys.argv[2]))   # pl. python client.py localhost 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(server_addr)
    client.sendall(packer.pack("Hello server".encode()))
    data = client.recv(64)
    print("Received:", data.decode())
```

`server.py` (a `USERS` szótárat ismeri, de a kliens még nem küld azonosítót — ez a gyakorlófeladat lényege, hogy kiegészítsék):
```python
import socket
import struct
import sys

USERS = {
    0: "vendég", 1: "Anna", 2: "Bence", 3: "Csilla", 4: "Dávid", 5: "Emese",
    6: "Ferenc", 7: "Gréta", 8: "Henrik", 9: "Ilona", 10: "János",
}

packer = struct.Struct("12s")                    # egyelore csak a 'Hello server' uzenet
server_addr = ("localhost", int(sys.argv[1]))   # pl. python server.py 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_addr)
    sock.listen(1)
    sock.settimeout(1.0)

    try:
        while True:
            try:
                client, client_addr = sock.accept()
                print(f"Connected: {client_addr[0]}:{client_addr[1]}")
                with client:
                    (greeting,) = packer.unpack(client.recv(packer.size))
                    user_id = 0                          # a kliens meg nem kuldi az azonositojat
                    print(f"Received: {greeting.decode()} from user {user_id}")
                    name = USERS.get(user_id, "ismeretlen")
                    client.sendall(f"Hello {name}".encode())
            except TimeoutError:
                pass
    except KeyboardInterrupt:
        print("Server stopped")
```

`users.json` (ugyanaz az adat, mint a `USERS` szótár, fájlban is):
```json
{
  "0": "vendég", "1": "Anna", "2": "Bence", "3": "Csilla", "4": "Dávid", "5": "Emese",
  "6": "Ferenc", "7": "Gréta", "8": "Henrik", "9": "Ilona", "10": "János"
}
```

### `tesztek/` és `tests.py`

A `tesztek/` mappa (`bank.py`, `barkoba.py`, `common.py`, `dns_kezzel.py`, `szamologep.py`, `szavazas.py`, `webszerver.py`, `run.py`) ugyanúgy **Pyarmor-obfuszkált**, mint a `zh/tesztek/` (lásd 1.5. pont), csak a Pyarmor runtime külön `pyarmor_runtime_000000/` almappában. A `tests.py` (392 sor) szerkezetileg megegyezik a `zh/tests.py`-ban (1.4. pont) részletesen leírt Docker-alapú harness-szel, de itt a token nem egy 12 karakteres kód, hanem a hallgató **NEPTUN kódja** (`python tests.py check <NEPTUN> <feladat>`), és a `CHECKS` szótár a heti feladatokat (`barkoba`, `dns`, `szamologep`) tartalmazza portokkal/indítási paraméterekkel.

## 4.2 `6_gyakorlat_csomag-2/` — Blokkoló vs. select-es szerverek, HTTP/TLS, bank, szavazás, webszerver

### Feladat-README-k (teljes szöveg)

**`bank/README.txt`:**
```
Ide kerül a bankszerver (B rész) megoldása, ezekkel a fájlnevekkel:
  server.py      indítás: python server.py <port>
Ellenőrzés: python tests.py check <NEPTUN> bank
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`szavazas/README.txt`:**
```
Ide kerül a szavazószerver megoldása, ezekkel a fájlnevekkel:
  server.py      indítás: python server.py <port>
Ellenőrzés: python tests.py check <NEPTUN> szavazas
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`webszerver/README.txt`:**
```
Ide kerül a saját webszerver megoldása, ezekkel a fájlnevekkel:
  web_server.py  indítás: python web_server.py <host> <port> www   (a mellette lévő www mappát szolgálja ki)
Ellenőrzés: python tests.py check <NEPTUN> webszerver
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```
A `webszerver/www/` mappa egy minta weboldalt tartalmaz a teszteléshez: `index.html` (13 sor, "Működik!" cím, `style.css`-re hivatkozik, `kep.png`-t jelenít meg), `style.css` (3 sor egyszerű stílus), `kep.png` (bináris kép, 128×128, nem olvasható/beágyazható tartalom).

### `demo/blocking_client.py` + `blocking_server.py` – blokkoló szerver korlátai (kísérletek [K1]–[K3])

A blokkoló szerver (`listen(0)`, egyszerre egy klienst szolgál ki, 2 mp mesterséges késleltetéssel) bemutatja, hogy **egy lassú kliens blokkolja a többit** (`three_clients()` függvény: 3 kliens csatlakozik egyszerre, de sorban kapnak választ). Kulcsrészlet:
```python
def blocking_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(ADDR)
        server.listen(0)                  # [K1] a lehető legrövidebb várakozási sor
        while True:
            client, addr = server.accept()
            with client:
                msg = client.recv(1024)
                time.sleep(2)              # [K1] lassú kiszolgálás, hogy lássuk a sorban állást
                client.sendall(b"Hello client")
                client.recv(1024)          # megvárjuk, hogy a kliens bontson
```

### `demo/select_client.py` + `select_server.py` – a select bevezetése, TCP-folyam csapdák ([K4]–[K7])

A select-es szerver több klienst kezel egyszerre. A kliens oldali kísérletek bemutatják a TCP bájtfolyam-jelenséget:
- `two_messages()` [K6]: két `sendall` gyorsan egymás után — a szerver késleltetve olvassa, láthatóan **összefolyhat** egy `recv`-ben.
- `split_message()` [K7]: egy 9 bájtos struct üzenet ( `"i i c"` ) **két részletben** érkezik (4+5 bájt, köztük 1 mp szünet) — demonstrálja, hogy sima `recv(1024)` ekkor hibásan csak a töredéket kapja, és **`recv_exact`** kell.
```python
def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return b""
        data += chunk
    return data
```
A `[K5]` kísérlet megmutatja: ha `inputs.remove(s)` kikommentezve marad, a bontott kliens végtelenül "olvashatónak" tűnik és a szerver 100%-on pörög.

### `demo/http_tls.py` – valódi HTTP/HTTPS kérés socket-tel (TELJES kód logikája)

Három függvény mutatja be ugyanazt a GET-kérést különböző rétegeken:
```python
def http_plain():       # sima TCP a 80-as porton (HTTP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80)); sock.sendall(request.encode()); print(sock.recv(200).decode())

def https_tls():         # TLS-becsomagolt socket a 443-as porton (HTTPS)
    context = ssl.create_default_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tls = context.wrap_socket(sock, server_hostname=host)
    tls.connect((host, 443)); print(tls.version())   # pl. TLSv1.3
    tls.sendall(request.encode()); print(tls.recv(200).decode())

def http_to_https():     # sima HTTP kérés a 443-as portra: TLS kézfogás hiányában értelmetlen válasz jön
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 443)); sock.sendall(request.encode())
    print(sock.recv(300).decode(errors="replace"))
```
Ez szemlélteti a TLS szükségességét a 443-as (HTTPS) porton.

### `start/calc_client.py` + `calc_server.py` – egyszerű számológép gyakorlófeladat (TELJES kód)

```python
# calc_client.py
packer = struct.Struct("i i c")  # ket szam es a muveleti jel
host, port, a, op, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5])
op = "*" if op == "x" else op    # a shell miatt 'x'-szel jelölik a szorzást
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    client.sendall(packer.pack(a, b, op.encode()))
    result, _, _ = packer.unpack(client.recv(packer.size))
    print(f"{a} {op} {b} = {result}")
```
```python
# calc_server.py
ops = {b"+": lambda a,b: a+b, b"-": lambda a,b: a-b, b"*": lambda a,b: a*b, b"/": lambda a,b: a//b}
# fogadja az (a,b,op) structot, kiszámolja az eredményt, visszaküldi (result, 0, b"R") formában
```

### `tesztek/` és `tests.py`

Ugyanaz a mintázat, mint 4.1-ben: obfuszkált `bank.py`, `barkoba.py`, `common.py`, `dns_kezzel.py`, `szamologep.py`, `szavazas.py`, `webszerver.py` + `run.py`, és egy 392 soros `tests.py` Docker-harness (NEPTUN-kódos azonosítással).

## 4.3 `7_gyakorlat_csomag-2/` — UDP, TCP proxy, select-es szerverek gyakorlása, cache, proxy, STUN

### Feladat-README-k (teljes szöveg)

**`cache/README.txt`:**
```
Ide kerül a gyorsítótáras proxy megoldása, ezekkel a fájlnevekkel:
  cache_proxy.py   indítás: python cache_proxy.py <port> <szerver_port>
Ellenőrzés: python tests.py check <NEPTUN> cache
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`proxy/README.txt`:**
```
Ide kerül a B rész proxyja megoldása, ezekkel a fájlnevekkel:
  proxy.py         indítás: python proxy.py <port> <összeadó_port> <szorzó_port>
Ellenőrzés: python tests.py check <NEPTUN> proxy
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

**`stun/README.txt`:**
```
Ide kerül a STUN kliens megoldása, ezekkel a fájlnevekkel:
  client.py        indítás: python client.py <host> <port>   (a kapott címet IP:port alakban írja ki)
Ellenőrzés: python tests.py check <NEPTUN> stun
A programok minden adatot parancssori paraméterként kapnak (sys.argv), input() nélkül.
```

### `demo/` – teljes TCP-proxy lánc bemutatása (TELJES kód logikája)

Ez a csomag mutatja be legrészletesebben a **proxy mintát**, amire a ZH 3. feladata is épül:

- **`square_server.py`** — a "backend" TCP szerver, egy állandó kapcsolaton sok kérést szolgál ki (`i` → `i`, négyzetre emelés):
  ```python
  def square_server():
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
          server.bind(ADDR); server.listen(1); server.settimeout(1.0)
          while True:
              try: conn, addr = server.accept()
              except TimeoutError: continue
              with conn:
                  while data := recv_exact(conn, number.size):   # amig a proxy nem bont
                      (n,) = number.unpack(data)
                      conn.sendall(number.pack(n * n))
  ```
- **`tcp_proxy.py`** — a proxy: a kliensek felé `select`-es szerver, a backend felé **egyetlen, állandó** kliens-kapcsolat:
  ```python
  def tcp_proxy():
      with socket.socket(...) as backend, socket.socket(...) as server:
          backend.connect(SERVER_ADDR)         # egyszer, a ciklus elott
          server.bind(PROXY_ADDR); server.listen(5)
          inputs = [server]                     # a backend NEM kerul ide
          while True:
              readables, _, _ = select.select(inputs, [], [], 1.0)
              for s in readables:
                  if s is server:
                      client, addr = server.accept(); inputs.append(client); continue
                  msg = recv_exact(s, in_packer.size)
                  if not msg:
                      inputs.remove(s); s.close(); continue
                  name, n = in_packer.unpack(msg)          # atcsomagolas: a szerver csak a szamot kapja
                  backend.sendall(out_packer.pack(n))
                  (result,) = out_packer.unpack(recv_exact(backend, out_packer.size))
                  s.sendall(reply_packer.pack(name, result))
  ```
- **`name_client.py`** — a kliens, amely a proxyhoz kapcsolódik (nem ismeri a backendet), 3 kérést küld egy kapcsolaton (`10s i` formátum, válasz is `10s i`, nullakitöltés-levágás a névnél).
- **`udp_client.py`** + **`udp_server.py`** — UDP alapok bemutatása: `[K1]`/`[K2]` egy üzenet és válasz, kisebb puffer hatás (`recvfrom(5)` egy nagyobb üzenetre); `[K3]` három kliens egyszerre küld, a UDP szerver `recvfrom`/`sendto`-val válaszol a feladó címére, nincs listen/accept.

### `start/` – hat gyakorló váz (TELJES kód)

- **`add_udp_server.py`** — UDP összeadó szerver: `request = Struct("i i")`, `reply = Struct("i")`, méretellenőrzéssel (`len(data) != request.size` → eldobás), `settimeout(1.0)` Windowson a Ctrl+C miatt.
- **`mul_tcp_server.py`** — select-es TCP szorzó szerver: `request = Struct("i i")`, `reply = Struct("i")`, a `p3_select_tcp_szerver.py`/`select_server.py` mintájára.
- **`calc_client.py`** / **`calc_server.py`** — azonos a 4.2-ben bemutatott számológép gyakorlattal (`"i i c"` formátum).
- **`proxy_client.py`** — a proxy-feladathoz tartozó kliens: `request = Struct("i i c")` (két szám + művelet), válasz `reply = Struct("i")` (csak az eredmény, bytesztring helyett struct).
- **`rate_server.py`** — "lassú árfolyam-szerver": `request = Struct("3s")` (devizakód, pl. `b"EUR"`), `reply = Struct("i")`; minden lekérdezésnél `time.sleep(1.0)`-ot szimulál (ez indokolja a gyorsítótárazást a `cache/` feladatban), az árfolyamokat `rates.setdefault(code, random.randint(100, 99999))`-tel véletlenszerűen, de konzisztensen generálja.
- **`select_server.py`** — általános select-es minta `"i i c"` (9 bájt) üzenetekkel, `recv_exact` használatával, `OK` válasszal.

### `tesztek/` és `tests.py`

Ugyanaz a Pyarmor-obfuszkált minta (itt plusz `cache.py`, `proxy.py`, `rdt.py`, `stun.py` is szerepel a `bank.py`, `barkoba.py`, `common.py`, `dns_kezzel.py`, `szamologep.py`, `szavazas.py`, `webszerver.py` mellett), és egy 402 soros `tests.py` Docker-harness, NEPTUN-kódos azonosítással — szerkezete megegyezik a `zh/tests.py`-ban (1.4. pont) leírttal.

---

# 5. Top-level fájlok

- **`Socket_ZH_magyarazat.pdf`** — ugyanaz a dokumentum, mint a `telkom_socket_zh/magyarazat/Socket_ZH_magyarazat.pdf` (lásd 2.2. fejezet, teljes transzkripció ott található).
- **`ZH_osszefoglalo.md`** — ez a jelen összefoglaló fájl.
- **`.DS_Store`** fájlok (a mappa gyökerében és több almappában) — macOS Finder metaadat, nem releváns tartalom, figyelmen kívül hagyva.

---

# 6. `ujak/` – korábban kihagyott mappa

Ez a mappa korábban kimaradt a feldolgozásból. Három részből áll: egy duplikált `zh/` almappából, egy README nélküli "Minta ZH"-ból (kész, működő referenciakóddal), és egy "Pót ZH" autókereskedés-feladatból két variánsban (ez utóbbi piszkozat-jellegű, hibás/hiányos kóddal).

## 6.1 `ujak/zh/` és `ujak/zhpdf.pdf`

`ujak/zh/` ugyanaz, mint a fenti `zh/` mappa (azonos tartalom, lásd ott). Az egyetlen eltérés, hogy a `zhpdf.pdf` itt nem az `ujak/zh/` almappában van, hanem egy szinttel feljebb, `ujak/zhpdf.pdf` néven – tartalma (checksum alapján) megegyezik a `zh/zhpdf.pdf`-fel.

## 6.2 `ujak/Minta_ZH/` – README nélküli, kész mintamegoldások

Ebben a mappában nincs `README.txt` / feladatleírás, csak teljes, futásra kész (nem obfuszkált, nem vázlat) `.py` fájlok két független forgatókönyvhöz (`ZH_1/`, `ZH_2/`). A feladatleírásokat alább a kód alapján visszafejtve, a dokumentumban eddig használt README-stílusban írtuk meg.

### 6.2.1 `Minta_ZH/ZH_1/` – beteg / orvos / patika

**Szerepek a kód alapján:**
- `beteg.py` – TCP **kliens** ("beteg" = a teszt/referencia kliens, amit a tesztrendszer futtatna a hallgató megoldása ellen). A `('localhost', 1000)` TCP címre kapcsolódik.
- `orvos.py` – TCP **szerver**, ami a parancssori argumentumokból egy betegség→gyógyszer szótárat épít fel, és a `('localhost', 1000)` TCP porton `select`-tel fogadja a betegeket. **Ez a tényleges ZH-feladat**, amit a hallgatónak meg kell írnia.
- `patika.py` – UDP **szerver** ("patika" = teszt/referencia backend), a `('localhost', 1001)` címen figyel; ezt a beteg közvetlenül, az orvostól kapott port alapján keresi meg, az orvos maga nem kommunikál vele.

Mindhárom fájl a `struct.Struct('32s I I')` csomagolót használja: egy 32 bájtos szöveges mező (betegség/tünet neve, illetve gyógyszer neve) és két 4 bájtos egész szám (darabszám, illetve portszám).

**Feladatleírás (visszafejtve).** Írja meg az `orvos.py` TCP szervert, amely betegeket szolgál ki! A program parancssori argumentumként betegség–gyógyszer páro(ka)t kap, pl.:

```
python orvos.py HUZODAS gipsz FEJFAJAS aszpirin
```

ezekből építi fel a `cure` szótárat (`cure["HUZODAS"] = "gipsz"`, stb.). A szerver a `localhost:1000` TCP porton figyel, `select`-tel egyszerre több beteget is ki tud szolgálni (`settimeout(1.0)`, `SO_REUSEADDR`).

Egy beteg (adott, `beteg.py`) `'32s I I'` formátumú kérést küld: az első (32 bájtos) mezőben a tünet/betegség neve, a másik két mező a kérésben nem releváns (0, 0).

A szervernek meg kell néznie, van-e a `cure` szótárban gyógyszer az adott tünetre:
- ha **nincs**, a válasz `("NINCS", 0, patika_port)` legyen (`'32s I I'` formátumban), ahol `patika_port` a patika UDP portja (1001);
- ha **van**, a válasz `(gyógyszer_neve, véletlen_darabszám, patika_port)` legyen, ahol a darabszám egy 1 és 3 közötti véletlen egész szám (`random.randint(1, 3)`).

A beteg a választ megkapva, ha nem "NINCS" gyógyszert kapott, saját maga (UDP-n, a válaszban kapott port alapján) megkeresi a patikát: elküldi neki a gyógyszer nevét, és kiírja a patika válaszát. Ez már adott (a beteg és a patika kódja), az orvosnak nem kell UDP-n a patikával beszélnie.

Hibakezelés: `timeout` kivétel esetén a ciklus folytatódik (nincs teendő), `struct.error` esetén (hibás/hiányos adat érkezett) a hibás kliens socketet el kell távolítani az `inputs` listából.

**Teszt fájlok (adott):**

```python
# beteg.py – teszt kliens
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import struct

packer = struct.Struct('32s I I')
server_addr = ('localhost', 1000)


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    data = ("HUZODAS".encode(), 0, 0)

    client.sendall(packer.pack(*data))

    data = client.recv(packer.size)
    res = packer.unpack(data)
    med = res[0].decode().replace('\x00','')
    print("Gyógyszer: ", med, " ennyit: ", res[1])

    if med != 'NINCS':
        patika_port = res[2]
        with socket(AF_INET, SOCK_DGRAM) as patika:

            server_addr = ('localhost', patika_port)

            print("Kertem a patikaba gyogyszert:")

            sent = patika.sendto(med.encode(), server_addr)

            data, address = patika.recvfrom(4)

            print("Patika valasza: ", data.decode())
```

```python
# patika.py – teszt szerver (patika)
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ('localhost', 1001)
sock.bind(server_addr)

while True:
    print("várakozok betegre...")
    data, address = sock.recvfrom(256)
    print("beteg érkezett: ", address, " ilyen gyószert kér: ", data.decode() )

    sock.sendto("KESZ".encode(), address)
```

**Megoldás (`orvos.py`):**

```python
import builtins
from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select
import sys
import random

packer = struct.Struct('32s I I')
server_addr = ('localhost', 1000)
shop_port = 1001

build = sys.argv[1:]

cure = {}
for i in range(len(build) // 2):
	cure[build[i*2]] = build[i*2+1]

print(cure)
with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    inputs = [ server ]
    while True:

        readable, writable, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                print('Beteg érkezett')
            else:
                try:
                    data = s.recv(packer.size)
                    req = packer.unpack(data)

                    ill = req[0].decode().replace('\x00','')
                    print("Beteg tünetei:", ill)
                    res = ('NINCS'.encode(), 0, shop_port)
                    if ill in cure:
                        res = (cure[ill].encode(), random.randint(1,3), shop_port)

                    print('Betegségre gyógyszer:', res)
                    s.sendall(packer.pack(*res))
                except timeout:
                    pass
                except struct.error:
                    inputs.remove(s)
```

### 6.2.2 `Minta_ZH/ZH_2/` – bid / licit / log

**Szerepek a kód alapján:**
- `bid.py` – TCP **kliens** ("bid" = teszt/referencia kliens), a `('localhost', 999)` TCP címre kapcsolódik, és parancssori argumentumként kapott ajánlatokat (`offers = sys.argv[1:]`) küld el egymás után, ugyanazon a kapcsolaton.
- `licit.py` – TCP **szerver** ("licit" = aukciós szerver, `select`-tel), ez a tényleges ZH-feladat. A `('localhost', 999)` TCP porton figyel, és egy `('localhost', 998)` UDP naplózó szervernek jelenti az új, elfogadott árakat.
- `log.py` – UDP **szerver** ("log" = teszt/referencia backend), a `('localhost', 998)` címen csak fogad és kiír, választ nem küld.

Mindhárom fájl a `struct.Struct('8s I')` csomagolót használja: egy 8 bájtos szöveges parancs/állapot mező, és egy 4 bájtos egész szám (ajánlat/ár).

**Feladatleírás (visszafejtve).** Írja meg a `licit.py` TCP aukciós szervert, amely a `localhost:999` porton figyel, `select`-tel egyszerre több licitálót is tud kezelni (`settimeout`, `SO_REUSEADDR`), és egy, a program indításakor 0-ra állított `price` (jelenlegi legjobb ár) változót tart számon.

A licitálók (adott, `bid.py`) `'8s I'` formátumú kérést küldenek: az első mező mindig a szöveg `"BID"`, a második az ajánlott összeg (egész szám). A szervernek minden `BID` kérésnél meg kell néznie, hogy az ajánlott összeg nagyobb-e a jelenlegi árnál:

- ha **nem** nagyobb, a válasz `("LOW", price)` legyen (a jelenlegi, változatlan ár), `'8s I'` formátumban;
- ha **nagyobb**, frissítse a `price`-t az új összegre, a válasz `("OK", price)` legyen, és az új árat szövegként (UDP-n, `sendto`, válasz fogadása nélkül) jelentse be a naplózó szervernek (`localhost:998`).

Hibakezelés: `timeout` kivétel esetén folytatás, `struct.error` esetén a hibás kliens socket eltávolítása az `inputs` listából.

**Teszt fájlok (adott):**

```python
# bid.py – teszt kliens
from socket import socket, AF_INET, SOCK_STREAM
import struct
import sys

packer = struct.Struct('8s I')
server_addr = ('localhost', 999)

offers = sys.argv[1:]

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    for offer in offers:
        data = ("BID".encode(), int(offer))

        client.sendall(packer.pack(*data))

        data = client.recv(packer.size)
        resoult = packer.unpack(data)
        print("Uj ajanlat elküldve: ", offer, " a licit valasza: ", resoult[0].decode().replace('\x00','') )
```

```python
# log.py – teszt szerver (log)
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = ('localhost', 998)

sock.bind(server_addr)

while True:
    data, address = sock.recvfrom(256)
    print("Új ajánlat érkezett:", data.decode())
```

**Megoldás (`licit.py`):**

```python
from socket import socket,AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select

packer = struct.Struct('8s I')
server_addr = ('localhost', 999)
log_addr = ('localhost', 998)

price = 0

with socket(AF_INET, SOCK_STREAM) as server:
    with socket(AF_INET, SOCK_DGRAM) as log:
        server.bind(server_addr)
        server.listen(1)
        server.settimeout(2)
        server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        inputs = [ server ]
        while True:
            readable, writable, exceptional = select.select(inputs, [], inputs, 1)

            for s in readable:
                if s is server:
                    print('Új licitáló')
                    client, client_addr = s.accept()
                    inputs.append(client)
                else:
                    try:
                        data = s.recv(packer.size)
                        request = packer.unpack(data)


                        newprice = request[1]
                        print("A licitáló ajánlata: ", newprice)

                        resoult = ('LOW'.encode(), price)
                        if newprice > price:
                            price = newprice
                            resoult = ('OK'.encode(), price)
                            log.sendto(f"{price}".encode(), log_addr)

                        print('Az ár a licit megtétele után: ', price)
                        s.sendall(packer.pack(*resoult))
                    except timeout:
                        pass
                    except struct.error:
                        inputs.remove(s)
```

## 6.3 `ujak/PotZH/` – autókereskedés (Pót ZH)

Ez a mappa egy pótzárthelyi feladat két variánsban: `1,2,3/` (egyetlen, egyszerűbb szerver) és `4/` (két UDP backend adatbázis között kell routingolni). **Fontos:** a `4/` variáns forráskódja hallgatói piszkozatnak tűnik – copy-paste hibák, hiányzó importok, üres `if`/`elif` ágak, nem konzisztens becsomagolás. Ezeket NEM javítottuk ki "csendben", hanem alább mindegyiket megjelöljük, és két, önállóan is futásképes, javított megoldást adunk rá.

### 6.3.1 `PotZH/1,2,3/` – alapverzió (ez a pár már helyesen, együtt működik)

**Szerepek:** `autokereskedes.py` a TCP szerver (a kereskedő/proxy – ez a feladat), `vasarlo.py` ("vásárló" = vevő) a teszt/referencia TCP kliens. A szerver parancssori argumentumokból épít fel egy autó-adatbázist: minden autó egy `(tipus, kor, ar)` szöveg-hármas (`cars[i] = (tipus, kor, ar)`), pl.:

```
python autokereskedes.py suzuki 3 2000000 opel 7 1500000
```

A kliens `'10s 10s'` formátumú kérést küld: egy mezőnév (`"tipus"`, `"kor"` vagy `"ar"`) és egy érték (pl. `("kor", "1")`). A szerver a `cars` adatbázisban megkeresi az illő autókat:
- `tipus`: pontos egyezés a típusra,
- `kor`: azok az autók, amelyeknek a kora **≤** a kért érték,
- `ar`: azok az autók, amelyeknek az ára **≤** a kért érték,

és a találatokat `"tipus kor ar|"` alakban, `|`-tal elválasztva, nyers (nem struct-tal csomagolt, csak `.encode()`-olt) szövegként küldi vissza; a kliens `'32s'` méretű darabot olvas ki és egyszerűen dekódolja (nem `unpack`-el).

**Megjegyzés (nem hiba, csak csapda):** a `kor`/`ar` összehasonlítás (`cars[i][1] <= ask2`) **szöveges** (lexikografikus) összehasonlítás, mivel az autó-adatok argv-ből string-ként jönnek és nincs `int()`-esítve – ez többjegyű számoknál (pl. `"9"` vs `"10"`) helytelen sorrendet adhat, de mivel az adott `vasarlo.py`/`autokereskedes.py` pár konzisztensen ugyanezt a logikát használja, a teszt lefut vele.

**Adott + Megoldás együtt (ez a variáns már kész, futásra kész pár):**

```python
# vasarlo.py – teszt kliens
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import struct

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    data = ("kor".encode(), "1".encode())
    #data = ("tipus".encode(), "k".encode())

    client.sendall(packer.pack(*data))

    data = client.recv(packer2.size)
    print(data)
    res = data.decode()
    #cars = res[0].decode().replace('\x00','')
    print("Lekért adat: ", res)
```

```python
# autokereskedes.py – Megoldás (1,2,3 variáns)
import builtins
from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select
import sys
import random

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)
server_addr1 = ('localhost', 10001)
server_addr2 = ('localhost', 10002)

build = sys.argv[1:]

cars = {}
for i in range(len(build) // 3):
	cars[i] = (build[i*3],build[i*3+1],build[i*3+2])

print(cars)
print(len(cars))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    inputs = [ server ]
    while True:

        readable, writable, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                print('Vásárló érkezett')
            else:
                try:
                    data = s.recv(packer.size)
                    req = packer.unpack(data)

                    ask1 = req[0].decode().replace('\x00','')
                    ask2 = req[1].decode().replace('\x00','')
                    print("Vásárló kérése: ", ask1)
                    print("Adat: ", ask2)

                    res = ""
                    if ask1 == "tipus":
                        for i in range(len(cars)):
                            if cars[i][0] == ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    elif ask1 == "kor":
                        for i in range(len(cars)):
                            if cars[i][1] <= ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    elif ask1 == "ar":
                        for i in range(len(cars)):
                            if cars[i][2] <= ask2:
                                res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
                    print('Kérésre válasz:', res)
                    s.send(res.encode())
                except timeout:
                    pass
                except struct.error:
                    inputs.remove(s)
```

### 6.3.2 `PotZH/4/` – két UDP adatbázis közötti routing (hibás/hiányos piszkozat)

**Mi változott a `1,2,3` variánshoz képest:** az `autokereskedes.py` fejrésze (importok, `packer`/`packer2`, portok, a `cars` felépítése, a `select`-ciklus kerete) **szó szerint azonos** a `1,2,3` variánséval, és a két extra port (`server_addr1` = `('localhost', 10001)`, `server_addr2` = `('localhost', 10002)`) már ott is megvolt, csak kihasználatlanul. A különbség csak a `readable` ág belsejében van: a teljes `tipus`/`kor`/`ar` elágazás **el van véve**, helyette egy törött, routingolni próbáló töredék maradt:

```python
try:
    if client_addr % 2 == 0:

    elif client_addr % 2 == 1:

except timeout:
    pass
```

Ez így **szintaktikailag hibás** (üres `if`/`elif` test – Python ezt nem fogadja el), és `client_addr` egy `(host, port)` **tuple**, amin a `%` operátor nem is értelmezhető közvetlenül (csak pl. `client_addr[1] % 2`-ként). Ez a töredék azt a szándékot sugallja, hogy a vásárló TCP-kapcsolatát valamilyen szabály alapján a két új UDP "adatbázis-szerver" (`DB1.py`, 10001-es port / `DB2.py`, 10002-es port) közül az egyikhez kell irányítani.

A `vasarlo.py` (4) fejrésze is azonos a `1,2,3` variánséval, de a 12. sorban hibás tuple-szétbontás van:

```python
data, client = ("kor".encode(), "1".encode())   # BUG: felülírja a "client" socketet b"1"-re!
```

Ez a `DB1.py`/`DB2.py` `data, client = server.recvfrom(1024)` mintájának nyilvánvaló copy-paste-je: itt viszont a kliens TCP socketjét tárolja a `client` név (a `with socket(...) as client:` miatt), és ez a sor **felülírja** azt a bájtsztring `b"1"`-gyel, így a következő sor (`client.sendall(...)`) `AttributeError`-ral elhasalna, mert `bytes`-nak nincs `sendall` metódusa.

A `DB1.py` és `DB2.py` egy közös, de hibás sablont követ: mindkettő egy "Hello client!" UDP kézfogással kezd (fogad egy üzenetet, visszaköszön), majd a tényleges `tipus`/`kor`/`ar` lekérdezést próbálja feldolgozni – de:
- **sehol** nincs `import struct`, `import sys`, sem a `packer`/`packer2` Struct, sem a `cars` adatbázis felépítve (nincs argv-feldolgozás, mint az `autokereskedes.py`-ban);
- `DB1.py` a `packer.unpack(data)`-t hívja (`packer` nincs definiálva → `NameError`), majd a válasznál `s.send(...)`-et hív, de `s` sosincs definiálva (a socket neve `server`) – ráadásul UDP-n `send` (kapcsolat nélkül) nem is működne, `sendto` kellene;
- `DB2.py` ehelyett `req = data.decode()`-ot hív, majd `req[0]`, `req[1]`-et indexeli – de ez a dekódolt **string karaktereit** indexeli, nem a két mezőt (`ask1`/`ask2`) különíti el, tehát értelmetlen eredményt adna; a válasznál helyesen `server.sendto(res.encode(), client)`-et hív, ami ebben a párban az egyetlen hibátlan sor.

**Mivel a forrás hiányos és egymásnak ellentmondó (a routing-szabály és az adatbetöltés sincs megírva), az alábbi feladatleírás feltételezett/visszafejtett feladatleírás, mert a forrás hiányos és hibás volt.** A `vasarlo.py` működő lekérdezési logikájából (mezőnév + érték, `'10s 10s'` kérés, `'32s'` válasz) és a `DB1.py`/`DB2.py`-ban duplikált autó-szűrő logikából (tipus==, kor<=, ar<=, `|`-tal elválasztott eredmény) a legjobb visszafejtésünk szerint a feladat egy **TCP→UDP proxy/kereskedés**: az `autokereskedes.py` a vásárlóktól TCP-n fogadja a `'10s 10s'` kérést, ezt egy "Hello client!" UDP-kézfogással bevezetett kéréssel továbbítja az egyik UDP adatbázis-szervernek (`DB1` vagy `DB2`), majd a kapott választ visszaadja a vásárlónak.

Mivel a pontos routingszabály nem rekonstruálható egyértelműen, **két plauzibilis megoldást** adunk:

- **Variáns A – portparitás alapú terheléselosztás** (ez illeszkedik legjobban a megmaradt `client_addr % 2` töredékhez): a vásárló TCP-kapcsolatának forrásportja (`client_addr[1]`) dönti el, hogy `DB1`-hez vagy `DB2`-höz menjen a kérés – egyszerű round-robin/load-balancing proxy, a két DB-nek ugyanaz az adatbázisa van.
- **Variáns B – tartalom alapú (kérés szerinti) routing**: a kérés `ask1` mezője (a lekérdezett tulajdonság: `"tipus"`, `"kor"` vagy `"ar"`) dönti el, melyik DB-hez menjen a kérés (pl. `"tipus"` → `DB1`, `"kor"`/`"ar"` → `DB2`) – ekkor a két DB-nek különböző (vagy felosztott) autó-adatbázisa lehet.

Mindkét variánshoz javítjuk a nyilvánvaló hibákat: hiányzó `import struct`/`import sys`, hiányzó `packer`/`cars` a DB-kben, az értelmetlen `s.send`/`req[0]` sorokat, és a `vasarlo.py` tuple-szétbontási hibáját.

**Teszt/adott fájlok (eredeti, hibás állapotukban):**

```python
# autokereskedes.py (4) – adott, hibás/hiányos
import builtins
from socket import socket,AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select
import sys
import random

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)
server_addr1 = ('localhost', 10001)
server_addr2 = ('localhost', 10002)

build = sys.argv[1:]

cars = {}
for i in range(len(build) // 3):
	cars[i] = (build[i*3],build[i*3+1],build[i*3+2])

print(cars)
print(len(cars))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    inputs = [ server ]
    while True:

        readable, writable, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                print('Vásárló érkezett')
            else:
                try:
                    if client_addr % 2 == 0:

                    elif client_addr % 2 == 1:

                except timeout:
                    pass
                except struct.error:
                    inputs.remove(s)
```

```python
# vasarlo.py (4) – adott, hibás (tuple-szétbontási bug a 12. sorban)
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import struct

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)


with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    data, client = ("kor".encode(), "1".encode())
    #data = ("tipus".encode(), "k".encode())

    client.sendall(packer.pack(*data))

    data = client.recv(packer2.size)
    print(data)
    res = data.decode()
    #cars = res[0].decode().replace('\x00','')
    print("Lekért adat: ", res)
```

```python
# DB1.py – adott, hiányos (nincs import struct, packer, cars; s.send nem létező socketen)
from socket import socket, AF_INET, SOCK_DGRAM, timeout

with socket(AF_INET, SOCK_DGRAM) as server:
  server_address = ('localhost', 10001)

  server.bind(server_address)
  server.settimeout(1.0)

  while True:
    try:
      data, client = server.recvfrom(1024)
      print("Received:", data.decode(), "From:", client)
      server.sendto("Hello client!".encode(), client)

      data, client = server.recvfrom(1024)
      req = packer.unpack(data)

      ask1 = req[0].decode().replace('\x00','')
      ask2 = req[1].decode().replace('\x00','')
      print("Vásárló kérése: ", ask1)
      print("Adat: ", ask2)

      res = ""
      if ask1 == "tipus":
          for i in range(len(cars)):
              if cars[i][0] == ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "kor":
          for i in range(len(cars)):
              if cars[i][1] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "ar":
          for i in range(len(cars)):
              if cars[i][2] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      print('Kérésre válasz:', res)
      s.send(res.encode())
    except timeout:
      pass
```

```python
# DB2.py – adott, hiányos (nincs import struct, packer, cars; req[0]/req[1] karakterindexelés, nem mezőszétválasztás)
from socket import socket, AF_INET, SOCK_DGRAM, timeout

with socket(AF_INET, SOCK_DGRAM) as server:
  server_address = ('localhost', 10002)

  server.bind(server_address)
  server.settimeout(1.0)

  while True:
    try:
      data, client = server.recvfrom(1024)
      print("Received:", data.decode(), "From:", client)
      server.sendto("Hello client!".encode(), client)

      data, client = server.recvfrom(1024)
      req = data.decode()

      ask1 = req[0].decode().replace('\x00','')
      ask2 = req[1].decode().replace('\x00','')
      print("Vásárló kérése: ", ask1)
      print("Adat: ", ask2)

      res = ""
      if ask1 == "tipus":
          for i in range(len(cars)):
              if cars[i][0] == ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "kor":
          for i in range(len(cars)):
              if cars[i][1] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      elif ask1 == "ar":
          for i in range(len(cars)):
              if cars[i][2] <= ask2:
                  res = res + cars[i][0] + " " + cars[i][1] + " "  + cars[i][2] + "|"
      print('Kérésre válasz:', res)
      server.sendto(res.encode(), client)
    except timeout:
      pass
```

**Javított teszt kliens (a `vasarlo.py` (4) 12. sorának hibáját javítva, hogy egyáltalán tesztelhető legyen):**

```python
# vasarlo.py (4) – javítva
from socket import socket, AF_INET, SOCK_STREAM
import struct

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    data = ("kor".encode(), "1".encode())
    # data = ("tipus".encode(), "k".encode())

    client.sendall(packer.pack(*data))

    adat = client.recv(packer2.size)
    res = adat.decode().replace('\x00', '')
    print("Lekért adat: ", res)
```

**Megoldás – Variáns A (portparitás alapú load-balancing proxy, DB1/DB2 azonos adatbázissal):**

Az `autokereskedes.py` ebben a variánsban nem tárol maga autókat: a 10001/10002-es UDP adatbázis-szerverek mindketten megkapják ugyanazt az autó-listát argumentumként, és az `autokereskedes.py` csak továbbít a kettő között, a vásárló TCP forrásportjának paritása szerint.

```python
# autokereskedes.py – Megoldás, Variáns A
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)
db_addrs = [('localhost', 10001), ('localhost', 10002)]   # DB1, DB2

with socket(AF_INET, SOCK_STREAM) as server, socket(AF_INET, SOCK_DGRAM) as db:
    db.settimeout(2.0)
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    inputs = [server]
    while True:
        readable, _, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                client.setblocking(True)
                # a kliens socket-hez tároljuk, melyik DB-hez tartozik (forrásport paritása)
                client._db_addr = db_addrs[client_addr[1] % 2]
                print('Vásárló érkezett', client_addr, '->', client._db_addr)
                continue
            try:
                data = s.recv(packer.size)
                if not data:
                    inputs.remove(s)
                    s.close()
                    continue

                target = s._db_addr

                # "Hello client!" kézfogás a kiválasztott DB-vel
                db.sendto(b"HELLO", target)
                db.recvfrom(1024)   # "Hello client!" válasz, eldobható

                db.sendto(data, target)
                valasz, _ = db.recvfrom(packer2.size)

                s.sendall(valasz)
            except timeout:
                pass
            except struct.error:
                inputs.remove(s)
```

```python
# DB1.py – Megoldás (Variáns A, ugyanaz a logika, mint DB2)
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct
import sys

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')

build = sys.argv[1:]
cars = {}
for i in range(len(build) // 3):
    cars[i] = (build[i * 3], build[i * 3 + 1], build[i * 3 + 2])

with socket(AF_INET, SOCK_DGRAM) as server:
    server_address = ('localhost', 10001)
    server.bind(server_address)
    server.settimeout(5.0)

    while True:
        try:
            data, client = server.recvfrom(1024)
            print("Received:", data, "From:", client)
            server.sendto("Hello client!".encode(), client)

            data, client = server.recvfrom(1024)
            req = packer.unpack(data)

            ask1 = req[0].decode().replace('\x00', '')
            ask2 = req[1].decode().replace('\x00', '')
            print("Vásárló kérése: ", ask1, "Adat: ", ask2)

            res = ""
            if ask1 == "tipus":
                for i in range(len(cars)):
                    if cars[i][0] == ask2:
                        res = res + cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            elif ask1 == "kor":
                for i in range(len(cars)):
                    if cars[i][1] <= ask2:
                        res = res + cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            elif ask1 == "ar":
                for i in range(len(cars)):
                    if cars[i][2] <= ask2:
                        res = res + cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            print('Kérésre válasz:', res)
            server.sendto(res.encode(), client)
        except timeout:
            pass
```

```python
# DB2.py – Megoldás (Variáns A, csak a port más: 10002)
# ugyanaz, mint a fenti DB1.py, csak:
#   server_address = ('localhost', 10002)
```

**Megoldás – Variáns B (tartalom alapú routing: a kért mező dönt, a két DB különböző adatbázist tárol):**

Itt az `autokereskedes.py` a `vasarlo.py` kérésének `ask1` mezőjét (a nem-becsomagolt első 10 bájtot) olvassa ki routingdöntéshez, mielőtt a teljes csomagot továbbítaná – pl. `"tipus"` kérdés a `DB1`-hez (ami a hazai autókat tárolja), `"kor"`/`"ar"` kérdés a `DB2`-hez (ami az egész adatbázist tárolja és bármelyik mezőre tud válaszolni) megy.

```python
# autokereskedes.py – Megoldás, Variáns B
from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import select

packer = struct.Struct('10s 10s')
packer2 = struct.Struct('32s')
server_addr = ('localhost', 10000)
DB1_ADDR = ('localhost', 10001)
DB2_ADDR = ('localhost', 10002)

with socket(AF_INET, SOCK_STREAM) as server, socket(AF_INET, SOCK_DGRAM) as db:
    db.settimeout(2.0)
    server.bind(server_addr)
    server.listen(1)
    server.settimeout(1.0)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    inputs = [server]
    while True:
        readable, _, exceptional = select.select(inputs, [], inputs, 1)

        for s in readable:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
                print('Vásárló érkezett', client_addr)
                continue
            try:
                data = s.recv(packer.size)
                if not data:
                    inputs.remove(s)
                    s.close()
                    continue

                ask1, _ = packer.unpack(data)
                ask1 = ask1.decode().replace('\x00', '')

                # tartalom alapú routing: a kért mező dönt, melyik DB-hez menjen a kérés
                target = DB1_ADDR if ask1 == "tipus" else DB2_ADDR

                db.sendto(b"HELLO", target)
                db.recvfrom(1024)   # "Hello client!" kézfogás

                db.sendto(data, target)
                valasz, _ = db.recvfrom(packer2.size)

                s.sendall(valasz)
            except timeout:
                pass
            except struct.error:
                inputs.remove(s)
```

```python
# DB1.py – Megoldás (Variáns B, pl. csak a "tipus" szerinti kérdésekre kap forgalmat)
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct
import sys

packer = struct.Struct('10s 10s')

build = sys.argv[1:]
cars = {}
for i in range(len(build) // 3):
    cars[i] = (build[i * 3], build[i * 3 + 1], build[i * 3 + 2])

with socket(AF_INET, SOCK_DGRAM) as server:
    server.bind(('localhost', 10001))
    server.settimeout(5.0)

    while True:
        try:
            data, client = server.recvfrom(1024)
            server.sendto("Hello client!".encode(), client)

            data, client = server.recvfrom(1024)
            ask1, ask2 = packer.unpack(data)
            ask1 = ask1.decode().replace('\x00', '')
            ask2 = ask2.decode().replace('\x00', '')

            res = ""
            if ask1 == "tipus":
                for i in range(len(cars)):
                    if cars[i][0] == ask2:
                        res += cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            server.sendto(res.encode(), client)
        except timeout:
            pass
```

```python
# DB2.py – Megoldás (Variáns B, a "kor" és "ar" kérdésekre válaszol)
from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct
import sys

packer = struct.Struct('10s 10s')

build = sys.argv[1:]
cars = {}
for i in range(len(build) // 3):
    cars[i] = (build[i * 3], build[i * 3 + 1], build[i * 3 + 2])

with socket(AF_INET, SOCK_DGRAM) as server:
    server.bind(('localhost', 10002))
    server.settimeout(5.0)

    while True:
        try:
            data, client = server.recvfrom(1024)
            server.sendto("Hello client!".encode(), client)

            data, client = server.recvfrom(1024)
            ask1, ask2 = packer.unpack(data)
            ask1 = ask1.decode().replace('\x00', '')
            ask2 = ask2.decode().replace('\x00', '')

            res = ""
            if ask1 == "kor":
                for i in range(len(cars)):
                    if cars[i][1] <= ask2:
                        res += cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            elif ask1 == "ar":
                for i in range(len(cars)):
                    if cars[i][2] <= ask2:
                        res += cars[i][0] + " " + cars[i][1] + " " + cars[i][2] + "|"
            server.sendto(res.encode(), client)
        except timeout:
            pass
```

---

## Záró megjegyzés — mire kell a ZH-n koncentrálni

A teljes anyag egyetlen visszatérő mintasorra épül:

1. **TCP kliens** – `create_connection`, `sendall(Struct.pack(...))`, `recv_exact(sock, méret)`, `Struct.unpack(...)`.
2. **UDP kliens** – `socket(SOCK_DGRAM)`, `sendto`, `recvfrom(1024)`, `settimeout`.
3. **TCP szerver `select`-tel** – `inputs = [server]` a ciklus előtt, `select.select(inputs, [], [], 1.0)`, új kliens vs. meglévő kliens ága, bontás kezelése (`inputs.remove(s)`), közös állapot a ciklus előtt.
4. **UDP szerver** – `bind`, `recvfrom`/`sendto` ciklusban, válasz a feladó címére.
5. **Proxy (TCP → UDP vagy TCP → TCP)** – egy "elöl" `select`-es TCP szerver + egy "hátul" UDP/TCP kliens-kapcsolat, parancs-átfordítással (szótár) és válasz-továbbítással.

A `zh/` mappa (1. fejezet) tartalmazza a **valódi vizsgafeladatokat** ebben a sémában (járatfoglalás = minta #1+#5 kombinációja, raktárkészlet = minta #3, azonosítási proxy = minta #5 proxy-változata), a többi mappa pedig ugyanezen minták gyakorlására szolgáló, egyre bővülő feladatkészlet.
