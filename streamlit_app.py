"""Big Block Timer — Streamlit wrapper around index.html.

Run locally:  streamlit run streamlit_app.py
"""

import base64
import re
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent

st.set_page_config(page_title="Big Block Timer", page_icon="⏱️", layout="wide")

# Strip Streamlit's header, toolbar and padding so the timer fills the window
st.html("""
<style>
  header[data-testid="stHeader"], [data-testid="stToolbar"],
  [data-testid="stDecoration"], footer { display: none !important; }
  .stApp, [data-testid="stAppViewContainer"] { background: #0b0a09; }
  .block-container, [data-testid="stMainBlockContainer"] {
    padding: 0 !important; max-width: none !important;
  }
  [data-testid="stVerticalBlock"] { gap: 0 !important; }
  [data-testid="stElementContainer"]:has(> .stHtml) { display: none; }
  iframe { display: block; width: 100vw !important; height: 100vh !important; border: 0; }
  html, body { overflow: hidden; }
</style>
""")


@st.cache_data
def build_page() -> str:
    """Inline the photos as data URIs; the component iframe can't read local files."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    def inline(match: re.Match) -> str:
        data = base64.b64encode((ROOT / match.group(1)).read_bytes()).decode()
        return f'img: "data:image/jpeg;base64,{data}"'

    return re.sub(r'img: "(images/[^"]+\.jpg)"', inline, html)


components.html(build_page(), height=900)
