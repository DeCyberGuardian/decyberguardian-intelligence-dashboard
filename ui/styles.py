import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    body { background-color: #0e1117; color: #eaeaea; }
    h1, h2, h3 { color: #008080; }
    a { color: #FFD700; text-decoration: none; }
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
    small { color: #9da5b4; }
    </style>
    """, unsafe_allow_html=True)
