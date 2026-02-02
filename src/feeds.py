# feeds.py
import feedparser
from html import unescape
import streamlit as st
from datetime import datetime

from src.mitre.tagger import mitre_tags

RSS_FEEDS = {
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "CISA Advisories": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "The DFIR Report": "https://thedfirreport.com/feed/",
    "CrowdStrike": "https://www.crowdstrike.com/blog/feed/",
    "Palo Alto Unit 42": "https://unit42.paloaltonetworks.com/feed/",
    "Mandiant": "https://cloud.google.com/blog/products/identity-security/rss",
    "Recorded Future": "https://www.recordedfuture.com/feed/",
    "GreyNoise": "https://www.greynoise.io/blog/rss.xml"
}

def normalize_date(entry):
    try:
        return entry.get("published", "") or entry.get("updated", "")
    except Exception:
        return "N/A"


def normalize_mitre(mitre_raw):
    """
    Ensures MITRE data is always a dict:
    {
        "tactics": [...],
        "techniques": [...]
    }
    """
    tactics = set()
    techniques = set()

    if isinstance(mitre_raw, list):
        for item in mitre_raw:
            tactics.add(item.get("tactic"))
            techniques.add(item.get("technique"))

    return {
        "tactics": sorted(t for t in tactics if t),
        "techniques": sorted(t for t in techniques if t)
    }


@st.cache_data(ttl=900)
def fetch_feeds():
    articles = []

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                title = unescape(entry.get("title", "No title"))
                summary = unescape(
                    entry.get("summary", entry.get("description", ""))
                )
                link = entry.get("link", "")
                published = normalize_date(entry)

                full_text = f"{title} {summary}"

                articles.append({
                    "source": source,
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                    # 🔥 Advanced fields
                    "mitre": normalize_mitre(mitre_tags(full_text)),
                    "iocs": {},            # populated next step
                    "confidence": None     # scoring later
                })

        except Exception as e:
            continue

    return articles
