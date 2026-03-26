import requests
import os

# Deine 11 Quellen - Pfad für TechRZN-IPs auf neuen Repo-Namen angepasst
SOURCES = {
    "hagezi_pro": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt",
    "hagezi_bypass": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt",
    "hagezi_threat": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt",
    "techrzn_ips": "https://raw.githubusercontent.com/SmokingBull/TechRZN-Blocklist-Collection/refs/heads/main/deny-ip-list.txt",
    "hagezi_windows": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_63.txt",
    "smart_tv": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_7.txt",
    "urlhaus_malicious": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_11.txt",
    "hagezi_gambling": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/gambling.mini.txt",
    "hagezi_fake": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt",
    "adguard_german": "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt",
    "dan_pollock": "https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt"
}

# Automatische HaGeZi Referral Whitelist
HAGEZI_WHITELIST_URL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt"

def clean_line(line):
    line = line.strip()
    if line and not line.startswith(('#', '!', '[', ' ')):
        return line.split('#')[0].split('!')[0].strip()
    return None

def main():
    combined_set = set()
    global_whitelist = set()

    # 1. Lokale Whitelist laden (Deine manuellen Einträge in Kleve)
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "r") as f:
            for line in f:
                domain = clean_line(line)
                if domain: global_whitelist.add(domain)

    # 2. Externe HaGeZi Whitelist laden
    try:
        r_white = requests.get(HAGEZI_WHITELIST_URL, timeout=15)
        for line in r_white.text.splitlines():
            domain = clean_line(line)
            if domain: global_whitelist.add(domain)
        print(f"Whitelist aktiv: {len(global_whitelist)} Domains geschützt.")
    except Exception as e:
        print(f"Hinweis: Externe Whitelist konnte nicht geladen werden: {e}")

    if not os.path.exists("lists"):
        os.makedirs("lists")

    # 3. Alle Listen verarbeiten und gegen Whitelist prüfen
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=20)
            lines = r.text.splitlines()
            individual_list = []
            for line in lines:
                cleaned = clean_line(line)
                if cleaned and cleaned not in global_whitelist:
                    individual_list.append(cleaned)
                    combined_set.add(cleaned)
            
            with open(f"lists/{name}.txt", "w") as f:
                f.write(f"# TechRZN Blocklist: {name}\n# Status: Automatisch bereinigt & ge-whitelistet\n\n")
                for item in sorted(set(individual_list)):
                    f.write(f"{item}\n")
            print(f"Update erfolgreich: {name}")
        except Exception as e:
            print(f"Fehler bei Quelle {name}: {e}")

    # 4. Die große Masterliste für AdGuard Home speichern
    with open("combined_blocklist.txt", "w") as f:
        f.write(f"# TechRZN Combined Masterlist\n# Erstellt für das Setup in Kleve\n\n")
        for item in sorted(combined_set):
            f.write(f"{item}\n")

if __name__ == "__main__":
    main()
