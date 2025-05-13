import requests
import subprocess
from socket import *
from services import Colors

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