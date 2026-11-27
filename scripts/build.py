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
HEADERS = {"User-Agent": "Mozilla/5.0 TechRZN-Bot/1.3"}

MAX_DOMAIN_LEN = 80
MAX_ENTRIES_PER_LIST = 1_200_000
MAX_WORKERS = 6
REQUEST_TIMEOUT = (5, 25)

DOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+$")


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

    # Protokoll, Pfad und Adblock-Syntax entfernen
    if "://" in line:
        line = line.split("://", 1)[1]
    line = line.split("/", 1)[0]
    line = line.replace("^$important", "").replace("||", "").replace("^", "")
    line = line.removeprefix("*.")
    line = line.replace("*", "")

    if line.startswith("www."):
        line = line[4:]

    line = line.strip(".")
    if not line or len(line) > MAX_DOMAIN_LEN or "." not in line:
        return None

    if not DOMAIN_RE.match(line):
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


def main() -> None:
    started_at = time.monotonic()
    timestamp = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")
    print(f"🚀 TechRZN Update gestartet: {timestamp}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(WL_DIR, exist_ok=True)

    whitelist = load_whitelist(LOCAL_WHITELIST)
    print(f"🛡️ Whitelist geladen: {len(whitelist)} Domains")

    session = create_session()

    try:
        for cat_name, src_path in CATEGORIES.items():
            if not os.path.exists(src_path):
                print(f"⚠️ Überspringe {cat_name} ({src_path} fehlt)")
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
                continue

            if not urls:
                print(f"⚠️ Keine URLs in {src_path}")
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
                output_path = os.path.join(OUTPUT_DIR, f"techrzn_{cat_name}.txt")
                sorted_domains = sorted(category_domains)

                if existing_domains_match(output_path, sorted_domains):
                    print(f"⏭️ {cat_name}: Keine Aenderungen ({len(sorted_domains)} Domains).")
                    continue

                try:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(f"! TechRZN - {cat_name.upper()}\n")
                        f.write(f"! Stand: {timestamp}\n")
                        f.write(f"! Eintraege: {len(sorted_domains)}\n\n")
                        for d in sorted_domains:
                            f.write(f"||{d}^\n")
                    print(f"✅ {cat_name}: {len(sorted_domains)} Domains -> {output_path}")
                except Exception as e:
                    print(f"❌ Fehler beim Schreiben von {output_path}: {e}")
    finally:
        session.close()

    elapsed = time.monotonic() - started_at
    print(f"🏁 Fertig in {elapsed:.1f}s.")


if __name__ == "__main__":
    main()
