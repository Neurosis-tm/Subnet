from os import system
try:
    from ipwhois import IPWhois
except ImportError:
    import os
    os.system('pip install ipwhois')
    from ipwhois import IPWhois
    os.system('pip install requests')
    import requests
def get_asn(ip_address):
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_rdap()
        return result.get('asn', 'ASN bulunamadı')
    except Exception as e:
        return f'Hata: {e}'

def get_ip_ranges(asn):
    try:
        url = f'https://api.bgpview.io/asn/{asn}/prefixes'
        response = requests.get(url)
        data = response.json()
        
        print(f"API jogaby: {data}")  # ýalňyşlary tapmak üçin

        if 'data' in data and 'ipv4_prefixes' in data['data']:
            # diňe ipi almak üçin split('/')[0] ullanýarys
            ipv4_addresses = [prefix['prefix'].split('/')[0] for prefix in data['data']['ipv4_prefixes']]
            if ipv4_addresses:
                with open(f'ASN_{asn}_asn subnet info.txt', 'w') as file:
                    file.write('\n'.join(ipv4_addresses))
                return ipv4_addresses
            else:
                return "IP adresi tapylmady."
        else:
            return "maglumat tapylmady!"
    except Exception as e:
        return f'Hata: {e}'

def main():
    while True:
        print("""\033[91m
           _____       __               __          __              __            
          / ___/__  __/ /_  ____  ___  / /_   _____/ /_  ___  _____/ /_____  _____
          \__ \/ / / / __ \/ __ \/ _ \/ __/  / ___/ __ \/ _ \/ ___/ //_/ _ \/ ___/
         ___/ / /_/ / /_/ / / / /  __/ /_   / /__/ / / /  __/ /__/ ,< /  __/ /    
        /____/\__,_/_.___/_/ /_/\___/\__/   \___/_/ /_/\___/\___/_/|_|\___/_/ """)
        
        print("""\033[92m|---------------------------------------------------------------------------|""")
        print("""\033[94m|             Created by: @REDHAKER                                         |""")
        print("""\033[92m|---------------------------------------------------------------------------|""")
        print("""\033[93m|       1.ipv4 adresi bilen ASN kodyny tapmak")                             |""")
        print("""\033[93m|       2.Asn bilen podset çykarmak")                                       |""")
        print("""\033[93m|       3.Çykyş                                                             |""")
        print("""\033[92m|---------------------------------------------------------------------------|""")


        choice = input("\033[91m1-3:").strip()
        
        if choice == "1":
            ip = input("IPv4 adresi giriziň: ")
            asn = get_asn(ip)
            print(f"{ip} adresinin ASN kody: {asn}")
        elif choice == "2":
            asn = input("ASN kodyny giriziň: ")
            if asn.isdigit():
                ip_ranges = get_ip_ranges(asn)
                print(ip_ranges)
                if isinstance(ip_ranges, list) and ip_ranges:
                    print(f"ASN {asn} üçin IP adresleri '{asn}asn subnet info.txt' faýlyna goşuldy.")
                else:
                    print(f"ASN {asn} üçin IP adresleri tapylmady!")
            else:
                print("Dogry ASN kody giriziň!")
        elif choice == "3":
            print("Çykylýar...")
            break
        else:
            print("ýalňys seçim, täzeden 1-3 aralygynda san seçiň!\033[0m")

if __name__ == "__main__":
    main()