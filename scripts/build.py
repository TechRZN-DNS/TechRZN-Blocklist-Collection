import re
import os
import requests
import shutil

# Alle Kategorien passend zu deinen .raw Dateien
CATEGORIES = {
    "malware": "sources/malware.raw",
    "phishing": "sources/phishing.raw",
    "fakeshops": "sources/fakeshops.raw",
    "ads": "sources/ads.raw",
    "tracking": "sources/tracking.raw",
    "jugendschutz": "sources/jugendschutz.raw",
    "dating": "sources/dating.raw",
    "crypto": "sources/crypto.raw",
    "gambling": "sources/gambling.raw",
    "spam": "sources/spam.raw",
    "fake_science": "sources/fake_science.raw",
    "domain_squatting": "sources/domain_squatting.raw",
    "threat_intel": "sources/threat_intel.raw",
    "bypass": "sources/bypass.raw",
    "popups": "sources/popups.raw",
    "native_tracker": "sources/native_tracker.raw"
}

OUTPUT_DIR = "blocklists"
WL_DIR = "Whitelists"
WHITELIST_RAW = "sources/whitelist.raw" # Pfad angepasst

def clean_domain(line):
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): return None
    # Bereinigung von Präfixen und Suffixen
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    if domain.startswith('www.'): domain = domain[4:]
    return domain.split('#')[0].strip()

if __name__ == "__main__":
    # 1. Verzeichnisse vorbereiten
    for folder in [OUTPUT_DIR, WL_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder)

    # 2. Whitelist laden & exportieren
    whitelist = set()
    if os.path.exists(WHITELIST_RAW):
        with open(WHITELIST_RAW, 'r') as f:
            for line in f:
                d = clean_domain(line)
                if d: whitelist.add(d)
        
        # Die fertige Whitelist-Datei schreiben
        wl_output = os.path.join(WL_DIR, "techrzn_whitelist.txt")
        with open(wl_output, 'w', encoding='utf-8') as f:
            f.write("### TechRZN - GLOBAL WHITELIST ###\n\n")
            for d in sorted(list(whitelist)):
                f.write(f"{d}\n")
        print(f"✅ Whitelist exportiert ({len(whitelist)} Domains).")

    # 3. Kategorien (Blocklisten) verarbeiten
    for cat_name, src_file in CATEGORIES.items():
        if not os.path.exists(src_file): 
            print(f"⚠️ Überspringe {cat_name}: Quelle nicht gefunden.")
            continue
        
        category_domains = set()
        with open(src_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for url in urls:
            try:
                r = requests.get(url, timeout=15)
                for line in r.text.splitlines():
                    domain = clean_domain(line)
                    # Nur hinzufügen, wenn nicht auf der Whitelist
                    if domain and domain not in whitelist:
                        category_domains.add(domain)
            except: 
                continue

        if category_domains:
            output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"### TechRZN - {cat_name.upper()} ###\n\n")
                for d in sorted(list(category_domains)):
                    f.write(f"||{d}^\n")
            print(f"✅ {cat_name} fertig ({len(category_domains)} Domains).")
