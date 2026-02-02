import requests
import os

VT_API_KEY = os.getenv("VT_API_KEY")
VT_BASE = "https://www.virustotal.com/api/v3"

def lookup_vt(ioc):
    if not VT_API_KEY:
        return None

    headers = {"x-apikey": VT_API_KEY}

    if "." in ioc and ioc.replace(".", "").isdigit():
        url = f"{VT_BASE}/ip_addresses/{ioc}"
    elif "." in ioc:
        url = f"{VT_BASE}/domains/{ioc}"
    else:
        url = f"{VT_BASE}/files/{ioc}"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None

        stats = r.json()["data"]["attributes"]["last_analysis_stats"]
        return stats
    except Exception:
        return None
