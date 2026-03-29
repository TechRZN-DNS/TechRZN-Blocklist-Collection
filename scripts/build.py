import re
import os

def is_valid_domain(domain):
    # Validiert Domain-Struktur (keine Sonderzeichen außer - und .)
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$'
    return re.match(pattern, domain.lower()) is not None

def clean_domain(line):
    # Entfernt Protokolle, Pfade und Whitespace
    line = line.strip().lower()
    if not line or line.startswith('#'):
        return None
    domain = line.replace('http://', '').replace('https://', '').split('/')[0]
    domain = domain.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def build():
    raw_file = 'allowlist.raw'
    output_file = 'whitelist.txt'
    
    if not os.path.exists(raw_file):
        print(f"⚠️ {raw_file} nicht gefunden!")
        return

    with open(raw_file, 'r') as f:
        content = f.readlines()

    domains = set()
    for line in content:
        domain = clean_domain(line)
        if domain and is_valid_domain(domain):
            domains.add(domain)
        elif domain:
            print(f"❌ Ungültige Domain ignoriert: {domain}")

    sorted_domains = sorted(list(domains))
    
    with open(output_file, 'w') as f:
        f.write("############################################################\n")
        f.write("# TechRZN - Master Whitelist (HaGeZi-Style Build)\n")
        f.write(f"# Einträge: {len(sorted_domains)}\n")
        f.write("############################################################\n\n")
        for d in sorted_domains:
            f.write(f"@@||{d}^$important\n")

if __name__ == "__main__":
    build()
