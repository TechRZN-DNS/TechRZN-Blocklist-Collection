import re
import os
import requests

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

def is_valid_domain(domain):
    # Nur Domains bis 80 Zeichen zulassen (spart massiv Platz bei Tracking-Müll)
    if len(domain) > 80: return False
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')): return None
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    domain = domain.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '')
    if domain.startswith('www.'): domain = domain[4:]
    return domain

def build_whitelist():
    raw_file = 'allowlist.raw'
    output_file = 'whitelist.txt'
    all_domains = set()
    if not os.path.exists(raw_file):
        with open(raw_file, 'w') as f: f.write("# TechRZN Whitelist\n")
    with open(raw_file, 'r') as f:
        for line in f:
            domain = clean_domain(line)
            if domain and is_valid_domain(domain):
                all_domains.add(domain)
    with open(output_file, 'w') as f:
        f.write("### TechRZN - MASTER WHITELIST ###\n\n")
        for d in sorted(list(all_domains)):
            f.write(f"@@||{d}^$important\n")
    return all_domains

def fetch_and_build_blocklist(cat_name, source_file, global_whitelist):
    if not os.path.exists(source_file): return
    all_domains = set()
    with open(source_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            for line in r.text.splitlines():
                domain = clean_domain(line)
                # Filter: Domain muss gültig sein, nicht auf Whitelist und KEINE riesigen Subdomain-Ketten
                if domain and is_valid_domain(domain) and domain not in global_whitelist:
                    all_domains.add(domain)
        except: continue

    if all_domains:
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
        output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
        
        # Sicherheits-Check: Wenn Liste zu groß für GitHub (über 1,5 Mio Einträge), dann kürzen
        final_list = sorted(list(all_domains))
        if len(final_list) > 1200000:
            final_list = final_list[:1200000] # Kappt die Liste bei 1,2 Mio Einträgen
            
        with open(output_path, 'w') as f:
            f.write(f"### TechRZN - {cat_name.upper()} ###\n\n")
            for d in final_list:
                f.write(f"||{d}^\n")
        print(f"✅ {output_path} fertig.")

if __name__ == "__main__":
    w_list = build_whitelist()
    for cat, src in CATEGORIES.items():
        fetch_and_build_blocklist(cat, src, w_list)
