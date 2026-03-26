<p align="center">
  <img src="techrzn-dns.png" width="400" alt="TechRZN DNS Logo">
</p>

# 🛡️ TechRZN DNS Filter Hub
### High-Performance Blocklists • Täglich aktualisiert • 100% Bereinigt

![GitHub last commit](https://img.shields.io/github/last-commit/SmokingBull/my-blocklist-collection?style=flat-square&color=blue)
![Rules](https://img.shields.io/badge/Total_Rules-1M+-success?style=flat-square)
![Status](https://img.shields.io/badge/Service-Automated-orange?style=flat-square)

Willkommen beim TechRZN Filter-Hub. Diese Repository bietet eine täglich aktualisierte "All-in-One" Blocklist für AdGuard Home, Pi-hole und Technitium. Alle Listen werden automatisch von Duplikaten bereinigt und gegen eine mehrstufige Whitelist geprüft.

---

## 🚀 Die Master-Liste (Empfohlen)
Die ultimative Lösung. Enthält alle 11 unten aufgeführten Listen in einer einzigen, performanten Datei.

**Link für deinen DNS-Filter:**
> `https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/combined_blocklist.txt`

---

## 🧩 Alle 11 Filter-Module einzeln
Hier kannst du die Filter nach Kategorien getrennt abonnieren.

| Modul | Fokus / Schutzbereich | Raw-Link |
| :--- | :--- | :--- |
| **🥇 HaGeZi Pro** | All-in-One Schutz | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_pro.txt) |
| **🔐 Bypass Filter** | VPN/Proxy/Tor/Bypass | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_bypass.txt) |
| **🏴‍☠️ Threat Intel** | Cyber-Angriffe & Botnets | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_threat.txt) |
| **🇩🇪 German Filter** | DE/AT/CH Optimierung | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/adguard_german.txt) |
| **📺 Smart-TV** | TV-Tracking & Werbung | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/smart_tv.txt) |
| **🦠 URLHaus** | Malware URLs & Phishing | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/urlhaus_malicious.txt) |
| **💻 Windows Spy** | MS Telemetrie & Office | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_windows.txt) |
| **🎮 Gambling** | Glücksspiel & Wetten | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_gambling.txt) |
| **⚠️ Fake DNS** | Scam & Fake-Shops | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/hagezi_fake.txt) |
| **📜 Dan Pollock** | Hosts-File Klassiker | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/dan_pollock.txt) |
| **📍 TechRZN IPs** | Eigene Malicious IP-Liste | [Link](https://raw.githubusercontent.com/SmokingBull/my-blocklist-collection/main/lists/techrzn_ips.txt) |

---

## ⚪ Intelligente Whitelists (Erlaubnislisten)
Um "Overblocking" zu vermeiden und sicherzustellen, dass wichtige Dienste (Logins, Referral-Links, Updates) funktionieren, nutzt TechRZN ein zweistufiges Verfahren:

1.  **HaGeZi Referral Whitelist:** Automatische Integration der [HaGeZi Whitelist](https://github.com/hagezi/dns-blocklists/blob/main/adblock/whitelist-referral.txt), um gängige Fehlblockierungen zu verhindern.
2.  **TechRZN Custom Whitelist:** Eine manuelle Liste (`whitelist.txt`) für ganz persönliche Ausnahmen.

---

## 🙏 Danksagung & Urheberrecht
Ein Projekt wie dieses wäre ohne die unermüdliche Arbeit der Community nicht möglich. Mein besonderer Dank gilt den Urhebern der hier genutzten Listen, deren Daten ich für mein Setup verwende:

* **[HaGeZi](https://github.com/hagezi/dns-blocklists):** Für die exzellenten Block- und Whitelists.
* **[AdGuard Team](https://github.com/AdguardTeam):** Für den deutschen Sprachfilter und die Hostlist-Registry.
* **[Abuse.ch (URLHaus)](https://urlhaus.abuse.ch/):** Für kritische Malware-Daten.
* **[Dan Pollock](https://someonewhocares.org/hosts/):** Für den legendären Hosts-Klassiker.
* **[Perflyst & Dandelion Sprout](https://github.com/Perflyst/PiHoleBlocklist):** Für die spezialisierten Smart-TV Filter.

**Vielen Dank für euren Beitrag zu einem sichereren Internet!**

---

## ⚙️ Setup & Wartung
* **Automatisierung:** Das System aktualisiert sich alle 24 Stunden automatisch per GitHub Actions.
* **Anpassung:** Trage eigene Domains in die `whitelist.txt` ein, um sie global freizugeben.

---

## ☕ Support
Wenn dir diese Zusammenstellung hilft, freue ich mich über einen digitalen Kaffee:
[**Unterstützen via PayPal**](https://www.paypal.me/DEIN_NAME)

---
*Maintained with ❤️ in Kleve • Stand: März 2026*
