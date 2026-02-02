MITRE_MAPPING = {
    "ransomware": ("T1486", "Data Encrypted for Impact"),
    "phishing": ("T1566", "Phishing"),
    "credential": ("T1555", "Credentials from Password Stores"),
    "c2": ("T1071", "Application Layer Protocol"),
    "command and control": ("T1071", "Application Layer Protocol"),
    "lateral movement": ("T1021", "Remote Services"),
    "persistence": ("T1547", "Boot or Logon Autostart Execution"),
    "exfiltration": ("T1041", "Exfiltration Over C2 Channel"),
    "privilege escalation": ("T1068", "Exploitation for Privilege Escalation"),
    "zero-day": ("T1203", "Exploitation for Client Execution"),
    "exploit": ("T1203", "Exploitation for Client Execution"),
}

def mitre_tags(text: str):
    text = text.lower()
    tags = set()

    for keyword, (tid, name) in MITRE_MAPPING.items():
        if keyword in text:
            tags.add(f"{tid} — {name}")

    return sorted(tags)
