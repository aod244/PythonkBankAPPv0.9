import socket
from funkcje import *
import threading

header = 1024
port = 1234
SERVER = socket.gethostbyname(socket.gethostname())
addr = (SERVER, port)
format = 'utf-8'
disconnect_msg = "0"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)


def login_dialog(conn):
    conn.send("Podaj nr konta do logowania: ".encode(format))
    account_number = receive_message(conn)

    conn.send("Podaj hasło: ".encode(format))
    password = receive_message(conn)
    return account_number, password


def client(conn, addr):
    print(f"[NOWE POLACZENIE Z:] {addr}")

    connected = True
    while connected:
        msg = receive_message(conn)
        if msg == disconnect_msg:
            connected = False

        print(f"[{addr}] {msg}")
        ###!!!Important news - zmieniłem funkcje by zapisywały dane i towrzyły konta w folderze "accounts", jeśli nie znajdą takiego folderu to wywali błąd
        if msg == "1":
            print(f"[{addr}] Klient wybral logowanie.")
            account_number, password = login_dialog(conn)
            login_result = login(account_number, password)
            conn.send(login_result.encode(format))
            if login_result == "Zalogowano!":
                print(f"[{addr}] Klient sie zalogowal na nr: {account_number}.")
                while msg != disconnect_msg:
                    msg = receive_message(conn)
                    if msg == "0":
                        pass
                    elif msg == "1":
                        print(f"[{addr}] {account_number} wybral wplate na konto.")
                        conn.send("Proszę podaj kwotę zasilenia".encode(format))
                        msg = receive_message(conn)
                        charge_amount = int(msg)
                        msg_to_client = charge(account_number, charge_amount) + ". Mozesz wybrać kolejną operację (1-5)"
                        conn.send(msg_to_client.encode(format))
                        print(f"[{addr}] {account_number} zasilil konto kwota {charge_amount}")
                    elif msg == "2":
                        print(f"[{addr}] {account_number} wybral wyplate srodkow.")
                        conn.send("Proszę podaj kwotę wypłaty: ".encode((format)))
                        withdrawal_amount = receive_message(conn)
                        msg_to_client = withdrawal(account_number, withdrawal_amount)
                        conn.send(f"{msg_to_client}".encode(format))
                        if msg_to_client == "Srodki zostały wypłacone":
                            print(f"[{addr}] {account_number} wyplacil z konta {withdrawal_amount}")
                        else:
                            print(f"[{addr}] {account_number} popelnil blad podczas operacji, operacja anulowana")
                    elif msg == "3":
                        print(f"[{addr}] {account_number} wybral przelew na inne konto.")
                        conn.send("Proszę podaj numer konta na które chcesz przelać środki: ".encode(format))
                        receiver_account_number = receive_message(conn)
                        conn.send("Proszę podaj kwotę przelewu: ".encode(format))
                        transfer_amount = receive_message(conn)
                        msg_to_client = transfer(account_number, receiver_account_number, transfer_amount)
                        conn.send(msg_to_client.encode(format))
                        print(f"[{addr}] {account_number} przelal {transfer_amount} na konto {receiver_account_number}")
                    elif msg == "4":
                        conn.send(f"Twoje saldo to: {check_balance(account_number)}".encode(format))
                        balance = check_balance(account_number)
                        print(f"[{addr}] {account_number} sprawdzil saldo, ktore wynosi: {balance}")
                    else:
                        print(f"[{addr}] {account_number} wybral bledna opcje.")
                        conn.send(f"Wybrano bledna opcje, wpisz menu aby wyswietlic dostepne opcje".encode(format))

        if msg == "2":
            print(f"[{addr}] Klient wybral rejestracje.")
            conn.send("Podaj: Imie, Nazwisko, password, Pesel, Kwote pierwszej wplaty: (przecinek spacja po kazdej zmiennej)".encode(format))
            registration_data = receive_message(conn)
            print(f"[{addr}] Klient wprowadzil nastepujace dane: ")
            print(registration_data)  
            split_registration_data = registration_data.split(", ")
            if len(split_registration_data) != 5:
                print(f"[{addr}] Klient nie wpełnił formularza rejestracji poprawnie")
                conn.send("Wszystkie pola są obowiązkowe, konto nie zostało utworzone. Proszę wybierz ponownie operacje (0-2)".encode(format))
            else:
                client_number = register(split_registration_data[0], split_registration_data[1], split_registration_data[2], split_registration_data[3], split_registration_data[4],)
                conn.send(f"Twoj numer klienta: {client_number}. Wpisz 1 zeby sie zalogowac".encode(format))
                print(f"[{addr}] Klient po rejestracji dostal nastepujacy nr konta: {client_number}")
        else:
            print(f"[{addr}] Klient sie rozlaczyl.")

    conn.close()
    print(f"[Liczba aktywnych klientow] {(threading.activeCount() - 1) - 1}")


def start():
    server.listen()
    print(f"[SERWER NASLUCHUJE NA:] {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client, args=(conn, addr))
        thread.start()
        print(f"[Liczba aktywnych klientow] {threading.activeCount() - 1}")


start()
