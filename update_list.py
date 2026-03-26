import requests
import re

# Deine Quellen
urls = [
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt",
    "https://raw.githubusercontent.com/SmokingBull/malicious-ip-blocklist/refs/heads/main/deny-ip-list.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_63.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_7.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_11.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/gambling.mini.txt",
    "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/fake.txt",
    "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_6_German/filter.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt"
]

def main():
    combined_set = set()
    for url in urls:
        try:
            print(f"Lade: {url}")
            r = requests.get(url, timeout=15)
            lines = r.text.splitlines()
            for line in lines:
                line = line.strip()
                # Nur echte Einträge nehmen: Ignoriere Leerzeilen und reine Kommentare
                if line and not line.startswith(('#', '!', '[', ' ')):
                    # Falls der Eintrag noch Kommentare am Ende hat, schneiden wir sie ab
                    clean_line = line.split('#')[0].split('!')[0].strip()
                    if clean_line:
                        combined_set.add(clean_line)
        except Exception as e:
            print(f"Fehler bei {url}: {e}")

    # Speichern der bereinigten Liste
    with open("combined_blocklist.txt", "w") as f:
        f.write("# TechRZN Combined DNS Blocklist\n")
        f.write(f"# Einträge insgesamt: {len(combined_set)}\n")
        f.write("# Automatisch aktualisiert durch GitHub Actions\n\n")
        for item in sorted(combined_set):
            f.write(f"{item}\n")
    print(f"Fertig! {len(combined_set)} Einträge gespeichert.")

if __name__ == "__main__":
    main()
