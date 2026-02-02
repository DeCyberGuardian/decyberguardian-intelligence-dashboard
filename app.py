# app.py
import streamlit as st

from src.feeds import fetch_feeds, RSS_FEEDS
from src.styles import inject_css
from src.cards import render_article
from src.ui.side_panel import render_side_panel

from src.enrichment.otx import lookup_otx
from src.enrichment.virustotal import lookup_vt
from src.mitre.tagger import mitre_tags

# -------------------------------------------------
# App State
# -------------------------------------------------
if "selected_article" not in st.session_state:
    st.session_state.selected_article = None

# -------------------------------------------------
# Page Config + Styles
# -------------------------------------------------
st.set_page_config(
    page_title="DeCyberGuardian Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# -------------------------------------------------
# Sidebar — IOC Intelligence Panel
# -------------------------------------------------
st.sidebar.title("🛡️ DeCyberGuardian")
st.sidebar.markdown("**Cyber Threat Intelligence Dashboard**")
st.sidebar.markdown("---")
st.sidebar.subheader("🧪 IOC Intelligence Panel")

ioc = st.sidebar.text_input(
    "IP / Domain / Hash",
    placeholder="8.8.8.8 | example.com | SHA256"
)

if ioc:
    st.sidebar.markdown("### 🔍 Analysis Results")

    # AlienVault OTX
    otx = lookup_otx(ioc)
    if otx:
        st.sidebar.success(
            f"**AlienVault OTX**\n\n"
            f"- Pulses: {otx.get('pulse_count', 0)}\n"
            f"- Confidence: {otx.get('confidence', 'N/A')}"
        )
    else:
        st.sidebar.warning("No AlienVault OTX data.")

    # VirusTotal
    vt = lookup_vt(ioc)
    if vt:
        st.sidebar.info(
            f"**VirusTotal**\n\n"
            f"- Malicious: {vt.get('malicious', 0)}\n"
            f"- Suspicious: {vt.get('suspicious', 0)}\n"
            f"- Harmless: {vt.get('harmless', 0)}"
        )
    else:
        st.sidebar.warning("VirusTotal data unavailable.")

    # MITRE ATT&CK Mapping
    mitre = mitre_tags(ioc)
    if mitre:
        st.sidebar.markdown("### 🎯 MITRE ATT&CK")
        for m in mitre:
            st.sidebar.code(m)

# -------------------------------------------------
# Sidebar — Filters
# -------------------------------------------------
st.sidebar.markdown("---")

keyword = st.sidebar.text_input(
    "🔍 Filter by Keyword",
    placeholder="Ransomware, CVE, APT..."
)

sources = st.sidebar.multiselect(
    "🗂️ Select Sources",
    options=list(RSS_FEEDS.keys()),
    default=list(RSS_FEEDS.keys())
)

# -------------------------------------------------
# Main Layout (SOC View)
# -------------------------------------------------
st.title("📡 DeCyberGuardian Intelligence Dashboard")
st.markdown("Real-time cybersecurity intelligence for Blue Teams & CTI Analysts.")

articles = fetch_feeds()

if keyword:
    articles = [
        a for a in articles
        if keyword.lower() in a["title"].lower()
        or keyword.lower() in a["summary"].lower()
    ]

articles = [a for a in articles if a["source"] in sources]

left, right = st.columns([3, 2])

with left:
    for idx, article in enumerate(articles):
        if st.button("🔍 Analyze", key=f"analyze_{idx}"):
            st.session_state.selected_article = article

        render_article(article, idx)

with right:
    render_side_panel(st.session_state.selected_article)
