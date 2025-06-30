import whois
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from services import Colors

class WhoisLookup:
    """
    HackTools -> Whois Lookup | WHOIS query for domains or IPs, supports multiple, threading and exports to TXT or JSON.
    """
    @staticmethod
    def lookup(domain: str):
        try:
            whoisResponse = whois.whois(domain)
            result = { "domain": domain }
        
            print(Colors.GREEN + f"\n[WHOIS Info for {domain}]\n" + Colors.END)

            for attr in [
                'domain_name', 'registrar', 'registrar_url',
                'reseller', 'whois_server', 'referral_url',
                'updated_date', 'creation_date', 'expiration_date',
                'name_servers', 'status', 'emails'
                'dnssec', 'name', 'org', 'address', 'city',
                'state', 'registrant_postal_code', 'country'
            ]:
                
                result[attr] = getattr(whoisResponse, attr, None)

            return result
        
        except Exception as e:
            return {"domain": domain, "error": str(e)}

        except Exception as e:
            print(Colors.RED + f"[WhoisLookup] Error: {e}" + Colors.END)

    @staticmethod
    def save_result(result: dict, path: str = "", export_json=False):
        domain = result.get("domain", "unknown").replace('.', '_')
        filename = f"{domain}_whois.{ 'json' if export_json else 'txt' }"
        
        if not path:
            dir_path = Path.home() / "HackingTool_WhoisLookup"
        else:
            dir_path = Path(path)
        os.makedirs(dir_path, exist_ok=True)
        file_path = dir_path / filename

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                if export_json:
                    json.dump(result, f, indent=4, default=str)
                else:
                    for key, value in result.items():
                        f.write(f"{key}: {value}\n")
            print(Colors.GREEN + f"[+] WHOIS info saved to: {file_path}" + Colors.END)
        except Exception as e:
            print(Colors.RED + f"[!] Failed to save file: {e}" + Colors.END)

    @staticmethod
    def batch_lookup(domains: list, path: str = "", export_json=False):
        print(Colors.BLUE + f"\n[+] Starting WHOIS lookup on {len(domains)} targets..." + Colors.END)
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = { executor.submit(WhoisLookup.lookup, d): d for d in domains }
            for future in futures:
                result = future.result()
                domain = result.get("domain")
                
                # print no console (colorido)
                print(Colors.GREEN + f"\n[WHOIS Info for {domain}]" + Colors.END)
                for key, value in result.items():
                    if key != "domain":
                        print(f"{Colors.CYAN}{key}: {Colors.END}{value}")

                # save to file
                WhoisLookup.save_result(result, path, export_json)