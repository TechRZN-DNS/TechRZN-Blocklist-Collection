import os
import requests
import shutil
from datetime import datetime

# --- KONFIGURATION ---
CATEGORIES = {
    "ads": "sources/ads.raw",
    "tracking": "sources/tracking.raw",
    "malware": "sources/malware.raw",
    "phishing": "sources/phishing.raw",
    "threat_intel": "sources/threat_intel.raw",
    "fakeshops": "sources/fakeshops.raw",
    "gambling": "sources/gambling.raw",
    "crypto": "sources/crypto.raw",
    "dating": "sources/dating.raw",
    "spam": "sources/spam.raw",
    "fake_science": "sources/fake_science.raw",
    "bypass": "sources/bypass.raw",
    "native_tracker": "sources/native_tracker.raw",
    "popups": "sources/popups.raw",
    "domain_squatting": "sources/domain_squatting.raw",
    "jugendschutz": "sources/jugendschutz.raw"
}

# --- NEUE PFADE FÜR IP-LISTE ---
MANUAL_IP_SRC = "manual_sources/deny-ip-list.txt"
IP_OUTPUT = "blocklists/techrzn_ips.txt"

OUTPUT_DIR = "blocklists"
WL_DIR = "Whitelists"
LOCAL_WHITELIST = "sources/whitelist.raw"
REMOTE_WHITELIST = "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/whitelist-referral.txt"

def clean_domain(line):
    line = line.strip().lower()
    if not line or line.startswith(('#', '!', '[')):
        return None
    if '://' in line:
        line = line.split('://')[-1]
    line = line.split('/')[0]
    line = line.replace('*.', '').replace('*', '')
    domain = line.replace('@@||', '').replace('^$important', '').replace('||', '').replace('^', '')
    if ' ' in domain:
        return None
    if domain.startswith('www.'):
        domain = domain[4:]
    domain = domain.split('#')[0].split('!')[0].strip()
    return domain if domain and '.' in domain else None

def main():
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # 1. Ordner vorbereiten
    for folder in [OUTPUT_DIR, WL_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    # 2. Whitelist aufbauen
    whitelist = set()
    if os.path.exists(LOCAL_WHITELIST):
        with open(LOCAL_WHITELIST, 'r', encoding='utf-8') as f:
            for line in f:
                d = clean_domain(line)
                if d: whitelist.add(d)
    
    try:
        r = requests.get(REMOTE_WHITELIST, timeout=15)
        if r.status_code == 200:
            for line in r.text.splitlines():
                d = clean_domain(line)
                if d: whitelist.add(d)
    except:
        print("⚠️ Warnung: Remote Whitelist konnte nicht geladen werden.")

    wl_file = os.path.join(WL_DIR, "techrzn_whitelist.txt")
    with open(wl_file, 'w', encoding='utf-8') as f:
        f.write(f"### TechRZN Master Whitelist ###\n### Stand: {timestamp} ###\n\n")
        for d in sorted(list(whitelist)):
            f.write(f"{d}\n")
    print(f"✅ Whitelist erstellt: {len(whitelist)} Einträge.")

    # --- 3. MANUELLE IP-LISTE VERARBEITEN (NEU) ---
    if os.path.exists(MANUAL_IP_SRC):
        print(f"⚙️ Verarbeite manuelle IP-Quelle: {MANUAL_IP_SRC}")
        ip_count = 0
        with open(MANUAL_IP_SRC, "r", encoding="utf-8") as f_in:
            lines = f_in.readlines()
            
        with open(IP_OUTPUT, "w", encoding="utf-8") as f_out:
            f_out.write(f"### TechRZN - Deny IP List (Marius Hosting) ###\n")
            f_out.write(f"### Stand: {timestamp} ###\n\n")
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('#', '!', '/')):
                    f_out.write(f"{line}\n")
                    ip_count += 1
        print(f"✅ IP-Liste erstellt: {ip_count} Einträge in {IP_OUTPUT}")
    else:
        print(f"ℹ️ Keine manuelle IP-Liste in {MANUAL_IP_SRC} gefunden. Überspringe...")

    # 4. Domain-Blocklisten bauen
    for cat_name, src_path in CATEGORIES.items():
        if not os.path.exists(src_path):
            continue
        
        category_domains = set()
        with open(src_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for url in urls:
            try:
                final_url = url.replace("cdn.jsdelivr.net/gh/", "raw.githubusercontent.com/").replace("@latest/", "/main/")
                r = requests.get(final_url, timeout=20)
                if r.status_code == 200:
                    for line in r.text.splitlines():
                        domain = clean_domain(line)
                        if domain and domain not in whitelist:
                            category_domains.add(domain)
            except Exception:
                continue

        if category_domains:
            output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"### TechRZN - {cat_name.upper()} ###\n")
                f.write(f"### Stand: {timestamp} | Regeln: {len(category_domains):,} ###\n\n".replace(',', '.'))
                for d in sorted(list(category_domains)):
                    f.write(f"||{d}^\n")
            print(f"✅ {cat_name} fertig.")

    # 5. Aufräumen
    for ghost in ["combined_part1.txt", "combined_part2.txt", "combined_blocklist.txt", "update_list.py"]:
        if os.path.exists(ghost):
            os.remove(ghost)

if __name__ == "__main__":
    main()
