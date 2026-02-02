# cards.py
import streamlit as st
from urllib.parse import quote

TIER_1_SOURCES = {
    "CrowdStrike",
    "Mandiant",
    "Recorded Future",
    "Palo Alto Unit 42",
    "GreyNoise"
}

def social_links(title, link):
    text = quote(f"{title} | via DeCyberGuardian")
    url = quote(link)

    return {
        "x": f"https://twitter.com/intent/tweet?text={text}&url={url}",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={url}"
    }

def render_mitre_tags(mitre_data: dict):
    """
    mitre_data format:
    {
        "techniques": [("T1059", "Command and Scripting Interpreter"), ...],
        "tactics": ["Execution", "Persistence"]
    }
    """
    if not mitre_data:
        return

    st.markdown("**MITRE ATT&CK Mapping**")

    if mitre_data.get("tactics"):
        st.markdown(
            " ".join(
                f"`{tactic}`" for tactic in mitre_data["tactics"]
            )
        )

    if mitre_data.get("techniques"):
        for tid, name in mitre_data["techniques"]:
            st.markdown(f"- **{tid}** — {name}")

def render_article(article, idx):
    border = "#FFD700" if article["source"] in TIER_1_SOURCES else "#008080"
    share = social_links(article["title"], article["link"])

    with st.container():
        st.markdown(
            f"""
            <div class="card" style="border-left: 5px solid {border}; padding-left: 12px;">
                <h4>{article["title"]}</h4>
                <small>
                    {article["source"]} • {article["published"]}
                </small>
                <p>{article["summary"][:400]}...</p>
                <a href="{article["link"]}" target="_blank">
                    Read full article →
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        if article.get("mitre"):
            with st.expander("🧠 MITRE ATT&CK Analysis", expanded=False):
                render_mitre_tags(article["mitre"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"[Share on X]({share['x']})")
        with c2:
            st.markdown(f"[Share on LinkedIn]({share['linkedin']})")
        with c3:
            if st.button("🎥 TikTok Script", key=f"tt_{idx}"):
                st.text_area(
                    "Generated Script",
                    f"""Hook (0–5s):
Blue teamers, this just dropped.

Context:
{article['title']}

Why it matters:
{article['summary'][:250]}...

MITRE Lens:
{", ".join(article.get("mitre", {}).get("tactics", []))}

Follow DeCyberGuardian for CTI insights.""",
                    height=180
                )
