import platform
from services import Colors, OperationalSys
from tools.email_validator import Email_Validator
from tools.port_scanner import Port_Scanner
from tools.connection import Connection, Ip_Address
from tools.crypt import Encryptor, Decryptor
from tools.password_generator import PasswordGenerator
from tools.whois_lookup import WhoisLookup

class HackTools:
    def __init__(self) -> None:
        self.title = self.load_title()
        self.options = {
            1: self.handle_ip_address,
            2: self.handle_port_scanner,
            3: self.handle_connection,
            4: self.handle_email_validator,
            5: self.handle_encryptor,
            6: self.handle_decryptor,
            7: self.handle_password_generator,
            8: self.handle_whois_lookup
        }
        self.run()

    def load_title(self):
        try:
            with open("services/title.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "HackTools"

    def show_menu(self):
        print("=" * 50)
        print(Colors.CYAN + self.title + Colors.END)
        print(Colors.BLUE + "\n- Author: Baku-Stark" + Colors.END)
        print(Colors.BLUE + "\n- Copyright | Baku-Stark" + Colors.END)
        print("=" * 50)
        print("\nAvailable Options:\n")

        for idx, func in self.options.items():
            print(f"[ {idx} ] {func.__name__.replace('handle_', '').replace('_', ' ').title()}")

        print(f"[ {len(self.options)+1} ] Exit")
        print("=" * 50)

    def run(self):
        while True:
            self.show_menu()

            try:
                choice = int(input(f"\n[{self.__class__.__name__}] Choose an option: "))
            except ValueError:
                print(Colors.RED + "[Error] Invalid input. Please enter a number." + Colors.END)
                continue

            if choice == len(self.options) + 1: # EXIT OPTION
                print(Colors.GREEN + "\nExiting HackTools. See you next time!" + Colors.END)
                break

            action = self.options.get(choice)
            if action:
                action()
            else:
                print(Colors.RED + "[Error] Invalid choice. Try again." + Colors.END)

    def handle_ip_address(self):
        print(Colors.PURPLE + Ip_Address.__doc__ + Colors.END)
        ip = input("\n[IP Address] Enter a valid IPv4 address: ").strip()

        if self.validate_ip(ip):
            Ip_Address.ip_v4(ip)
        else:
            print(Colors.RED + "[Error] Invalid IP format!" + Colors.END)

    def handle_port_scanner(self):
        print(Colors.PURPLE + Port_Scanner.__doc__ + Colors.END)
        host = input("\n[Port Scanner] Enter a host (IP or domain): ").strip()
        try:
            scanner = Port_Scanner(host)
            scanner.start()
        except Exception as e:
            print(Colors.RED + f"[Error] Failed to scan ports: {e}" + Colors.END)

    def handle_connection(self):
        print(Colors.PURPLE + Connection.__doc__ + Colors.END)
        url = input("\n[Connection] Enter a URL (without http/https): ").strip()

        if url:
            Connection.ping(url)
            Connection.ip_address_hostname(url)
        else:
            print(Colors.RED + "[Error] URL cannot be empty!" + Colors.END)

    def handle_email_validator(self):
        print(Colors.PURPLE + Email_Validator.__doc__ + Colors.END)
        email = input("\n[Email Validator] Enter an email address: ").strip()

        if email:
            Email_Validator.validate_email(email)
        else:
            print(Colors.RED + "[Error] Email cannot be empty!" + Colors.END)

    def handle_encryptor(self):
        print(Colors.PURPLE + Encryptor.__doc__ + Colors.END)
        user_text = input("\n[Encryptor] Enter text to encrypt: ").strip()

        if not user_text:
            print(Colors.RED + "[Error] Text cannot be empty!" + Colors.END)
            return

        aes_key = input("[Encryptor] Enter a key for AES encryption: ").strip()
        if not aes_key:
            print(Colors.RED + "[Error] Key is required for AES encryption!" + Colors.END)
            return

        # SHOW ALL CRYPT METHODS
        Encryptor.base64_encode(user_text)
        Encryptor.sha3_256_hash(user_text)
        Encryptor.aes_encrypt(user_text, aes_key)


    def handle_decryptor(self):
        print(Colors.PURPLE + Decryptor.__doc__ + Colors.END)
        user_text = input("\n[Decryptor] Enter AES encrypted (base64) text to decrypt: ").strip()
        if not user_text:
            return

        aes_key = input("[Decryptor] Enter the AES key used for encryption: ").strip()
        if not aes_key:
            print(Colors.RED + "[Error] AES key is required!" + Colors.END)
            return

        # AES decoding attempt
        Decryptor.aes_decrypt(user_text, aes_key)

        # Base64 decoding attempt
        decode_b64 = input("\n[Decryptor] Decode as Base64 too? (y/n): ").strip().lower()
        if decode_b64 == 'y':
            Decryptor.base64_decode(user_text)

    def handle_password_generator(self):
        print(Colors.PURPLE + PasswordGenerator.__doc__ + Colors.END)
        level = str(input("Password Level (Use: simple, medium or strong): ")).strip().lower()
        
        try:
            length = int(input("Type password lenght: "))
        except ValueError:
                print(Colors.RED + "[Error] Invalid Length!" + Colors.END)

        PasswordGenerator.generate(level, length)

    def handle_whois_lookup(self):
        print(Colors.PURPLE + WhoisLookup.__doc__ + Colors.END)
        domains = input("\n[Whois Lookup] Enter domains or IPs (space-separated): ").strip()

        if not domains:
            print(Colors.RED + "[Error] Input cannot be empty!" + Colors.END)
            return

        save_path = input("[Whois Lookup] Enter path to save results (blank = ~/HackingTool_WhoisLookup): ").strip()
        export_json = input("[Whois Lookup] Export as JSON? (y/n): ").strip().lower() == 'y'

        domain_list = domains.split()
        WhoisLookup.batch_lookup(domain_list, save_path, export_json)


    @staticmethod
    def validate_ip(ip):
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for item in parts:
            if not item.isdigit():
                return False
            num = int(item)
            if num < 0 or num > 255:
                return False
        return True

# Clear console on start
OperationalSys.clean_console()

if __name__ == "__main__":
    try:
        if platform.system().lower() == 'linux':
            HackTools()
        else:
            print(Colors.RED + f"Unsupported system: {platform.system()}" + Colors.END)

    except KeyboardInterrupt:
        print(Colors.RED + "\n[!] KeyboardInterrupt detected. Exiting..." + Colors.END)

    finally:
        print(Colors.BLUE + "\n** BYE! **" + Colors.END)