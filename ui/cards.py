import streamlit as st
from utils.social import social_share_links
from utils.tiktok import generate_tiktok_script

def render_article(article):
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
