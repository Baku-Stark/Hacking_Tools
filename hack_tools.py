import os
from services import Colors, CurrentTime, OperationalSys

from tools import Port_Scanner, Ip_Address, Connection

class HackTools:
    def __init__(self) -> None:
        self.__menu()
        self.__menu_choice()

    @classmethod
    def __menu(cls):
        title = open("services/title.txt", "r", encoding="utf-8")
        print("=" * 50)
        print(Colors.CYAN + title.read() + Colors.END)
        print(Colors.BLUE + "\n- Author: Baku-Stark" + Colors.END)
        print("=" * 50)
        title.close()

    @classmethod
    def __menu_choice(cls):
        """
        Menu Choice
        """
        options = [Ip_Address.__name__, Port_Scanner.__name__, Connection.__name__]
        
        while True:
            for ind_, op in enumerate(options):
                print(f"[ {ind_ + 1} ] {op}")
            print(f"[ {len(options)+1} + ] Exit")
            print('\n')

            try:
                choice = int(input(f"[{__class__.__name__}] Choice a number: "))

            except ValueError as v_error:
                print(Colors.RED + f"[{cls.__name__}] : {v_error}" + Colors.END)
                print("=" * 50)

            else:
                match choice:
                    case 1:
                        print(f"└── Your choice : {options[choice-1]}")
                        print(Colors.PURPLE + Ip_Address.__doc__ + Colors.END)
                        print('\n')

                        ip_ad = str(input(f"[{options[choice-1]}] Type a IP ADRESS >: "))
                        Ip_Address.ip_v4(ip_ad)
                        print('\n' * 2)
                        print("=" * 50)

                    case 2:
                        print(f"└── Your choice : {options[choice-1]}")
                        print(Colors.PURPLE + Port_Scanner.__doc__ + Colors.END)
                        print('\n')

                        host = str(input(f"[{options[choice-1]}] Type a HOST >: "))
                        Port_Scanner(host).start()
                        print('\n' * 2)
                        print("=" * 50)

                    case 3:
                        print(f"└── Your choice : {options[choice-1]}")
                        print(Colors.PURPLE + Connection.__doc__ + Colors.END)
                        print('\n')

                        url_site = str(input(f"[{options[choice-1]}] URL Site >: "))
                        Connection.ip_address_hostname(url_site)
                        print('\n' * 2)
                        print("=" * 50)

                    case _:
                        print("** BYE! **")
                        break

OperationalSys.clean_console()
HackTools() if __name__ == '__main__' else None