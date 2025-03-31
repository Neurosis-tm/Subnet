from os import system
import requests
import socket
try:
    from ipwhois import IPWhois
except ImportError:
    system('pip install ipwhois')
    from ipwhois import IPWhois
    system('pip install requests')

def get_asn(ip_address):
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_rdap()
        return result.get('asn', 'ASN kody tapylmady')
    except Exception as e:
        return f'Error: {e}'

def get_ip_from_domain(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return "Nädogry domain adresi girdiňiz"

def get_ip_ranges(asn):
    try:
        url = f'https://api.bgpview.io/asn/{asn}/prefixes'
        response = requests.get(url)
        data = response.json()

       
        if response.status_code != 200:
            return f"Error: API haýyşy şowsuz boldy, HTTP status kody: {response.status_code}"

        if 'data' in data and 'ipv4_prefixes' in data['data']:
            ipv4_addresses = [prefix['prefix'].split('/')[0] for prefix in data['data']['ipv4_prefixes']]
            if ipv4_addresses:
                with open(f'ASN_{asn}_asn_subnet_info.txt', 'w') as file:
                    file.write('\n'.join(ipv4_addresses))
                return ipv4_addresses
            else:
                return "Ip adresi tapylmady!"
        else:
            return "data tapylmady"
    except Exception as e:
        return f'Hata: {e}'

def main():
    while True:
        print("""
         _____       __               __                
        / ___/__  __/ /_  ____  ___  / /_ 
        \__ \/ / / / __ \/ __ \/ _ \/ __/  
       ___/ / /_/ / /_/ / / / /  __/ /_   
      /____/\__,_/_.___/_/ /_/\___/\__/    
        """)
        
        print("\033[92m|--------------------------------------|")
        print("\033[94m|      Created by: @REDHAKER           |")
        print("\033[92m|--------------------------------------|")
        print("\033[93m| 1. IP adresi bilen asn kody tapmak   |")
        print("\033[93m| 2. Domain bilen ip adresini tapmak   |")
        print("\033[93m| 3. ASN kody bilen podsetleri tapmak  |")
        print("\033[93m| 4. Çykyş                             |")
        print("\033[92m|------------------------------------- |")

        choice = input("\033[91m1-4: ").strip()
        
        if choice == "1":
            ip = input("Ip adresini giriziň: ")
            asn = get_asn(ip)
            print(f"{ip} adresiniň ASN kody: {asn}")
        
        elif choice == "2":
            domain = input("Domain adresini giriziň: ").strip()
            ip = get_ip_from_domain(domain)
            if ip != "Nädogry domain adresi girdiňiz":
                print(f"{domain} domainyň IP adresi: {ip}")
            else:
                print(ip)  

        elif choice == "3":
            asn = input("ASN kodunu girin: ").strip()
            if asn.isdigit():
                ip_ranges = get_ip_ranges(asn)
                print(ip_ranges)
                if isinstance(ip_ranges, list) and ip_ranges:
                    print(f"ASN {asn} üçin IP adresleri 'ASN_{asn}_asn_subnet_info.txt' faýlyna goşuldy.")
                else:
                    print(f"ASN {asn} üçin podsetler tapylmady!")
            else:
                print("Dogry ASN kody giriziň!")
        
        elif choice == "4":
            print("Çykylýar...")
            break
        else:
            print("Yanlış seçim, 1-4 aralygynda bir san giriziň!\033[0m")

if __name__ == "__main__":
    main()
