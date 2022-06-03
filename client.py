import socket

header = 1024
port = 1234
format = 'utf-8'
disconnect_msg = "0"
server = socket.gethostbyname(socket.gethostname())
addr = (server, port)
logged_in = False

starting_menu = """Witaj w Banku S & F co moge dla ciebie zrobic?:
    0 - Wyjscie
    1 - Zaloguj sie
    2 - Rejestracja
    """

clients_menu = """Prosze wybierz operacje:
    0 - Rozłącz
    1 - Zasil konto
    2 - Wypłać środki
    3 - Przelew na inne konto
    4 - Stan konta 
    menu - Ponownie wyświetla dostępne opcje
    """

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(addr)


def send(msg):
    message = msg.encode(format)
    msg_length = len(message)
    send_length = str(msg_length).encode(format)
    send_length += b' ' * (header - len(send_length))
    client.send(send_length)
    client.send(message)
    msg_server = client.recv(2048).decode(format)
    print(msg_server)
    if msg_server == "Zalogowano!":
        print(clients_menu)


disconnect = False
print(starting_menu)

while not disconnect:
    msg = input(">>>:")
    if msg == "0":
        disconnect = True
        print(f"Dowidzenia!")
    elif msg == "menu":
        print(clients_menu)
    else:
        send(msg)

send(disconnect_msg)