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
