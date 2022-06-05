Witam w projekcie applikacji bankowej autorstwa Filipa Ostrowskiego i Szymona Jankowskiego.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
URUCHAMIANIE

1. Na początek należy odpalić server.py

2. Następnie w zależności czy zamierzasz uruchomić client.py na tym samym komputerze lub innym należy ustawić w pliku client.py wartość "server" na adres ip servera.
   Domyślnie client.py będzie brał jako adres servera adres komputera na którym został uruchomiony.

3. Po uruchomieniu client.py można stowrzyć nowego użytkownika lub użyć już istniejących - dane konta można podejrzeć w aplikacji bankier.py

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ZAŁOŻENIA

Każde konto klienta ma osobny plik w folderze "accounts".

Dla zwiększenia czytelności kodu server.py oraz bankier.py używają napisanych przez nas funkcji znajdujących się w funckje.py.

Każde nowe połączenie do servera tworzy nowy wątek, w którym przeprowadzana jest dalsza logika kodu.


