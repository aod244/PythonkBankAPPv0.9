import pickle, random
import os.path

HEADER = 1024
PORT = 1234

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "Rozlacz"

#FUNKCJE
def save_to_file(account_data, account_nr):
    account_file = open(f"accounts\{account_nr}.pkl", "wb")
    pickle.dump(account_data, account_file)
    account_file.close()

def get_file_content(account_nr):
    account_file = open(f"accounts\{account_nr}.pkl", "rb")
    output = pickle.load(account_file)
    account_file.close()
    return output

#Funckja przyjmuje data klienta i tworzy pliczek z nazwą numeru konta
def create_account(name, surname, password, pesel, account_nr, balance):
    account_data = {"name": name, "surname": surname, "hasło": password, "pesel": pesel, "balance": balance}
    save_to_file(account_data, account_nr)


def register(name, surname, password, pesel, balance):
    client_number = random.randint(10000, 100000)
    while os.path.isfile(f"accounts\{client_number}.pkl"):
        client_number = random.randint(10000, 100000)
    create_account(name, surname, password, pesel, client_number, balance)
    return client_number

def login(account_nr, password):
    if os.path.isfile(f"accounts\{account_nr}.pkl"):
        data_from_file = get_file_content(account_nr)
        if data_from_file["hasło"] == password:
            return "Zalogowano!"
        else:
            return "Błedne hasło!"
    else:
        return "Blędny numer klienta"

def check_balance(account_nr):
    data = get_file_content(account_nr)
    balance = data["balance"]
    return balance

def charge(account_nr, charge_amount):
    data = get_file_content(account_nr)
    charge_amount = int(charge_amount)
    present_balance = int(data["balance"])
    if charge_amount > 0:
        data = get_file_content(account_nr)
        present_balance += charge_amount
        data["balance"] = present_balance
        save_to_file(data, account_nr)
        return "Konto zostało zasilone"
    else:
        return "Kwota zasilenia jest za niska, proszę sprobuj ponownie z inną kwotą"

def withdrawal(account_nr, withdrawal_amount):
    data = get_file_content(account_nr)
    present_balance = int(data["balance"])
    withdrawal_amount = int(withdrawal_amount)
    if withdrawal_amount <= present_balance and withdrawal_amount > 0:
        data["balance"] -= withdrawal_amount
        save_to_file(data, account_nr)
        return "Srodki zostały wypłacone"
    elif present_balance < withdrawal_amount:
        return "Brak wystarczajacych srodkow na koncie"
    else:
        return "Nie można wypłacić ujemnych środków"

def transfer(sender_account_nr, receiver_account_nr, amount):
    if receiver_account_nr != sender_account_nr:
        data = get_file_content(sender_account_nr)
        balance = int(data["balance"])
        amount = int(amount)
        if balance >= amount:
            if os.path.isfile(f"accounts\{receiver_account_nr}.pkl"):
                receiver_data = get_file_content(receiver_account_nr)
                receiver_balance = int(receiver_data["balance"])
                data["balance"] = balance - amount
                receiver_data["balance"] = amount + receiver_balance
                save_to_file(data, sender_account_nr)
                save_to_file(receiver_data, receiver_account_nr)
                return "transfer został wykonany, możesz ponownie wybrać operacje."
            else:
                return "Odbiorca nie istnieje, możesz ponownie wybrać operacje."
        else:
            return "Niewystarczajace srodki na koncie, możesz ponownie wybrać operacje."
    else:
        return "Nie mozesz wyslac pieniedzy na swoje konto"

def receive_message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg