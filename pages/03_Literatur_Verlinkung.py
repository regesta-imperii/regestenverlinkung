import streamlit as st
import csv
import xml.etree.ElementTree as ET
import io
from collections import Counter

st.title("🔗 Literaturverlinkung")

# 1. File Uploaders
col1, col2 = st.columns(2)
with col1:
    csv_file = st.file_uploader("Upload Catalog (CSV)", type=["csv"])
with col2:
    xml_file = st.file_uploader("Upload Target XML", type=["xml"])

def remove_extra_whitespace(text):
    return " ".join(text.split())

if csv_file and xml_file:
    # Step 1: Create dictionary from CSV
    # We use io.StringIO to read the uploaded bytes as text
    csv_dict = {}
    content = csv_file.getvalue().decode("latin1")
    reader = csv.reader(io.StringIO(content))
    next(reader, None)  # skip header
    
    for row in reader:
        if len(row) < 2 or not row[0].strip():
            continue
        author_book = row[0].strip().rstrip(",")
        catalog_number = row[1].strip() if row[1].strip() else ""
        csv_dict[author_book] = catalog_number

    # Step 2: Parse the XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Step 3: Extract and Match
    linked_count = 0
    unmatched_entries = []

    for xref in root.findall(".//xref"):
        xref_text = remove_extra_whitespace("".join(xref.itertext()))
        xref_text_norm = xref_text.lower()

        matched = False
        for author_book, catalog_number in csv_dict.items():
            if author_book.lower() in xref_text_norm:
                xref.tag = "ref"
                xref.set("n", "linked")
                xref.set("target", catalog_number)
                linked_count += 1
                matched = True
                break

        if not matched:
            unmatched_entries.append(xref_text)
        # --- UI RESULTS & DOWNLOADS ---
    st.divider()
    st.subheader("Processing Results")
    
    c1, c2 = st.columns(2)
    c1.metric("Successfully Linked", linked_count)
    c2.metric("Unmatched Entries", len(unmatched_entries))

    # Zählen der nicht gefundenen Einträge
    unmatched_counts = Counter(unmatched_entries)

    # --- CSV PREPARATION (für den Download) ---
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Unmatched_Entry_Text', 'Count'])
    
    for entry, count in unmatched_counts.items():
        writer.writerow([entry, count])

    # Download Updated XML
    xml_buffer = io.BytesIO()
    tree.write(xml_buffer, encoding="utf-8", xml_declaration=True)
    st.download_button(
        label="📥 Download Linked XML",
        data=xml_buffer.getvalue(),
        file_name="linked_output.xml",
        mime="application/xml"
    )

    # Download Unmatched Log als echte CSV
    st.download_button(
        label="⚠️ Download Unmatched Log (.csv)",
        data=output.getvalue(),
        file_name="unmatched_log.csv",
        mime="text/csv"
    )
