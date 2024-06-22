import requests
import subprocess
import concurrent.futures

from socket import *

from services import Colors, CurrentTime

class Connection:
    """
    HackTools -> Connection | Tool to get the IP address information.
    """

    @staticmethod
    def ip_address_hostname(url_site : str = "www.stackoverflow.com"):
        try:
            response = gethostbyname_ex(url_site)

        except gaierror as error_ip:
            print(Colors.RED + f"[{__name__} - {__class__.__name__}] : {error_ip}" + Colors.END)

        else:
            print(
            f"""
                ● INFO ({url_site}):
            +----------------- x ----------------
            | Hostname: {response[0]}            
            | IP: {response[2]}
            +----------------- x ----------------
            """
            )

    @staticmethod
    def ping(url : str = "www.stackoverflow.com"):
        try:
            print(Colors.BLUE + "[-] Wait a few seconds (or minutes) for the analysis..." + Colors.END)
            output = subprocess.Popen(["ping", "-c", "4", url], stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()

        except subprocess.CalledProcessError:
            print(Colors.RED + f"[{__name__} - {__class__.__name__}] : {subprocess.CalledProcessError}" + Colors.END)
        
        else:
            #PING www.stackoverflow.com (172.64.155.249) 56(84) bytes of data.\n64 bytes from 172.64.155.249 (172.64.155.249): icmp_seq=1 ttl=60 time=9.86 ms\n64 bytes from 172.64.155.249 (172.64.155.249): icmp_seq=2 ttl=60 time=12.6 ms\n64 bytes from 172.64.155.249 (172.64.155.249): icmp_seq=3 ttl=60 time=13.9 ms\n64 bytes from 172.64.155.249 (172.64.155.249): icmp_seq=4 ttl=60 time=10.9 ms\n\n--- www.stackoverflow.com ping statistics ---\n4 packets transmitted, 4 received, 0% packet loss, time 3004ms\nrtt min/avg/max/mdev = 9.864/11.792/13.877/1.544 ms\n'
            res = str(output[0])[2:-1].split('\\n')

            for i in res:
                print(i)

class Ip_Address:
    """
    HackTools -> Ip_Address | Tool to get the IP address information.
    """
    
    @staticmethod
    def ip_v4(ip_ad : str):
        req = requests.get(f"http://ip-api.com/json/{ip_ad}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query", timeout=500)
        # print(req.json())
        
        if req.status_code == 200:
            if req.json()['status'] == 'success':
                print(Colors.GREEN + f"└── v Status SUCCESS v : {ip_ad}" + Colors.END)
                for key, val in dict(req.json()).items():
                    print(f"[{key}]\t- {val}")

        else:
            print(Colors.RED + f"└── x Status FAIL x : {ip_ad}" + Colors.END)

class Port_Scanner:
    """
    HackTools -> Port Scanner

    args:
        - host : str
        - port_range : int = 1023
    """
    def __init__(self, host : str, port_range : int = 1023) -> None:
        self.host, self.port_range = host, port_range

    def start(self):
        print(Colors.BACK_BLUE + f"== Port Scanner | {CurrentTime.created_at()} ==" + Colors.END)
        print(Colors.CYAN + f"├── Host : {self.host}" + Colors.END)
        print(Colors.CYAN + f"└── Port Range : 1 - {self.port_range}" + Colors.END)
        print('\n' * 2)

        #65536
        print(Colors.BLUE + "[-] Wait a few seconds (or minutes) for the analysis..." + Colors.END)
        ports = self.port_scan(self.host, range(1, self.port_range + 1))
        
        if not ports:
            print(Colors.RED + "Any port open..." + Colors.END)

        else:
            for port_number in ports:
                print(Colors.GREEN + "● " + Colors.END + f"Host ({self.host}) port - {port_number} : open")

    def scan_port(self, host, port):
        try:
            sock = socket(AF_INET, SOCK_STREAM)

            sock.settimeout(1)

            result = sock.connect_ex((host, port))

            if result == 0:
                return port, True
            
            else:
                return port, False
        
        except Exception:
            return port, False

    def port_scan(self, host, ports, workers=10):
        open_ports = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # Mapeia a função scan_port para cada porta na lista de portas
            future_to_port = {executor.submit(self.scan_port, host, port): port for port in ports}

            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                
                try:
                    port_result = future.result()
                    if port_result[1]:
                        open_ports.append(port_result[0])
                
                except Exception as e:
                    print(f"Error scanning port {port}: {e}")
        
        return open_ports