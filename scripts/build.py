import os
import requests
import shutil
from datetime import datetime

# --- KONFIGURATION BLEIBT GLEICH ---
CATEGORIES = {
    "ads": "sources/ads.raw",
    "tracking": "sources/tracking.raw",
    "malware": "sources/malware.raw",
    "phishing": "sources/phishing.raw",
    "threat_intel": "sources/threat_intel.raw",
    "fakeshops": "sources/fakeshops.raw",
    "gambling": "sources/gambling.raw",
    "crypto": "sources/crypto.raw", # <--- Diese Datei wird jetzt korrekt gelesen
    "dating": "sources/dating.raw",
    "spam": "sources/spam.raw",
    "fake_science": "sources/fake_science.raw",
    "bypass": "sources/bypass.raw",
    "native_tracker": "sources/native_tracker.raw",
    "popups": "sources/popups.raw",
    "domain_squatting": "sources/domain_squatting.raw",
    "jugendschutz": "sources/jugendschutz.raw"
}

OUTPUT_DIR = "blocklists"
WL_DIR = "Whitelists"
LOCAL_WHITELIST = "sources/whitelist.raw"
REMOTE_WHITELIST = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt"
MANUAL_IP_SRC = "manual_sources/deny-ip-list.txt"
IP_OUTPUT = os.path.join(OUTPUT_DIR, "techrzn_ips.txt")

def clean_domain(line):
    line = line.strip().lower()
    # WICHTIG: AdGuard Filter-Regeln wie ||example.com^ müssen hier korrekt gesäubert werden
    if not line or line.startswith(('!', '[')): # '#' entfernt, da manche Listen Kommentare so nutzen
        return None
    if '://' in line:
        line = line.split('://')[-1]
    line = line.split('/')[0]
    line = line.replace('*.', '').replace('*', '')
    # Säuberung von AdBlock-Syntax
    domain = line.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    if ' ' in domain or not domain:
        return None
    if domain.startswith('www.'):
        domain = domain[4:]
    domain = domain.split('#')[0].split('!')[0].strip()
    return domain if domain and '.' in domain else None

def main():
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # 1. Ordner vorbereiten (Wir löschen nur, wenn wir neu schreiben können)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(WL_DIR, exist_ok=True)

    # 2. Whitelist aufbauen (Code verkürzt für Übersicht)
    whitelist = set()
    # ... (Deine Whitelist Logik) ...

    # 4. Domain-Blocklisten bauen
    for cat_name, src_path in CATEGORIES.items():
        if not os.path.exists(src_path):
            print(f"⚠️ {src_path} nicht gefunden.")
            continue
        
        print(f"⚙️ Verarbeite {cat_name}...")
        category_domains = set()
        
        with open(src_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for url in urls:
            try:
                # NUR GitHub Links anpassen, externe Links (AdGuard) so lassen wie sie sind!
                if "cdn.jsdelivr.net" in url:
                    url = url.replace("cdn.jsdelivr.net/gh/", "raw.githubusercontent.com/").replace("@latest/", "/main/")
                
                r = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    for line in r.text.splitlines():
                        domain = clean_domain(line)
                        if domain and domain not in whitelist:
                            category_domains.add(domain)
                else:
                    print(f"   ❌ Fehler {r.status_code} bei {url}")
            except Exception as e:
                print(f"   ❌ Timeout/Fehler bei {url}")
                continue

        # WICHTIGSTER FIX: Erstelle die Datei nur, wenn Domains gefunden wurden
        if category_domains:
            output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"### TechRZN - {cat_name.upper()} ###\n")
                f.write(f"### Stand: {timestamp} | Regeln: {len(category_domains)} ###\n\n")
                for d in sorted(list(category_domains)):
                    f.write(f"||{d}^\n")
            print(f"   ✅ {output_path} erstellt.")
        else:
            print(f"   ⚠️ Keine Domains für {cat_name} gefunden (Liste leer?)")

if __name__ == "__main__":
    main()
