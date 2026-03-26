<p align="center">
  <img src="techrzn-dns.png" width="400" alt="TechRZN DNS Logo">
</p>

# 🛡️ TechRZN DNS Filter Hub
### High-Performance Blocklists • Täglich aktualisiert • 100% Bereinigt

![GitHub last commit](https://img.shields.io/github/last-commit/SmokingBull/my-blocklist-collection?style=flat-square&color=blue)
![Rules](https://img.shields.io/badge/Total_Rules-1M+-success?style=flat-square)
![Status](https://img.shields.io/badge/Service-Automated-orange?style=flat-square)

Willkommen beim TechRZN Filter-Hub. Diese Repository bietet eine täglich aktualisierte "All-in-One" Blocklist für AdGuard Home, Pi-hole und Technitium. Alle Listen werden automatisch von Duplikaten bereinigt und gegen eine eigene Whitelist geprüft.

---

## 🚀 Die Master-Liste (Empfohlen)
Die ultimative Lösung. Enthält alle 11 unten aufgeführten Listen in einer einzigen, performanten Datei.

**Link für deinen DNS-Filter:**
> `https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/combined_blocklist.txt`

---

## 🧩 Alle 11 Filter-Module einzeln
Hier kannst du die Filter nach Kategorien getrennt abonnieren. Ein großer Dank geht an alle Urheber für ihre Arbeit!

| Modul | Urheber / Projekt | Fokus | Raw-Link |
| :--- | :--- | :--- | :--- |
| **🥇 HaGeZi Pro** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | All-in-One Schutz | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_pro.txt) |
| **🔐 Bypass Filter** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | VPN/Proxy/Tor/Bypass | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_bypass.txt) |
| **🏴‍☠️ Threat Intel** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | Cyber-Angriffe & Botnets | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_threat.txt) |
| **🇩🇪 German Filter** | [AdGuard](https://github.com/AdguardTeam/FiltersRegistry) | DE/AT/CH Optimierung | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/adguard_german.txt) |
| **📺 Smart-TV** | [Perflyst/Dandelion](https://github.com/Perflyst/PiHoleBlocklist) | TV-Tracking & Werbung | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/smart_tv.txt) |
| **🦠 URLHaus** | [Abuse.ch](https://urlhaus.abuse.ch/) | Malware URLs & Phishing | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/urlhaus_malicious.txt) |
| **💻 Windows Spy** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | MS Telemetrie & Office | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_windows.txt) |
| **🎮 Gambling** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | Glücksspiel & Wetten | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_gambling.txt) |
| **⚠️ Fake DNS** | [HaGeZi](https://github.com/hagezi/dns-blocklists) | Scam & Fake-Shops | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_fake.txt) |
| **📜 Dan Pollock** | [Dan Pollock](https://someonewhocares.org/hosts/) | Hosts-File Klassiker | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/dan_pollock.txt) |
| **📍 TechRZN IPs** | [SmokingBull](https://github.com/SmokingBull) | Eigene Malicious IP-Liste | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/techrzn_ips.txt) |

---

## ⚙️ Setup & Wartung
* **Eigene Whitelist:** Trage Domains einfach in die `whitelist.txt` ein, um sie global in allen Listen freizugeben.
* **Update-Intervall:** Das System aktualisiert sich alle 24 Stunden automatisch per GitHub Actions.
* **Technik:** Das Python-Skript entfernt Kommentare und Metadaten, um die Systemlast auf deinem DNS-Server (z.B. NAS oder PC) zu minimieren.

---

## ☕ Support
Wenn dir diese Zusammenstellung hilft und du meine Arbeit unterstützen möchtest, freue ich mich über einen digitalen Kaffee:
[**Unterstützen via PayPal**](https://www.paypal.me/DEIN_NAME)

---
*Maintained with ❤️ in Kleve • Stand: März 2026*
