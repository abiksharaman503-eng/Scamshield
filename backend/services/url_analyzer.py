"""Static URL analysis. It NEVER fetches the URL, so the user's server can't be lured to a malicious page."""
import re
from ml.features import parse, SUSPICIOUS_TLDS, SHORTENERS, KEYWORDS
from ml.model import predict_url
from .risk_engine import sig, combine

OFFICIAL = {
    "paypal": ["paypal.com"], "amazon": ["amazon.com", "amazon.in", "amazon.co.uk"],
    "google": ["google.com", "google.co.in"], "microsoft": ["microsoft.com", "live.com", "office.com"],
    "apple": ["apple.com", "icloud.com"], "netflix": ["netflix.com"], "sbi": ["sbi.co.in", "onlinesbi.sbi", "sbicard.com"],
    "hdfc": ["hdfcbank.com"], "icici": ["icicibank.com"], "paytm": ["paytm.com"], "phonepe": ["phonepe.com"],
    "flipkart": ["flipkart.com"], "facebook": ["facebook.com"], "instagram": ["instagram.com"],
    "whatsapp": ["whatsapp.com"], "irctc": ["irctc.co.in"], "gpay": ["pay.google.com"],
}
TWO_PART_TLDS = {"co.in", "co.uk", "com.au", "gov.in", "org.in", "co.nz", "com.br", "ac.in", "gov.uk"}
LEET = str.maketrans({"0": "o", "1": "l", "3": "e", "5": "s", "@": "a", "$": "s"})


def registered_domain(host: str) -> str:
    parts = host.split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in TWO_PART_TLDS:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def _edit1(a: str, b: str) -> bool:
    """True if a and b differ by at most one edit (and aren't identical)."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    s, l = (a, b) if len(a) < len(b) else (b, a)
    return any(l[:i] + l[i + 1:] == s for i in range(len(l)))


def analyze_url(url: str) -> dict:
    p = parse(url)
    host = (p.hostname or "").lower()
    signals: list[dict] = []
    trusted = False

    if not host or "." not in host:
        return combine([sig("invalid", 0.3, "This doesn't look like a valid web address.")])

    reg = registered_domain(host)
    labels = host.split(".")
    tld = labels[-1]

    # Impersonation: brand name appears, but the real domain isn't the brand's
    flat = host.translate(LEET)
    for brand, domains in OFFICIAL.items():
        if reg in domains:
            trusted = True
            break
        tokens = re.split(r"[-.]", flat)
        # exact word, or brand glued to a pressure word (paypalsecure). 'pineapple' must not match 'apple'.
        if any(t == brand or (brand in t and any(k in t for k in KEYWORDS)) for t in tokens):
            signals.append(sig("brand_impersonation", 0.6,
                               f"The address uses the name '{brand}', but the real {brand.title()} website is {domains[0]}."))
            break
        near = next((t for t in tokens if len(t) > 3 and _edit1(t, brand)), None)
        if near:
            signals.append(sig("lookalike", 0.55, f"'{near}' is a near-copy of '{brand}', a common trick to fool people."))
            break

    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        signals.append(sig("ip_host", 0.5, "The link uses a raw IP address instead of a website name."))
    if "@" in url.split("?")[0]:
        signals.append(sig("at_symbol", 0.4, "An '@' in a link can hide the real destination."))
    if "xn--" in host:
        signals.append(sig("punycode", 0.45, "The address uses look-alike foreign characters (punycode)."))
    if tld in SUSPICIOUS_TLDS:
        signals.append(sig("bad_tld", 0.3, f"'.{tld}' addresses are frequently used in scams."))
    if host in SHORTENERS:
        signals.append(sig("shortener", 0.3, "This is a shortened link, so the real destination is hidden."))
    if p.scheme != "https":
        signals.append(sig("no_https", 0.2, "The site does not use an encrypted (HTTPS) connection."))
    if len(labels) - len(reg.split(".")) >= 3:
        signals.append(sig("many_subdomains", 0.3, "The address has many sub-parts, which is used to mimic real sites."))
    if host.count("-") >= 3:
        signals.append(sig("hyphens", 0.25, "Many hyphens in the domain are common in fake sites."))
    kw = [k for k in KEYWORDS if k in (host + p.path).lower()]
    if len(kw) >= 2 and not trusted:
        signals.append(sig("keywords", 0.25, f"The link contains pressure words such as {', '.join(kw[:3])}."))
    if len(url) > 100:
        signals.append(sig("long_url", 0.15, "The link is unusually long."))
    if p.port and p.port not in (80, 443):
        signals.append(sig("odd_port", 0.25, f"The link uses an unusual port ({p.port})."))
    if re.search(r"\.(apk|exe|scr|msi|bat|zip)$", p.path or "", re.I):
        signals.append(sig("download", 0.45, "The link downloads a file directly. Scam links often install malware."))

    result = combine(signals, ml_prob=predict_url(url), trusted=trusted)
    result.update({"host": host, "registered_domain": reg, "input": url})
    result["notes"] = ["Domain age, blocklist and redirect checks need a threat-intel provider. See README."]
    return result