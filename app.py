import streamlit as st
import requests
import json

# Streamlit App Title
st.title("🚀 Langflow Astra API - Crop Advisory System")

# User input
user_input = st.text_input("💬 Enter your crop query:", "Rust on wheat leaves in Pune, what treatment?")

# API endpoint & headers
url = "https://api.langflow.astra.datastax.com/lf/3e1ee4ba-21f0-4b05-a479-14553904059c/api/v1/run/9c5bad27-1fa5-4e72-846f-1d82606dcb2c"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer AstraCS:WDDhDcpAzwjvdBHqwyEnKTOO:47323d00c4a6d8bcbafe021b1db76a358c9cf7e3a5a6b94f1412799ebbc06c07"
}

# Button to send input
if st.button("Send to Langflow", type="primary"):
    payload = {
        "input_value": user_input,
        "output_type": "chat",
        "input_type": "chat"
    }
    
    with st.spinner("Analyzing crop health..."):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Robust text extraction with fallback paths
            text_output = None
            
            # Common Langflow response paths
            paths = [
                lambda r: r["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"],
                lambda r: r["outputs"][0]["text"],
                lambda r: r.get("text", ""),
                lambda r: r["outputs"][0]["results"]["text"] if r["outputs"] else ""
            ]
            
            for path in paths:
                try:
                    text_output = path(result)
                    if text_output:
                        break
                except (KeyError, IndexError, TypeError):
                    continue
            
            if text_output:
                st.success("✅ Advisory Generated")
                st.markdown(text_output)
            else:
                st.warning("⚠️ No text output found")
                st.json(result)  # Debug: show full response
                
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Error: {str(e)}")
        except (json.JSONDecodeError, ValueError) as e:
            st.error(f"❠ JSON Parse Error: {str(e)}")
            st.json(response.text if 'response' in locals() else "No response")

# Instructions
with st.expander("📋 How to use"):
    st.write("""
    1. Upload leaf photo or describe symptoms
    2. Add location (city/village)
    3. Click "Send to Langflow"
    4. Get instant treatment recommendations
    """)
