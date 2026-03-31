<div align="center">

# TechRZN-Blocklist-Collection

[![Lizenz: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Maintainer: TechRZN](https://img.shields.io/badge/Maintainer-TechRZN-green.svg)](https://github.com/TechRZN)

**Eine professionelle Sammlung von Blocklisten zur Verbesserung der Sicherheit und Privatsphäre in Netzwerken (DNS, Firewall, NAS).**

---
</div>

<div align="center">

<br>

<p align="center">
  <img src="techrzn.png" width="650" alt="TechRZN DNS Filter-Hub" />
</p>

<p align="center">
  Sprache: 🇩🇪 <b>[Deutsch]</b> | 🇺🇸 <a href="README.en.md">[English]</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STATUS-INFRASTRUKTUR_AKTIV-00C853?style=for-the-badge&logo=statuspage&logoColor=white" />
  <img src="https://img.shields.io/badge/DATENBANK-OPTIMIERT-FF6B6B?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/UPLINK-2.5_GBIT_BACKBONE-7957d5?style=for-the-badge&logo=wi-fi&logoColor=white" />
</p>

---

## 🛰️ Mission & Vision
> **High-Performance Blocklisten • Täglich aktualisiert • 100% Bereinigt**

Willkommen beim **TechRZN Filter-Hub**. Dieses Repository bietet eine hocheffiziente Lösung für **AdGuard Home, Pi-hole und Technitium**. Durch automatisierte Deduplizierung und eine intelligente Whitelist garantieren wir Schutz ohne "Overblocking".

---

## ❤️ Support & Community
Wenn der **TechRZN Filter-Hub** dir hilft, dein Netzwerk sicherer zu machen, würde ich mich über deine Unterstützung auf Patreon freuen!

<p align="center">
  <a href="https://patreon.com/TechRZN">
    <img src="https://img.shields.io/badge/PATREON-BECOME_A_SUPPORTER-orange?style=for-the-badge&logo=patreon&logoColor=white" height="45" />
  </a>
  <br>
  <img src="https://img.shields.io/badge/Status-Community_Project-orange?style=for-the-badge&logo=patreon" height="25" />
  <img src="https://img.shields.io/github/stars/TechRZN-DNS/TechRZN-Blocklist-Collection?style=for-the-badge&logo=github&color=7957d5" height="25" />
</p>

---

## 🛡️ Die TechRZN Whitelist (Empfohlen)
> **Stabilität & Kompatibilität:** Damit wichtige Systemdienste (z.B. Windows Updates, Apple iCloud, Streaming-Logins) trotz massiver Blocklisten reibungslos funktionieren, haben wir eine globale Whitelist integriert.

<p align="center">
  <a href="https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/whitelist.txt">
    <img src="https://img.shields.io/badge/WHITELIST-LINK_KOPIEREN-blue?style=for-the-badge&logo=github&logoColor=white" height="45" />
  </a>
</p>

* **Funktion:** Verhindert "False Positives" (versehentliches Blockieren legitimer Seiten).
* **Wartung:** Wird kontinuierlich erweitert, um die beste "Out-of-the-box"-Erfahrung zu garantieren.

---

## 🚸 Jugendschutz (Optional)
> [!WARNING]
> **Bewusste Trennung:** Diese Liste wird separat angeboten, um "Overblocking" zu vermeiden und jedem Nutzer die Wahl zu lassen, ob dieser strenge Filter aktiviert werden soll.

<p align="center">
  <a href="https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_jugendschutz.txt">
    <img src="https://img.shields.io/badge/TECHRZN_KIDS_SAFETY-LINK_KOPIEREN-red?style=for-the-badge&logo=familysearch&logoColor=white" height="40" />
  </a>
</p>

* **TechRZN Kids Safety:** Strenger Filter für Familiensicherheit (Gewalt, Drogen, jugendgefährdende Seiten).

---

## 🛠️ Eigene TechRZN Spezial-Module
*Diese Listen werden direkt in Kleve, Deutschland, handkuratiert und auf maximale Präzision optimiert.*

| Status | Modul | Fokus & Schutzwirkung | Link |
| :---: | :--- | :--- | :---: |
| 🛡️ | **TechRZN Ads** | **Werbe-Schild:** Werbenetzwerke und Tracker (Hagezi Pro Basis). | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_ads.txt) |
| 🕵️‍♂️ | **TechRZN Tracking** | **Tracking:** CNAME-Tracker & Telemetrie (Win/Android/iOS). | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_tracking.txt) |
| 🦠 | **TechRZN Malware** | **Virenschutz:** Blockiert Malware & C2-Server. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_malware.txt) |
| 🎣 | **TechRZN Phishing** | **Betrugsschutz:** Schutz vor gefälschten Logins & Scams. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_phishing.txt) |
| 🛑 | **TechRZN Threat Intel** | **Gefahrenabwehr:** Botnetze und Cyberangriffe. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_threat_intel.txt) |
| 🛍️ | **TechRZN Fakeshops** | **Einkaufsschutz:** Sperrt bekannte Betrugsshops. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_fakeshops.txt) |
| 🎰 | **TechRZN Gambling** | **Spielerschutz:** Sperrt Casinos, Wetten & Lootboxen. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_gambling.txt) |
| 🪙 | **TechRZN Crypto** | **Krypto-Schild:** Stoppt Browser-Miner & Krypto-Betrug. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_crypto.txt) |
| ❤️ | **TechRZN Dating** | **Dating-Filter:** Zugang zu Dating-Plattformen sperren. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_dating.txt) |
| 📧 | **TechRZN Spam** | **Spam-Schutz:** Filtert aggressive Marketing- & Spam-Domains. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_spam.txt) |
| 🧪 | **TechRZN Fake Science** | **Faktencheck:** Pseudowissenschaft & Fake News. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_fake_science.txt) |
| 🔓 | **TechRZN Bypass** | **Tunnel-Block:** VPN- und Proxy-Umgehungen. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_bypass.txt) |
| 📱 | **TechRZN Native** | **Geräte-Check:** Spezielle Tracker für Smart-TVs & Mobile. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_native_tracker.txt) |
| 💥 | **TechRZN Popups** | **Popup-Sperre:** Blockiert nervige Layer und Werbefenster. | [🔗](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/blocklists/techrzn_popups.txt) |

---

## 🛠️ Einrichtung & Optimierung

<details>
<summary><b>📖 Schritt-für-Schritt Installation (AdGuard & Pi-hole)</b></summary>
<br>
<blockquote>
<h3>🛡️ AdGuard Home</h3>
1. Gehe zu <b>Filter</b> ➔ <b>DNS-Sperrlisten</b>.<br>
2. Klicke auf <b>Sperrliste hinzufügen</b> ➔ <b>Benutzerdefinierte Liste hinzufügen</b>.<br>
3. Füge die Links der gewünschten TechRZN-Module ein.<br>

<h3>🥧 Pi-hole</h3>
1. Gehe zu <b>Adlists</b> im linken Menü.<br>
2. Füge die Modul-URLs einzeln ein.<br>
3. <b>Wichtig:</b> Führe ein Update unter <i>Tools</i> ➔ <i>Update Gravity</i> aus.
</blockquote>
</details>

<details>
<summary><b>⚙️ Optimale AdGuard Home Einstellungen (Empfohlen)</b></summary>
<br>
<blockquote>
Für maximale Performance (getestet auf <b>UGREEN NAS / 2.5 Gbit/s</b>):<br><br>
<b>1. DNS-Cache & TTL</b><br>
* Cache-Größe: <code>104.857.600</code> (100 MB)<br>
* Optimistisches Caching: <b>Aktiviert</b> ✅<br>
* TTL-Minimalwert: <code>3600</code> (1 Stunde)<br>
* TTL-Maximalwert überschreiben: <code>84600</code> (24 Stunden) ✅<br><br>
<b>2. Sicherheit & Filterung</b><br>
* DNSSEC: <b>Aktiviert</b> ✅<br>
* Blockierungsmodus: <code>Null IP</code><br>
* Upstream-Timeout: <code>2</code> Sek ⚡<br>
* TTL der blockierten Antwort: <code>300</code> Sek
</blockquote>
</details>

---

## 🏗️ Hardware Backbone (Kleve, Deutschland)
*Validiert auf Enterprise-Hardware für absolute Zuverlässigkeit.*

<table align="center" width="100%" style="border-collapse: collapse; background-color: #0d1117; border-radius: 12px; overflow: hidden; border: 1px solid #30363d;">
  <tr>
    <td align="left" style="padding: 20px;">
      <b>CORE NODE</b><br>UGREEN NAS DXP4800 Plus<br>
      <img src="https://img.shields.io/badge/64_GB_DDR5_ECC-7957d5?style=flat-square" alt="Memory" />
    </td>
    <td align="left" style="padding: 20px;">
      <b>BESCHLEUNIGUNG</b><br>2x Samsung 990 Pro RAID<br>
      <img src="https://img.shields.io/badge/NVMe_Gen4_RAID_1-FF6B6B?style=flat-square" alt="Storage" />
    </td>
  </tr>
  <tr>
    <td align="left" style="padding: 20px;">
      <b>NETZWERK</b><br>2.5 Gbit Hybrid-Power<br>
      <img src="https://img.shields.io/badge/Zyxel_Managed_Switch-00D2FF?style=flat-square" alt="Networking" />
    </td>
    <td align="left" style="padding: 20px;">
      <b>SPEICHER</b><br>80 TB WD Red Pro (12G SAS)<br>
      <img src="https://img.shields.io/badge/RAID_5_ZFS-00C853?style=flat-square" alt="Drives" />
    </td>
  </tr>
</table>

---

<div align="center">

---

## 🛡️ Lizenz & Urheberrecht

**TechRZN-Blocklist-Collection** ist eine spezialisierte Lösung für Netzwerksicherheit und lizenziert unter der **GNU General Public License v3.0 (GPLv3)**.

**Copyright (c) 2026 Jörg Berns (TechRZN)** | **Standort: Kleve, Deutschland**

Den vollständigen Lizenztext findest du in der [LICENSE](LICENSE) Datei.

</div>

## 🙏 Credits & Quellen
Dieses Projekt basiert auf der wertvollen Arbeit von: **HaGeZi**, **AdGuard Team**, und **Abuse.ch**.

**Status: März 2026**
<br>
<img src="https://capsule-render.vercel.app/render?type=soft&color=7957d5&height=30&section=footer" width="100%" />

</div>
