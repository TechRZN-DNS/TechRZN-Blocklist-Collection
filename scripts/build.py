import re
import os
import requests

# 1. Konfiguration der Quellen
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
    "threat_intel": "sources/threat_intel.raw",
    "bypass": "sources/bypass.raw",
    "popups": "sources/popups.raw",
    "native_tracker": "sources/native_tracker.raw"
}

OUTPUT_DIR = "blocklists"
# MASTER_FILE entfernt, da > 100MB nicht auf GitHub erlaubt sind
WHITELIST_OUTPUT = "whitelist.txt"
WHITELIST_RAW = "allowlist.raw"

# --- Hilfsfunktionen ---

def is_valid_domain(domain):
    """Prüft, ob eine Domain syntaktisch korrekt ist und unter 80 Zeichen bleibt."""
    if not domain or len(domain) > 80: 
        return False
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    """Bereinigt verschiedene Formate (Hosts, AdBlock, URLs) zu reinen Domains."""
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): 
        return None
    
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    
    if domain.startswith('www.'): 
        domain = domain[4:]
    
    domain = domain.split('#')[0].strip()
    return domain

# --- Hauptfunktionen ---

def build_whitelist():
    """Baut die Whitelist basierend auf der allowlist.raw."""
    all_domains = set()
    if not os.path.exists(WHITELIST_RAW):
        with open(WHITELIST_RAW, 'w') as f: 
            f.write("# TechRZN Whitelist - Domains hier eintragen\n")
    
    with open(WHITELIST_RAW, 'r') as f:
        for line in f:
            domain = clean_domain(line)
            if domain and is_valid_domain(domain):
                all_domains.add(domain)
    
    with open(WHITELIST_OUTPUT, 'w') as f:
        f.write("### TechRZN - MASTER WHITELIST ###\n\n")
        for d in sorted(list(all_domains)):
            f.write(f"@@||{d}^$important\n")
    
    print(f"⚪ Whitelist erstellt ({len(all_domains)} Einträge).")
    return all_domains

def fetch_and_build(cat_name, source_file, global_whitelist):
    """Lädt URLs aus der .raw Datei, bereinigt sie und speichert die Einzel-Blockliste."""
    if not os.path.exists(source_file):
        print(f"⚠️ Quelldatei fehlt: {source_file}")
        return set()

    category_domains = set()
    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            for line in r.text.splitlines():
                domain = clean_domain(line)
                if domain and is_valid_domain(domain) and domain not in global_whitelist:
                    category_domains.add(domain)
        except Exception as e:
            print(f"❌ Fehler bei URL {url}: {e}")
            continue

    if category_domains:
        if not os.path.exists(OUTPUT_DIR): 
            os.makedirs(OUTPUT_DIR)
        
        output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
        final_list = sorted(list(category_domains))
        
        # Hard-Cap bei 1,2 Mio für Einzelkategorien
        if len(final_list) > 1200000:
            final_list = final_list[:1200000]
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"### TechRZN - {cat_name.upper()} ###\n\n")
            for d in final_list:
                f.write(f"||{d}^\n")
        
        print(f"✅ {output_path} fertig ({len(final_list)} Domains).")
    
    return category_domains

# --- Ausführung ---

if __name__ == "__main__":
    # 1. Whitelist laden
    w_list = build_whitelist()
    
    # 2. Master-Sammelbecken
    master_domains = set()

    # 3. Alle Kategorien verarbeiten
    for cat, src in CATEGORIES.items():
        print(f"🔄 Verarbeite Kategorie: {cat}...")
        current_domains = fetch_and_build(cat, src, w_list)
        master_domains.update(current_domains)

    # 4. Master-Liste (All-in-One) in 300.000er Häppchen splitten
    if master_domains:
        final_master = sorted(list(master_domains))
        chunk_size = 300000 # Limit für GitHub Dateigröße (ca. 40MB pro Datei)
        
        # Bestehende alte Part-Dateien aufräumen, falls nötig
        # (Optional: sorgt für sauberen Build)

        for i in range(0, len(final_master), chunk_size):
            part_num = (i // chunk_size) + 1
            chunk = final_master[i:i + chunk_size]
            filename = f"combined_part{part_num}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"### TechRZN - MASTER BLOCKLIST PART {part_num} ###\n")
                f.write(f"### Rules in this part: {len(chunk)} ###\n\n")
                for d in chunk:
                    f.write(f"||{d}^\n")
            print(f"✅ {filename} erstellt ({len(chunk)} Domains).")
        
        print(f"\n✨ MASTER-BUILD FERTIG: Insgesamt {len(final_master)} Regeln aufgeteilt.")
    else:
        print("\n❌ Fehler: Keine Domains gefunden.")
