import requests

OTX_BASE = "https://otx.alienvault.com/api/v1/indicators"

def lookup_otx(ioc):
    if "." in ioc and ioc.replace(".", "").isdigit():
        url = f"{OTX_BASE}/IPv4/{ioc}/general"
    elif "." in ioc:
        url = f"{OTX_BASE}/domain/{ioc}/general"
    else:
        url = f"{OTX_BASE}/file/{ioc}/general"

    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None

        data = r.json()
        return {
            "pulse_count": data.get("pulse_info", {}).get("count", 0),
            "reputation": data.get("reputation", "unknown"),
            "confidence": "high" if data.get("pulse_info", {}).get("count", 0) > 5 else "low"
        }
    except Exception:
        return None
