import socket, json, os
from concurrent.futures import ThreadPoolExecutor
from services import Colors

class SubdomainFinder:
    """
    HackTools -> Subdomain Finder
    Enumerates subdomains based on a wordlist.
    """

    DEFAULT_WORDLIST = [
        "mail", "mail2", "www", "ns2", "ns1", "blog", "localhost", "m",
        "ftp", "mobile", "ns3", "smtp", "search", "api", "dev", "secure",
        "webmail", "admin", "img", "news", "sms", "marketing", "test",
        "video", "www2", "media", "static", "ads", "mail2", "beta", "wap",
        "blogs", "download", "dns1", "www3", "origin", "shop", "forum",
        "chat", "www1", "image", "new", "tv", "dns", "services", "music",
        "images", "pay", "ddrint", "conc"
    ]

    @staticmethod
    def check_subdomain(domain, sub):
        fqdn = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(fqdn)
            return fqdn, ip
        except:
            return None

    @staticmethod
    def find_subdomains(domain, wordlist_path=None, threads=30):
        print(Colors.BLUE + f"\n[+] Searching subdomains for: {domain}\n" + Colors.END)
        print(Colors.BLUE + f"\n[+] Threads: {threads}\n" + Colors.END)

        # Load wordlist
        if wordlist_path and os.path.isfile(wordlist_path):
            with open(wordlist_path, "r", encoding="utf-8") as f:
                words = [w.strip() for w in f.readlines() if w.strip()]
            print(Colors.GREEN + f"[+] Loaded {len(words)} words from custom wordlist\n" + Colors.END)
        else:
            words = SubdomainFinder.DEFAULT_WORDLIST
            print(Colors.YELLOW + f"[!] Using built-in default wordlist ({len(words)} entries)\n" + Colors.END)

        found = []

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for result in executor.map(lambda sub: SubdomainFinder.check_subdomain(domain, sub), words):
                if result:
                    fqdn, ip = result
                    print(Colors.GREEN + f"[FOUND] {fqdn} → {ip}" + Colors.END)
                    found.append({"subdomain": fqdn, "ip": ip})

        if not found:
            print(Colors.RED + "\n[!] No subdomains found." + Colors.END)
        else:
            print(Colors.CYAN + f"\n[+] Total found: {len(found)}\n" + Colors.END)

        return found

    @staticmethod
    def export_results(found, export_path="", as_json=False):
        if not export_path.strip():
            docs = os.path.join(os.path.expanduser("~"), "Documents")
            os.makedirs(docs, exist_ok=True)
            export_path = os.path.join(
                docs,
                "subdomains.json" if as_json else "subdomains.txt"
            )

        if as_json:
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(found, f, indent=4)
        else:
            with open(export_path, "w", encoding="utf-8") as f:
                for entry in found:
                    f.write(f"{entry['subdomain']} -> {entry['ip']}\n")

        print(Colors.GREEN + f"\n[+] Results exported to {export_path}" + Colors.END)