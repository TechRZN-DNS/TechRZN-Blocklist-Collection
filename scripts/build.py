import re
import os
import requests

# Konfiguration: Alle 17 Kategorien mit Pfaden zu deinen .raw Dateien in sources/
CATEGORIES = {
    "malware": "sources/malware.raw",
    "phishing": "sources/phishing.raw",
    "fakeshops": "sources/fakeshops.raw",
    "ads": "sources/ads.raw",
    "tracking": "sources/tracking.raw",
    "jugendschutz": "sources/jugendschutz.raw",
    "porn": "sources/porn.raw",
    "dating": "sources/dating.raw",
    "crypto": "sources/crypto.raw",
    "gambling": "sources/gambling.raw",
    "spam": "sources/spam.raw",
    "fake_science": "sources/fake_science.raw",
    "domain_squatting": "sources/domain_squatting.raw",
    # DEINE NEUEN ERWEITERUNGEN:
    "threat_intel": "sources/threat_intel.raw",
    "bypass": "sources/bypass.raw",
    "popups": "sources/popups.raw",
    "native_tracker": "sources/native_tracker.raw"
}

# Hier landen die fertigen Dateien (dein neu erstellter Ordner)
OUTPUT_DIR = "blocklists"

def is_valid_domain(domain):
    """Prüft, ob eine Domain ein gültiges Format hat."""
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    """Bereinigt verschiedene Formate (Adblock, Hosts, URLs) zu reinen Domains."""
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): return None
    # Entferne Protokolle und Pfade
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    # Entferne Adblock-Syntax und Hosts-Präfixe
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    # www-Präfix entfernen für Einheitlichkeit
    if domain.startswith('www.'): domain = domain[4:]
    return domain

def build_whitelist():
    """Erstellt die Master-Whitelist aus allowlist.raw."""
    raw_file = 'allowlist.raw'
    output_file = 'whitelist.txt'
    all_domains = set()
    if os.path.exists(raw_file):
        with open(raw_file, 'r') as f:
            for line in f:
                domain = clean_domain(line)
                if domain and is_valid_domain(domain):
                    all_domains.add(domain)
    
    # Immer die Whitelist schreiben (auch wenn leer, für die Struktur)
    with open(output_file, 'w') as f:
        f.write("### TechRZN - MASTER WHITELIST ###\n")
        f.write("# Diese Domains werden NIEMALS blockiert.\n\n")
        for d in sorted(list(all_domains)):
            f.write(f"@@||{d}^$important\n")
    return all_domains

def fetch_and_build_blocklist(cat_name, source_file, global_whitelist):
    """Lädt Links aus der .raw Datei und baut die gefilterte Blocklist."""
    all_domains = set()
    if not os.path.exists(source_file): 
        print(f"⚠️ Datei fehlt: {source_file}")
        return
        
    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not urls: 
        print(f"ℹ️ Keine Links in {source_file} gefunden.")
        return

    for url in urls:
        try:
            print(f"📥 {cat_name.upper()}: Lade {url}...")
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            for line in r.text.splitlines():
                domain = clean_domain(line)
                if domain and is_valid_domain(domain) and domain not in global_whitelist:
                    all_domains.add(domain)
        except Exception as e:
            print(f"❌ Fehler bei {url}: {e}")

    if all_domains:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
        with open(output_path, 'w') as f:
            f.write(f"### TechRZN - {cat_name.upper()} BLOCKLIST ###\n")
            f.write(f"# Stand: 2026\n")
            f.write(f"# Einträge: {len(all_domains)}\n\n")
            for d in sorted(list(all_domains)):
                f.write(f"||{d}^\n")
        print(f"✅ {output_path} mit {len(all_domains)} Domains erstellt.")

if __name__ == "__main__":
    # 1. Whitelist laden/erstellen
    whitelist = build_whitelist()
    
    # 2. Alle Kategorien abarbeiten
    for cat, src in CATEGORIES.items():
        fetch_and_build_blocklist(cat, src, whitelist)
