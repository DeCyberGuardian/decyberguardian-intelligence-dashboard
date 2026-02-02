import streamlit as st

def render_side_panel(article):
    if not article:
        st.info("Select an article to analyze")
        return

    st.subheader("🧠 Threat Analysis")

    # MITRE
    st.markdown("### 🎯 MITRE ATT&CK")
    mitre = article.get("mitre", {})

    if mitre.get("tactics"):
        st.markdown("**Tactics**")
        for t in mitre["tactics"]:
            st.code(t)

    if mitre.get("techniques"):
        st.markdown("**Techniques**")
        for t in mitre["techniques"]:
            st.code(t)

    # IOCs
    st.markdown("### 🔍 Indicators of Compromise")
    iocs = article.get("iocs", {})

    if not iocs:
        st.caption("No IOCs detected")
    else:
        for ioc_type, values in iocs.items():
            with st.expander(ioc_type.upper()):
                for v in values:
                    st.code(v)

    # Future export hook
    st.markdown("### 📤 Export")
    st.caption("MISP / SIEM export coming next phase")
