import streamlit as st
import json
import zipfile
import xml.etree.ElementTree as ET

st.title("📂 ODS to JSON Converter")
st.write("Convert your spreadsheet into a mapping dictionary for the JSON Modifier tool.")

# 1. File Uploader
uploaded_file = st.file_uploader("Upload an ODS file", type=["ods"])

if uploaded_file is not None:
    try:
        # 2. Read the ODS XML content natively using built-in libraries
        with zipfile.ZipFile(uploaded_file) as z:
            with z.open('content.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()

        data_dict = {}
        current_key = None

        # 3. Streamlined Text Extraction
        # We iterate through every element in the XML document in order.
        # Whenever we find text, we use it to build our key-value pairs sequentially.
        for elem in root.iter():
            if elem.text and elem.text.strip():
                text_value = elem.text.strip()
                
                if current_key is None:
                    # The first text chunk we find becomes the Key (e.g., '783')
                    current_key = text_value
                else:
                    # The next text chunk becomes the Value (e.g., 'fcdb2b4b-...')
                    data_dict[current_key] = text_value
                    current_key = None # Reset to look for the next key

        if not data_dict:
            raise ValueError("No data found. Ensure the ODS file contains valid text entries.")

        st.success(f"✅ Successfully processed {len(data_dict)} entries natively!")

        # 4. JSON Preparation & Download
        json_string = json.dumps(data_dict, indent=4)
        
        st.download_button(
            label="📥 Download JSON Dictionary",
            data=json_string,
            file_name="converted_dict.json",
            mime="application/json"
        )

        # 5. Preview the data
        with st.expander("Preview Dictionary Content"):
            st.json(data_dict)

    except Exception as e:
        st.error(f"Error processing file: {e}")
