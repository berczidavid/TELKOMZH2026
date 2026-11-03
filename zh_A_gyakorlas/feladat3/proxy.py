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
