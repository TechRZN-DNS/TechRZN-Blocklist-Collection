<p align="center">
  <img src="techrzn-dns.png" width="400" alt="TechRZN DNS Logo">
</p>

<p align="center">
  Language: 🇺🇸 <b>[English]</b> | 🇩🇪 <a href="README.md">[Deutsch]</a>
</p>

# 🛡️ TechRZN-Blocklist-Collection
### High-Performance Blocklists • Updated Daily • 100% Cleaned

<p align="left">
  <a href="https://github.com/TechRZN-DNS/TechRZN-Blocklist-Collection/actions/workflows/main.yml">
    <img src="https://github.com/TechRZN-DNS/TechRZN-Blocklist-Collection/actions/workflows/main.yml/badge.svg" alt="Blocklist Update">
  </a>
  <img src="https://img.shields.io/github/last-commit/TechRZN-DNS/TechRZN-Blocklist-Collection?style=flat-square&color=blue" alt="Last Commit">
  <img src="https://img.shields.io/badge/Total_Rules-1M+-success?style=flat-square" alt="Rules">
  <img src="https://img.shields.io/badge/Service-Automated-orange?style=flat-square" alt="Status">
</p>

Welcome to the **TechRZN Filter-Hub**. This repository provides a daily updated "All-in-One" blocklist for **AdGuard Home**, **Pi-hole**, and **Technitium**. All lists are automatically deduplicated and cross-checked against an intelligent, multi-stage whitelist.

---

## 🚀 The Master-List (Recommended)
The ultimate solution for your setup. Contains all **14 core modules** in a single, high-performance file.

**Link for your DNS filter:**
> `https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/combined_blocklist.txt`

---

## 🧩 Modular Filter Architecture (The 14 Core Modules)
| Module | Focus / Protection Area | Raw Link |
| :--- | :--- | :--- |
| 🥇 **HaGeZi Pro** | Global All-in-One (Gold Standard) | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_pro.txt) |
| 🔐 **Bypass Filter** | VPN & Proxy Protection | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_bypass.txt) |
| 🏴‍☠️ **Threat Intel** | Botnets & Cyber-Defense | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_threat.txt) |
| 🇩🇪 **German Filter** | Optimization for DE / AT / CH | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/adguard_german.txt) |
| 📺 **Smart TV** | TV Tracking & Advertising | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/smart_tv.txt) |
| 🦠 **URLHaus** | Malware & Phishing Intelligence | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/urlhaus_malicious.txt) |
| 💻 **Windows Spy** | MS Telemetry & Office Opt. | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_windows.txt) |
| 🎮 **Gambling** | Gambling & Betting | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_gambling.txt) |
| ⚠️ **Fake DNS** | Scams & Fake Shops | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/hagezi_fake.txt) |
| 📜 **Dan Pollock** | Legendary Hosts File Classic | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/dan_pollock.txt) |
| 📍 **TechRZN IPs** | Curated Custom IP Blocklist | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/techrzn_ips.txt) |
| 🛍️ **Anti-Fakeshop** | Subscription Traps (RPiList) | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/notserious.txt) |
| 🏦 **Banking Protection** | Phishing (DE Banks - RPiList) | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/phishing_de.txt) |
| 🔬 **Fake Science** | Predatory Publishers (RPiList) | [Link](https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/lists/fake_science.txt) |

---

## ⚪ Intelligent Whitelist (Allowlist)
To prevent "overblocking" and ensure a smooth user experience (e.g., for provider logins, gaming, or affiliate redirects), TechRZN utilizes a unified Master Whitelist:

* **Content:** Personal TechRZN exceptions combined with HaGeZi's Referral Allowlist.
* **Technology:** The Python backend automatically recognizes subdomains and cleans all 14 blocklists in real-time.

**Integration in AdGuard Home (DNS Allowlists):**
> `https://raw.githubusercontent.com/TechRZN-DNS/TechRZN-Blocklist-Collection/main/whitelist.txt`

---

## ⚙️ Optimal AdGuard Home Settings
For maximum performance with 1M+ rules (tested on **UGREEN NAS / 2.5 Gbit/s**):

### 1️⃣ DNS Cache & TTL
* **Cache Size:** `104,857,600` (100 MB) ✅
* **Optimistic Caching:** Enabled ✅
* **TTL Minimum:** `3600` (1 hour) 💡

### 2️⃣ Security & Filtering
* **DNSSEC:** Enabled ✅
* **Blocking Mode:** `Default` ✅
* **Blocking Response TTL:** `300` seconds ✅

---

## 🙏 Credits & Sources
This project is built upon the incredible work of:
* 🛡️ **HaGeZi:** The global gold standard.
* 🚀 **RPiList:** Specialized protection (Fake Shops, Phishing).
* 🌐 **AdGuard Team:** Language filters & Registry.
* 🦠 **Abuse.ch (URLHaus):** Malware Intelligence.

---

## ☕ Support & Infrastructure
Maintaining over 1 million rules daily and operating the **2.5 Gbit/s test environment** in Kleve (UGREEN NAS / 64 GB RAM) requires significant time and resources. If my work helps you:

* **Feedback:** Open an issue or give the project a ⭐.
* **Support:** Please contact me directly if you're interested in supporting the project.

*Maintained with ❤️ in Kleve • Status: March 2026*
