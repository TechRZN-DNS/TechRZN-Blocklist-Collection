from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import os
import re
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- KONFIGURATION ---
CATEGORIES = {
    "ads": "sources/ads.raw",
    "tracking": "sources/tracking.raw",
    "malware": "sources/malware.raw",
    "phishing": "sources/phishing.raw",
    "threat_intel": "sources/threat_intel.raw",
    "fakeshops": "sources/fakeshops.raw",
    "gambling": "sources/gambling.raw",
    "dating": "sources/dating.raw",
    "spam": "sources/spam.raw",
    "fake_science": "sources/fake_science.raw",
    "bypass": "sources/bypass.raw",
    "native_tracker": "sources/native_tracker.raw",
    "popups": "sources/popups.raw",
    "domain_squatting": "sources/domain_squatting.raw",
    "jugendschutz": "sources/jugendschutz.raw",
    "nrd": "sources/newly_registered_domains.raw",
}

OUTPUT_DIR = "blocklists"
WL_DIR = "Whitelists"
LOCAL_WHITELIST = "sources/whitelist.raw"
WHITELIST_OUTPUT_FILE = os.path.join(WL_DIR, "techrzn_whitelist.txt")
HEADERS = {"User-Agent": "Mozilla/5.0 TechRZN-Bot/1.3"}

# False = nur melden/zaehlen, wenn Domains in mehreren Kategorien auftauchen
# True  = jede Domain nur in der ersten passenden Kategorie behalten
DEDUPLICATE_ACROSS_CATEGORIES = False

MAX_DOMAIN_LEN = 80
MAX_ENTRIES_PER_LIST = 1_200_000
MAX_WORKERS = 6
REQUEST_TIMEOUT = (5, 25)

# Offensichtlich lokale, reservierte oder im DNS-Blocklisting unerwuenschte TLDs
BLOCKED_TLDS = {
    "local",
    "localhost",
    "localdomain",
    "lan",
    "home",
    "internal",
    "intranet",
    "corp",
    "arpa",
    "example",
    "invalid",
    "test",
    "onion",
}

# Haeufige Tippfehler bei bekannten Top-Level-Domains (.com, .de, .org, .net, .co, .io)
TYPO_TLDS = {
    "con",
    "cmo",
    "ocm",
    "comm",
    "coom",
    "vom",
    "xom",
    "dom",
    "deu",
    "ogr",
    "ofr",
    "orgg",
    "nett",
    "nte",
    "ent",
    "coo",
    "oi",
}

# TLD: entweder klassisch (2-24 Buchstaben) oder Punycode (xn--...)
DOMAIN_RE = re.compile(
    r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*"
    r"\.(?:xn--[a-z0-9-]{2,59}|[a-z]{2,24})$"
)


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)

    retry = Retry(
        total=3,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(
        pool_connections=MAX_WORKERS * 2,
        pool_maxsize=MAX_WORKERS * 2,
        max_retries=retry,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def normalize_url(url: str) -> str:
    url = url.strip()
    if "jsdelivr.net/gh/" in url:
        url = url.replace("cdn.jsdelivr.net/gh/", "raw.githubusercontent.com/").replace("@latest/", "/main/")
    return url


def clean_domain(line: str) -> str | None:
    line = line.strip().lower()
    if not line or line.startswith(("#", "!", "[", "@@")):
        return None

    # Inline-Kommentare entfernen
    for sep in ("#", "!"):
        if sep in line:
            line = line.split(sep, 1)[0].strip()

    if not line:
        return None

    # Hosts-Zeilen wie "0.0.0.0 domain.tld" oder "127.0.0.1 domain.tld"
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1", "::1"):
        line = parts[1]
    elif len(parts) > 1:
        return None

    # Protokoll, Pfad, Query/Port und Adblock-Syntax entfernen
    if "://" in line:
        line = line.split("://", 1)[1]
    line = line.split("/", 1)[0].split("?", 1)[0].split(":", 1)[0]
    line = line.replace("^$important", "").replace("||", "").replace("^", "")
    line = line.removeprefix("*.")
    line = line.replace("*", "")

    # Mehrfaches "www." am Anfang bereinigen (z. B. "www2." oder "www.www.")
    while line.startswith(("www.", "www2.", "www3.")):
        if line.startswith("www."):
            line = line[4:]
        elif line.startswith(("www2.", "www3.")):
            line = line[5:]

    line = line.strip(".")
    if not line or len(line) > MAX_DOMAIN_LEN or "." not in line:
        return None

    # Doppelte Punkte oder Bindestrich direkt am Label-Rand verwerfen
    if ".." in line or ".-" in line or "-." in line:
        return None

    # Umlaute / Unicode-Domains in Punycode (IDNA) wandeln, falls moeglich
    if not line.isascii():
        try:
            line = line.encode("idna").decode("ascii").lower()
        except Exception:
            return None

    if not DOMAIN_RE.match(line):
        return None

    tld = line.rsplit(".", 1)[-1]
    if tld in BLOCKED_TLDS or tld in TYPO_TLDS:
        return None

    return line


def load_whitelist(path: str) -> set[str]:
    wl = set()
    if not os.path.exists(path):
        return wl

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                d = clean_domain(line)
                if d:
                    wl.add(d)
    except Exception as e:
        print(f"⚠️ Fehler beim Laden der Whitelist ({path}): {e}")
    return wl


def fetch_source(session: requests.Session, url: str, whitelist: set[str], limit: int) -> set[str]:
    found = set()
    fetch_url = normalize_url(url)
    try:
        with session.get(fetch_url, timeout=REQUEST_TIMEOUT, stream=True) as r:
            r.raise_for_status()
            for raw_line in r.iter_lines(decode_unicode=True):
                if raw_line is None:
                    continue
                domain = clean_domain(raw_line)
                if domain and domain not in whitelist:
                    found.add(domain)
                    if len(found) >= limit:
                        break
    except Exception as e:
        print(f"❌ Fehler bei URL {fetch_url}: {e}")
    return found


def existing_domains_match(output_path: str, sorted_domains: list[str]) -> bool:
    if not os.path.exists(output_path):
        return False

    try:
        current_domains = []
        with open(output_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if s.startswith("||") and s.endswith("^"):
                    domain = s[2:-1].strip()
                    if domain:
                        current_domains.append(domain)
        return current_domains == sorted_domains
    except Exception:
        return False


def write_whitelist_file(whitelist: set[str], timestamp: str) -> None:
    if not whitelist:
        return

    sorted_wl = sorted(whitelist)
    if existing_domains_match(WHITELIST_OUTPUT_FILE, sorted_wl):
        print(f"⏭️ Whitelist: Keine Aenderungen ({len(sorted_wl)} Domains).")
        return

    try:
        with open(WHITELIST_OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("! TechRZN - WHITELIST\n")
            f.write(f"! Stand: {timestamp}\n")
            f.write(f"! Eintraege: {len(sorted_wl)}\n\n")
            for d in sorted_wl:
                f.write(f"||{d}^\n")
        print(f"✅ Whitelist: {len(sorted_wl)} Domains -> {WHITELIST_OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Fehler beim Schreiben der Whitelist ({WHITELIST_OUTPUT_FILE}): {e}")


def print_summary(stats: list[tuple[str, int, str]]) -> None:
    if not stats:
        return
    print("\n📊 Kategorie-Zusammenfassung:")
    print(f"{'Kategorie':<18} {'Eintraege':>10}  {'Status'}")
    print("-" * 48)
    for cat_name, count, status in stats:
        print(f"{cat_name:<18} {count:>10}  {status}")
    print("-" * 48)


def main() -> None:
    started_at = time.monotonic()
    timestamp = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")
    print(f"🚀 TechRZN Update gestartet: {timestamp}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(WL_DIR, exist_ok=True)

    whitelist = load_whitelist(LOCAL_WHITELIST)
    print(f"🛡️ Whitelist geladen: {len(whitelist)} Domains")
    write_whitelist_file(whitelist, timestamp)

    seen_domains: set[str] = set()
    cross_category_duplicates = 0
    summary_stats: list[tuple[str, int, str]] = []

    session = create_session()

    try:
        for cat_name, src_path in CATEGORIES.items():
            if not os.path.exists(src_path):
                print(f"⚠️ Überspringe {cat_name} ({src_path} fehlt)")
                summary_stats.append((cat_name, 0, "Quelle fehlt"))
                continue

            try:
                with open(src_path, "r", encoding="utf-8", errors="replace") as f:
                    urls = [
                        line.strip()
                        for line in f
                        if line.strip() and not line.strip().startswith("#")
                    ]
            except Exception as e:
                print(f"❌ Fehler beim Lesen von {src_path}: {e}")
                summary_stats.append((cat_name, 0, "Lesefehler"))
                continue

            if not urls:
                print(f"⚠️ Keine URLs in {src_path}")
                summary_stats.append((cat_name, 0, "Keine URLs"))
                continue

            print(f"📦 Verarbeite Kategorie: {cat_name} ({len(urls)} Quellen)")
            category_domains = set()

            with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(urls))) as executor:
                futures = [
                    executor.submit(fetch_source, session, url, whitelist, MAX_ENTRIES_PER_LIST)
                    for url in urls
                ]
                for future in as_completed(futures):
                    try:
                        domains = future.result()
                        remaining = MAX_ENTRIES_PER_LIST - len(category_domains)
                        if remaining <= 0:
                            break
                        for d in domains:
                            category_domains.add(d)
                            if len(category_domains) >= MAX_ENTRIES_PER_LIST:
                                break
                    except Exception as e:
                        print(f"❌ Fehler bei Quellen-Task in {cat_name}: {e}")

            if category_domains:
                cat_dups = len(category_domains & seen_domains)
                if cat_dups > 0:
                    cross_category_duplicates += cat_dups
                    print(f"🔁 {cat_name}: {cat_dups} Domain(s) bereits in anderen Kategorien vorhanden.")

                if DEDUPLICATE_ACROSS_CATEGORIES:
                    category_domains -= seen_domains

                seen_domains.update(category_domains)

                if not category_domains:
                    print(f"⚠️ {cat_name}: Nach Deduplizierung keine Domains mehr uebrig.")
                    summary_stats.append((cat_name, 0, "Leer nach Deduplizierung"))
                    continue

                output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
                sorted_domains = sorted(category_domains)

                if existing_domains_match(output_path, sorted_domains):
                    print(f"⏭️ {cat_name}: Keine Aenderungen ({len(sorted_domains)} Domains).")
                    summary_stats.append((cat_name, len(sorted_domains), "Unveraendert"))
                    continue

                try:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(f"! TechRZN - {cat_name.upper()}\n")
                        f.write(f"! Stand: {timestamp}\n")
                        f.write(f"! Eintraege: {len(sorted_domains)}\n\n")
                        for d in sorted_domains:
                            f.write(f"||{d}^\n")
                    print(f"✅ {cat_name}: {len(sorted_domains)} Domains -> {output_path}")
                    summary_stats.append((cat_name, len(sorted_domains), "Geschrieben"))
                except Exception as e:
                    print(f"❌ Fehler beim Schreiben von {output_path}: {e}")
                    summary_stats.append((cat_name, len(sorted_domains), "Schreibfehler"))
            else:
                summary_stats.append((cat_name, 0, "Keine Domains"))
    finally:
        session.close()

    print_summary(summary_stats)
    elapsed = time.monotonic() - started_at
    print(
        f"🏁 Fertig in {elapsed:.1f}s | "
        f"Einzigartige Domains gesamt: {len(seen_domains)} | "
        f"Kategorie-Ueberschneidungen: {cross_category_duplicates}"
    )


if __name__ == "__main__":
    main()
