import streamlit as st
import xml.etree.ElementTree as ET
import json
import pandas as pd
import io

st.title("🆔 Regestverlinkung: Error Reporter")

col1, col2 = st.columns(2)
with col1:
    xml_file = st.file_uploader("Upload XML File", type=["xml"])
with col2:
    json_file = st.file_uploader("Upload Mapping (JSON)", type=["json"])

def process_with_errors(xml_file, target_numbers):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = ""
    if "}" in root.tag:
        ns = root.tag.split("}")[0] + "}"
    
    mismatched_data = []
    total_count = 0
    match_count = 0
    
    for ref_element in root.findall(f".//{ns}ref"):
        total_count += 1
        target_id = (ref_element.get("target") or ref_element.get("entity") or "").strip()
        original_text = (ref_element.text or "").strip()
        
        # Mapping Logic
        mapping_group = target_numbers.get(target_id, {})
        corresponding_number = mapping_group.get(original_text)
        
        if corresponding_number:
            ref_element.set('to', corresponding_number)
            ref_element.set('n', 'regest-linked')
            match_count += 1
        else:
            # Only add to this list if it FAILED
            mismatched_data.append({
                "XML_Line_Estimate": "N/A", # ElementTree doesn't easily track line numbers
                "Target_ID": target_id,
                "Text_Content": original_text,
                "Reason": "ID not in JSON" if target_id not in target_numbers else "Text mismatch for this ID"
            })

    # Prepare modified XML
    xml_out = io.BytesIO()
    tree.write(xml_out, encoding="utf-8", xml_declaration=True)
    
    # Create DataFrame of ONLY errors
    error_df = pd.DataFrame(mismatched_data)
    
    return xml_out.getvalue(), error_df, total_count, match_count

if xml_file and json_file:
    try:
        target_numbers = json.load(json_file)
        xml_bytes, error_df, total, matches = process_with_errors(xml_file, target_numbers)
        
        # Display Stats
        st.metric("Total Tags Found", total)
        st.metric("Successfully Linked", matches, delta=matches-total)

        if not error_df.empty:
            st.warning(f"⚠️ Found {len(error_df)} tags that could not be linked.")
            
            # Download Buttons
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("📥 Download Modified XML", xml_bytes, "linked_data.xml", "application/xml")
            with c2:
                csv_errors = error_df.to_csv(index=False).encode('utf-8')
                st.download_button("📑 Download Mismatch Report (CSV)", csv_errors, "missing_tags.csv", "text/csv")
            
            # Show the table of missing items
            st.subheader("Items Missing from Mapping")
            st.dataframe(error_df, use_container_width=True)
        else:
            st.success("🎉 Perfect Match! No missing tags found.")
            st.download_button("📥 Download Modified XML", xml_bytes, "linked_data.xml", "application/xml")
            
    except Exception as e:
        st.error(f"Error: {e}")
            
    except Exception as e:
        st.error(f"Error: {e}")
