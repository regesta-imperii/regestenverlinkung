import streamlit as st

# 1. Page Configuration (This sets the browser tab name and icon)
st.set_page_config(
    page_title="Regest - Linking Workflow für Regesta Imperii",
    page_icon="🛠️",
    layout="centered"
)

# 2. Main Title and Intro
st.title("🛠️ Regestverlinkung")
st.markdown("""
Willkommen! Hier ist eine Sammlung von Tools, die darauf ausgelegt sind, Regestverlinkung zu automatisieren.
""")

st.divider()

# 3. User Guide (Briefly explaining what each sidebar tool does)
st.subheader("Available Tools")

col1, col2 = st.columns(2)

with col1:
    st.info("**1. Short Titles**\n\nExtrahiert Kurztiteln direct aus XML-Datei.")
    st.info("**2. Literaturverlinkung**\n\nOrdnet XML-Tags mit Kurztiteln.csv - Katalog ab, um verknüpfte Referenzen zu erstellen.")

with col2:
    st.info("**3. Regestverlinkung**\n\nAktualisiert Regestennumern mithilfe von allregestdict.json.")
    st.info("**4. ODS to JSON**\n\nKonvertiert (.ods)-Dateien in JSON-dict für die Verwendung in Tool#3.")

st.divider()

# 4. Instructions for the Coworker
st.warning("👈 **Getting Started:** Um zu beginnen, wählen Sie ein Werkzeug aus.")

st.caption("Tipp: Wenn die Seitenleiste versteckt ist, klicke auf den kleinen Pfeil (>) oben links auf dem Bildschirm.")