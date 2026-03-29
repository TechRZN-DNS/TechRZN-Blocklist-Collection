import re
import os
import requests

# Konfiguration: Name der Kategorie -> Pfad zur Datei im "sources" Ordner
# Angepasst an deinen Screenshot (Stand: 29.03.2026)
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
    "domain_squatting": "sources/domain_squatting.raw"
}

def is_valid_domain(domain):
    # Validiert die Domain-Struktur (keine Sonderzeichen außer - und .)
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    # Entfernt Protokolle, Pfade, Whitespace und AdBlock-Präfixe
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): 
        return None
    
    # Extrahiere reine Domain aus URLs oder AdBlock-Regeln
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    
    if domain.startswith('www.'): 
        domain = domain[4:]
    
    return domain

def build_whitelist():
    # Verarbeitet deine persönliche allowlist.raw im Hauptverzeichnis
    raw_file = 'allowlist.raw'
    output_file = 'whitelist.txt'
    all_domains = set()

    if os.path.exists(raw_file):
        with open(raw_file, 'r') as f:
            for line in f:
                domain = clean_domain(line)
                if domain and is_valid_domain(domain):
                    all_domains.add(domain)

    if all_domains:
        with open(output_file, 'w') as f:
            f.write("############################################################\n")
            f.write("# TechRZN - MASTER WHITELIST\n")
            f.write(f"# Einträge: {len(all_domains)}\n")
            f.write("############################################################\n\n")
            for d in sorted(list(all_domains)):
                f.write(f"@@||{d}^$important\n")
        print(f"✅ {output_file} mit {len(all_domains)} Domains erstellt.")

def fetch_and_build_blocklist(cat_name, source_file):
    # Verarbeitet die Blocklisten aus dem /sources Ordner
    all_domains = set()
    if not os.path.exists(source_file): 
        return

    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not urls:
        return

    for url in urls:
        try:
            print(f"📥 {cat_name.upper()}: Lade {url}...")
            r = requests.get(url, timeout=15)
            for line in r.text.splitlines():
                domain = clean_domain(line)
                if domain and is_valid_domain(domain):
                    all_domains.add(domain)
        except Exception as e:
            print(f"❌ Fehler bei {url}: {e}")

    if all_domains:
        output_file = f"techrzn_{cat_name}.txt"
        with open(output_file, 'w') as f:
            f.write(f"############################################################\n")
            f.write(f"# TechRZN - {cat_name.upper()} BLOCKLIST\n")
            f.write(f"# Einträge: {len(all_domains)}\n")
            f.write(f"############################################################\n\n")
            for d in sorted(list(all_domains)):
                f.write(f"||{d}^\n")
        print(f"✅ {output_file} erstellt.")

if __name__ == "__main__":
    # 1. Deine persönliche Whitelist bauen
    build_whitelist()
    
    # 2. Alle Blocklisten-Kategorien durchgehen
    for cat, src in CATEGORIES.items():
        fetch_and_build_blocklist(cat, src)
