import streamlit as st
import feedparser
from urllib.parse import quote

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="DeCyberGuardian Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS (Dark Mode + Teal & Gold)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: #eaeaea;
}
h1, h2, h3 {
    color: #008080;
}
a {
    color: #FFD700;
    text-decoration: none;
}
.stButton>button {
    background-color: #008080;
    color: white;
    border-radius: 6px;
}
.card {
    background-color: #161b22;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
    border-left: 4px solid #FFD700;
}
small {
    color: #9da5b4;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# RSS Sources
# -----------------------------
RSS_FEEDS = {
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "The DFIR Report": "https://thedfirreport.com/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
    "CISA Advisories": "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews"
}

# -----------------------------
# Helper Functions
# -----------------------------
def fetch_feeds():
    articles = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                "source": source,
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "published": entry.get("published", "N/A")
            })
    return articles


def generate_tiktok_script(title, summary):
    return f"""
Hook (0–5s):
“Blue teamers, this just dropped…”

Context (5–20s):
{title}

Key Insight (20–45s):
{summary[:300]}...

Why It Matters (45–55s):
This impacts defenders, detection logic, and response playbooks.

CTA (55–60s):
Follow DeCyberGuardian for daily CTI insights.
"""


def social_share_links(title, link):
    text = quote(f"{title} | via DeCyberGuardian")
    url = quote(link)
    return {
        "x": f"https://twitter.com/intent/tweet?text={text}&url={url}",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={url}"
    }

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.title("🛡️ DeCyberGuardian")
st.sidebar.markdown("**Cyber Threat Intelligence Dashboard**")

keyword_filter = st.sidebar.text_input(
    "🔍 Filter by Keyword",
    placeholder="Ransomware, Web3, IOC..."
)

selected_sources = st.sidebar.multiselect(
    "🗂️ Select Sources",
    options=list(RSS_FEEDS.keys()),
    default=list(RSS_FEEDS.keys())
)

# -----------------------------
# Main UI
# -----------------------------
st.title("📡 DeCyberGuardian Intelligence Dashboard")
st.markdown("Real-time cybersecurity intelligence for Blue Teams & CTI Analysts.")

articles = fetch_feeds()

# Filtering Logic
if keyword_filter:
    articles = [
        a for a in articles
        if keyword_filter.lower() in a["title"].lower()
        or keyword_filter.lower() in a["summary"].lower()
    ]

articles = [a for a in articles if a["source"] in selected_sources]

# -----------------------------
# Render Articles
# -----------------------------
for article in articles:
    share = social_share_links(article["title"], article["link"])

    st.markdown(f"""
    <div class="card">
        <h3>{article["title"]}</h3>
        <small>{article["source"]} • {article["published"]}</small>
        <p>{article["summary"][:400]}...</p>
        <a href="{article["link"]}" target="_blank">Read full article →</a>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"[Share on X]({share['x']})")
    with col2:
        st.markdown(f"[Share on LinkedIn]({share['linkedin']})")
    with col3:
        if st.button("🎥 Generate TikTok Script", key=article["link"]):
            st.text_area(
                "TikTok Script",
                generate_tiktok_script(article["title"], article["summary"]),
                height=180
            )
