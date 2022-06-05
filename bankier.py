from funkcje import *
import os.path

main_menu = """
1 - Stworz użytkownika
2 - Edytuj istniejącego użytkownika
3 - Sprawdz dane konta
4 - Zamknij aplikacje

"""

continue_connection = True

available_options = ["name", "surname", "password", "pesel", "balance"]

print("Witaj w aplikacji Bankiera, proszę wybierz jedną z poniższych operacji: ")
while continue_connection:
    choice = input(main_menu).lower()
    if choice == "1":
        data = input("Podaj: Imie, Nazwisko, hasło, pesel, kwote pierwszej wplaty: (przecinek spacja po kazdej zmiennej): \n").split(", ")
        if len(data) != 5:
            print("Niewłaściwa ilość danych, konto nie zostało utworzone.")
        else:
            new_client_nr = register(data[0],data[1],data[2],data[3],data[4])
            print(f"Użytkownik stworzony pomyślnie! Jego numer klienta to: {new_client_nr}")
    elif choice == "2":
        client_nr = input("Proszę podaj numer klienta, którego dane chcesz edytować: ")
        if os.path.isfile(f"accounts\{client_nr}.pkl"):
            data_to_change = ""
            while data_to_change != "0":
                data_to_change = input("Proszę wybierz wartość którą chcesz zmienić - name, surname, password, pesel, balance (możesz wybrać tylko jedną opcję na raz, wciśnij 0 jeśli chcesz wrócić do poprzedniego menu)\n").lower()
                if data_to_change in available_options:
                    account_data = get_file_content(client_nr)
                    account_data[data_to_change] = input(f"""Obecna wartość: {account_data[data_to_change]}
Proszę podaj nową wartość: """)
                    print(f"Operacja zakończona powodzeniem, nowa wartość to: {account_data[data_to_change]}")
                elif not data_to_change in available_options and data_to_change != "0":
                    print("Nie właściwy wybór... Operacja zakończona niepowodzeniem.")
        else:
            print("Podany numer konta nie istnieje w naszej bazie danych.")
    elif choice == "3":
        account_number = input("Proszę podaj numer konta użytkownika: ")
        if os.path.isfile(f"accounts{account_number}.pkl"):
            dane = get_file_content(account_number)
            for element in dane:
                print(f"{element} = {dane[element]}")
        else:
            print("Wybrane konto nie istnieje...")
        
    elif choice == "4":
        print("Aplikacja się zamyka, dziękuję za skorzystanie z naszych usług!")
        continue_connection = False
    else:
        print("Została wybrana niewłaściwa opcja, proszę wybierz ponownie.")