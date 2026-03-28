import requests
import os

# Die 14 Core-Module mit den exakten Namen aus deinem Screenshot
SOURCES = {
    "hagezi_pro": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt",
    "hagezi_bypass": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt",
    "hagezi_threat": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt",
    "techrzn_ips": "https://raw.githubusercontent.com/SmokingBull/malicious-ip-blocklist/main/deny-ip-list.txt",
    "hagezi_windows": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_63.txt",
    "smart_tv": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_7.txt",
    "urlhaus_malicious": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_11.txt",
    "hagezi_gambling": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/gambling.mini.txt",
    "hagezi_fake": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt",
    "adguard_german": "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt",
    "dan_pollock": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt",
    "notserious": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/notserious",
    "phishing_de": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Phishing-Angriffe",
    "fake_science": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Fake-Science"
}

def clean_line(line):
    line = line.strip()
    if line and not line.startswith(('#', '!', '[', ' ')):
        return line.split('#')[0].split('!')[0].strip()
    return None

def main():
    combined_set = set()
    global_whitelist = set()

    # 1. Lokale Whitelist laden
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "r") as f:
            for line in f:
                domain = clean_line(line)
                if domain: global_whitelist.add(domain)

    # 2. Ordner 'lists' sicherstellen
    if not os.path.exists("lists"):
        os.makedirs("lists")

    # 3. Quellen verarbeiten und im Unterordner 'lists' speichern
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                lines = r.text.splitlines()
                individual_list = []
                for line in lines:
                    cleaned = clean_line(line)
                    if cleaned and cleaned not in global_whitelist:
                        individual_list.append(cleaned)
                        combined_set.add(cleaned)
                
                # Pfad zu lists/name.txt
                filename = os.path.join("lists", f"{name}.txt")
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(f"# TechRZN Blocklist Module: {name}\n")
                    f.write(f"# Source: {url}\n\n")
                    for item in sorted(set(individual_list)):
                        f.write(f"{item}\n")
                print(f"✅ Created: {filename}")
            else:
                print(f"❌ Error {r.status_code} at {name}")
        except Exception as e:
            print(f"❌ Exception at {name}: {e}")

    # 4. Masterliste im Hauptverzeichnis speichern
    with open("combined_blocklist.txt", "w", encoding='utf-8') as f:
        f.write("# TechRZN Masterlist - Combined Protection Stack\n\n")
        for item in sorted(combined_set):
            f.write(f"{item}\n")
    
    print("\n--- All 14 files updated in /lists directory. ---")

if __name__ == "__main__":
    main()
