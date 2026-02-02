# src/ioc/extractor.py
import re
from src.ioc.extractor import extract_iocs


IOC_PATTERNS = {
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b[a-zA-Z0-9.-]+\.(com|net|org|io|ru|cn|info)\b",
    "url": r"https?://[^\s]+",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
}

def extract_iocs(text):
    "iocs": extract_iocs(full_text)

    for ioc_type, pattern in IOC_PATTERNS.items():
        matches = set(re.findall(pattern, text))
        if matches:
            iocs[ioc_type] = sorted(matches)

    return iocs
