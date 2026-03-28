import requests
import os

# Die 14 Core-Module (TechRZN Stack)
SOURCES = {
    "hagezi_pro": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt", "HaGeZi (Gold Standard)"),
    "hagezi_bypass": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt", "HaGeZi (VPN/Proxy)"),
    "hagezi_threat": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt", "HaGeZi (Threat Intel)"),
    "techrzn_ips": ("https://raw.githubusercontent.com/SmokingBull/malicious-ip-blocklist/main/deny-ip-list.txt", "SmokingBull / TechRZN"),
    "hagezi_windows": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_63.txt", "HaGeZi (Windows Telemetry)"),
    "smart_tv": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_7.txt", "AdGuard / TechRZN"),
    "urlhaus_malicious": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_11.txt", "Abuse.ch (URLHaus)"),
    "hagezi_gambling": ("https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/gambling.mini.txt", "HaGeZi (Gambling)"),
    "hagezi_fake": ("https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt", "HaGeZi (Fake DNS)"),
    "adguard_german": ("https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt", "AdGuard Team"),
    "dan_pollock": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt", "Dan Pollock (Classic)"),
    "notserious": ("https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/notserious", "RPiList (Anti-Fakeshop)"),
    "phishing_de": ("https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Phishing-Angriffe", "RPiList (Banking-Schutz)"),
    "fake_science": ("https://raw.githubusercontent.com/RPiList/specials/master/Blocklisten/Fake-Science", "RPiList (Fake-Science)")
}

# Externe HaGeZi Whitelist (Referrals/Affiliate)
REMOTE_WHITELIST_URL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/adblock/whitelist-referral.txt"

def clean_line(line):
    line = line.strip()
    if line and not line.startswith(('#', '!', '[', ' ')):
        # Entfernt Adblock-Syntax wie ||domain.com^
        cleaned = line.replace('||', '').replace('^', '')
        return cleaned.split('#')[0].split('!')[0].strip()
    return None

def is_whitelisted(domain, whitelist_set):
    """Prüft Domain und alle Subdomains gegen die kombinierte Whitelist."""
    if domain in whitelist_set:
        return True
    parts = domain.split('.')
    for i in range(len(parts) - 1):
        parent = '.'.join(parts[i+1:])
        if parent in whitelist_set:
            return True
    return False

def main():
    combined_set = set()
    global_whitelist = set()

    # 1. EIGENE LOKALE WHITELIST LADEN
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt", "r", encoding='utf-8') as f:
            for line in f:
                d = clean_line(line)
                if d: global_whitelist.add(d.replace('*.', ''))
        print(f"📂 Lokale Whitelist geladen.")

    # 2. EXTERNE HAGEZI WHITELIST LADEN & HINZUFÜGEN
    try:
        print(f"⏳ Lade HaGeZi Referral-Whitelist von GitHub...")
        r_white = requests.get(REMOTE_WHITELIST_URL, timeout=15)
        if r_white.status_code == 200:
            count = 0
            for line in r_white.text.splitlines():
                d = clean_line(line)
                if d:
                    global_whitelist.add(d)
                    count += 1
            print(f"✅ HaGeZi-Whitelist integriert (+{count} Einträge).")
    except Exception as e:
        print(f"⚠️ Fehler beim Laden der externen Whitelist: {e}")

    # 3. ORDNER 'LISTS' SICHERSTELLEN
    if not os.path.exists("lists"):
        os.makedirs("lists")

    # 4. QUELLEN VERARBEITEN
    for name, (url, credit) in SOURCES.items():
        try:
            r = requests.get(url, timeout=25)
            if r.status_code == 200:
                lines = r.text.splitlines()
                individual_list = []
                for line in lines:
                    cleaned = clean_line(line)
                    # Hier greift die kombinierte Whitelist-Logik
                    if cleaned and not is_whitelisted(cleaned, global_whitelist):
                        individual_list.append(cleaned)
                        combined_set.add(cleaned)
                
                filename = os.path.join("lists", f"{name}.txt")
                with open(filename, "w", encoding='utf-8') as f:
                    f.write(f"############################################################\n")
                    f.write(f"# TechRZN Blocklist Module: {name}\n")
                    f.write(f"# Credits: {credit} | Whitelisted by TechRZN & HaGeZi\n")
                    f.write(f"############################################################\n\n")
                    for item in sorted(set(individual_list)):
                        f.write(f"{item}\n")
                print(f"✅ Created: {filename}")
        except Exception as e:
            print(f"❌ Error at {name}: {e}")

    # 5. MASTERLISTE SPEICHERN
    with open("combined_blocklist.txt", "w", encoding='utf-8') as f:
        f.write("############################################################\n")
        f.write("# TechRZN Masterlist - Combined & Whitelisted Stack\n")
        f.write("# Credits: HaGeZi, RPiList, AdGuard, URLHaus, Dan Pollock\n")
        f.write("############################################################\n\n")
        for item in sorted(combined_set):
            f.write(f"{item}\n")
    
    print(f"\n--- Fertig! Gesamtanzahl Regeln: {len(combined_set)} ---")

if __name__ == "__main__":
    main()
