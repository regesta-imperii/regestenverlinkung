import streamlit as st
import xml.etree.ElementTree as ET
import csv
import io
from collections import defaultdict

st.title("✂️ Kurztiteln Extraktion")

uploaded_file = st.file_uploader("Upload XML File", type=["xml"])

if uploaded_file:
    # --- PROCESSING LOGIC ---
    tree = ET.parse(uploaded_file)
    root = tree.getroot()
    xref_elements = root.findall('.//xref')
    author_book_count = defaultdict(int)

    for xref_element in xref_elements:
        hi_elements = xref_element.findall('./hi')
        if hi_elements:
            author = ' '.join([hi.text.strip() for hi in hi_elements if hi.text])
            book_title = hi_elements[-1].tail.strip(',') if hi_elements[-1].tail else ''
            author_book = f"{author.strip()}, {book_title.strip()}"
        else:
            author_book = xref_element.text.strip() if xref_element.text else 'Unknown'
        
        author_book_count[author_book] += 1

    # --- CSV PREPARATION ---
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Author_Book', 'Count'])
    for key, value in author_book_count.items():
        writer.writerow([key, value])

    # --- DOWNLOAD BUTTON ---
    st.success("Done! You can now download your file below.")
    st.download_button(
        label="📥 Download CSV Results",
        data=output.getvalue(),
        file_name="author_book_counts.csv",
        mime="text/csv"
    )
