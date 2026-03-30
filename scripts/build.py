import re
import os
import requests

# 1. Konfiguration nach Wichtigkeit (Hagezi-Style)
# Die oberen Kategorien werden zuerst gefüllt, bis das Limit erreicht ist.
CATEGORIES = [
    ("malware", "sources/malware.raw"),
    ("phishing", "sources/phishing.raw"),
    ("threat_intel", "sources/threat_intel.raw"),
    ("ads", "sources/ads.raw"),
    ("tracking", "sources/tracking.raw"),
    ("fakeshops", "sources/fakeshops.raw"),
    ("crypto", "sources/crypto.raw"),
    ("spam", "sources/spam.raw"),
    ("native_tracker", "sources/native_tracker.raw"),
    ("popups", "sources/popups.raw")
    # Weniger wichtige Kategorien wie 'dating' oder 'porn' 
    # fliegen hier raus, um die 900k einzuhalten.
]

OUTPUT_FILE = "combined_blocklist.txt"
WHITELIST_RAW = "allowlist.raw"
MAX_TOTAL_DOMAINS = 900000 

def is_valid_domain(domain):
    if not domain or len(domain) > 80: return False
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): return None
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    if domain.startswith('www.'): domain = domain[4:]
    return domain.split('#')[0].strip()

if __name__ == "__main__":
    # Whitelist laden
    whitelist = set()
    if os.path.exists(WHITELIST_RAW):
        with open(WHITELIST_RAW, 'r') as f:
            for line in f:
                d = clean_domain(line)
                if d: whitelist.add(d)

    master_domains = []
    seen_domains = set()

    for cat_name, src_file in CATEGORIES:
        if len(master_domains) >= MAX_TOTAL_DOMAINS:
            break
        
        if not os.path.exists(src_file): continue
        
        with open(src_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for url in urls:
            if len(master_domains) >= MAX_TOTAL_DOMAINS: break
            try:
                r = requests.get(url, timeout=10)
                for line in r.text.splitlines():
                    domain = clean_domain(line)
                    if domain and is_valid_domain(domain) and domain not in whitelist:
                        if domain not in seen_domains:
                            master_domains.append(domain)
                            seen_domains.add(domain)
                            if len(master_domains) >= MAX_TOTAL_DOMAINS: break
            except:
                continue

    # Speichern als EINE All-in-One Datei
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"### TechRZN - HAGEZI-STYLE ALL-IN-ONE ###\n")
        f.write(f"### Optimized Limit: {len(master_domains)} ###\n\n")
        for d in sorted(master_domains):
            f.write(f"||{d}^\n")
            
    print(f"✨ Fertig! {len(master_domains)} wichtigste Domains gespeichert.")
