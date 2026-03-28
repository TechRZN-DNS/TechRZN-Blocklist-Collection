import requests
import os

# Aktualisierte Quellen inklusive der 3 neuen RPiList Module
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
    # NEU: RPiList Module (Passend zu deinen GitHub Links)
    "notserious": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/notserious",
    "phishing_de": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Phishing-Angriffe",
    "fake_science": "https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Fake-Science"
}

HAGEZI_WHITELIST_URL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt"

def clean_line(line):
    line = line.strip()
    # Behält die Zeile nur, wenn sie keine Kommentare oder Metadaten enthält
    if line and not line.startswith(('#', '!', '[', ' ')):
        return line.split('#')[0].split('!')[0].strip()
    return None

def main():
    combined_set = set()
    global_whitelist = set()

    # 1. Whitelist laden (Falls vorhanden)
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "r") as f:
            for line in f:
                domain = clean_line(line)
                if domain: global_whitelist.add(domain)

    # 2. Ordner erstellen
    if not os.path.exists("lists"):
        os.makedirs("lists")

    # 3. Quellen verarbeiten
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
                
                # Speichert die Datei im Ordner lists/ (z.B. lists/notserious.txt)
                with open(f"lists/{name}.txt", "w") as f:
                    f.write(f"# TechRZN Blocklist: {name}\n")
                    f.write(f"# Source: {url}\n\n")
                    for item in sorted(set(individual_list)):
                        f.write(f"{item}\n")
                print(f"Erfolgreich verarbeitet: {name}")
            else:
                print(f"Fehler {r.status_code} bei {name}")
        except Exception as e:
            print(f"Fehler bei {name}: {e}")

    # 4. Masterliste (Combined) speichern
    with open("combined_blocklist.txt", "w") as f:
        f.write("# TechRZN Masterlist - Combined Protection\n\n")
        for item in sorted(combined_set):
            f.write(f"{item}\n")
    print("\n--- Fertig! Alle 14 Listen wurden aktualisiert. ---")

if __name__ == "__main__":
    main()
