import requests
import os
import sys
from multiprocessing import Pool, cpu_count
from datetime import datetime

# --- GRUPPE 1: MASTER SOURCES (Basis für die geteilte Master-Liste) ---
MASTER_SOURCES = {
    "techrzn_ads": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_ads.txt", "TechRZN Ads"),
    "techrzn_tracking": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_tracking.txt", "TechRZN Tracking"),
    "techrzn_malware": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_malware.txt", "TechRZN Malware"),
    "techrzn_phishing": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_phishing.txt", "TechRZN Phishing"),
    "techrzn_threat_intel": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_threat_intel.txt", "TechRZN Threat Intel"),
    "techrzn_fakeshops": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_fakeshops.txt", "TechRZN Fakeshops"),
    "techrzn_squatting": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_domain_squatting.txt", "TechRZN Squatting"),
    "techrzn_gambling": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_gambling.txt", "TechRZN Gambling"),
    "techrzn_crypto": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_crypto.txt", "TechRZN Crypto"),
    "techrzn_dating": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_dating.txt", "TechRZN Dating"),
    "techrzn_spam": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_spam.txt", "TechRZN Spam"),
    "techrzn_fake_science": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_fake_science.txt", "TechRZN Fake Science"),
    "techrzn_bypass": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_bypass.txt", "TechRZN Bypass"),
    "techrzn_ips": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/techrzn_ips.txt", "TechRZN IPs"),
    "hagezi_pro": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt", "HaGeZi Pro"),
    "urlhaus_malicious": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_11.txt", "URLHaus"),
    "adguard_german": ("https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt", "AdGuard German"),
    "dan_pollock": ("https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt", "Dan Pollock"),
    "notserious": ("https://raw.githubusercontent.com/notserious/Anti-FakeShop/main/fakeshops.txt", "Anti-Fakeshop")
}

# --- GRUPPE 2: SPECIAL SOURCES ---
SPECIAL_SOURCES = {
    "techrzn_porn": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_porn.txt", "TechRZN Porn"),
    "techrzn_jugendschutz": ("https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_jugendschutz.txt", "TechRZN Jugendschutz")
}

REMOTE_WHITELIST_URL = "https://raw.githubusercontent.com/hagezi/dns-blocklists/refs/heads/main/adblock/whitelist-referral.txt"

def clean_line(line):
    if not line: return None
    line = line.strip()
    if line and not line.startswith(('#', '!', '[', ' ')):
        cleaned = line.replace('||', '').replace('^', '')
        return cleaned.split('#')[0].split('!')[0].strip()
    return None

def process_source(args):
    name, url, credit, whitelist_set = args
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        lines = r.text.splitlines()
        raw_count = len(lines)
        
        individual_set = set()
        for line in lines:
            cleaned = clean_line(line)
            if cleaned and cleaned not in whitelist_set:
                individual_set.add(cleaned)
        
        os.makedirs("lists", exist_ok=True)
        with open(os.path.join("lists", f"{name}.txt"), "w", encoding='utf-8') as f:
            f.write(f"# TechRZN Module: {name} | Source: {credit}\n\n")
            f.write("\n".join(sorted(individual_set)))
            
        return list(individual_set), raw_count
    except Exception:
        return [], 0

def main():
    final_whitelist = set()
    try:
        if os.path.exists("whitelist.txt"):
            with open("whitelist.txt", "r", encoding='utf-8', errors='ignore') as f:
                for line in f:
                    d = clean_line(line)
                    if d: final_whitelist.add(d.replace('*.', ''))
        r_white = requests.get(REMOTE_WHITELIST_URL, timeout=15)
        if r_white.status_code == 200:
            for line in r_white.text.splitlines():
                d = clean_line(line)
                if d: final_whitelist.add(d)
    except: pass

    ALL_SOURCES = {**MASTER_SOURCES, **SPECIAL_SOURCES}
    tasks = [(name, url, credit, final_whitelist) for name, (url, credit) in ALL_SOURCES.items()]
    
    with Pool(processes=cpu_count()) as pool:
        results_map = pool.map(process_source, tasks)
        results_dict = dict(zip(ALL_SOURCES.keys(), results_map))

    master_domains = []
    total_raw_lines = 0
    for name in MASTER_SOURCES.keys():
        domains, raw_count = results_dict[name]
        master_domains.extend(domains)
        total_raw_lines += raw_count

    combined_set = sorted(list(set(master_domains))) # Sortiert & Dedupliziert
    timestamp = datetime.now().strftime("%d. %B %Y um %H:%M")

    # --- MASTER-LISTE SPLITTEN (GitHub 100MB Limit Umgehung) ---
    half = len(combined_set) // 2
    part1 = combined_set[:half]
    part2 = combined_set[half:]

    # Speichern Part 1
    try:
        with open("combined_part1.txt", "w", encoding='utf-8') as f:
            f.write("############################################################\n")
            f.write("# TechRZN Master Blocklist - PART 1\n")
            f.write(f"# Aktualisiert: {timestamp} | Einträge: {len(part1):,}\n".replace(',', '.'))
            f.write("############################################################\n\n")
            f.write("\n".join(part1))
        
        # Speichern Part 2
        with open("combined_part2.txt", "w", encoding='utf-8') as f:
            f.write("############################################################\n")
            f.write("# TechRZN Master Blocklist - PART 2\n")
            f.write(f"# Aktualisiert: {timestamp} | Einträge: {len(part2):,}\n".replace(',', '.'))
            f.write("############################################################\n\n")
            f.write("\n".join(part2))
            
        print(f"✨ Master-Liste aufgeteilt erstellt ({len(combined_set)} Regeln total).")
        
        # WICHTIG: Die alte zu große Datei löschen, falls vorhanden
        if os.path.exists("combined_blocklist.txt"):
            os.remove("combined_blocklist.txt")
            
    except Exception as e:
        print(f"Fehler beim Speichern der Master-Teile: {e}")

    # --- Spezial-Listen ---
    for name in SPECIAL_SOURCES.keys():
        domains, raw_count = results_dict[name]
        if domains:
            output_file = f"{name}.txt"
            with open(output_file, "w", encoding='utf-8') as f:
                f.write(f"# TechRZN Special Module: {name.upper()}\n")
                f.write(f"# Stand: {timestamp} | Regeln: {len(domains)}\n\n")
                f.write("\n".join(sorted(domains)))
            print(f"🔞 Spezial-Liste erstellt: {output_file}")

if __name__ == "__main__":
    main()
