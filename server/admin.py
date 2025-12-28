import streamlit as st
import pandas as pd
import requests

# Replace with your actual Render URL
API_URL = "https://word-automation-addin.onrender.com/rules"

st.set_page_config(page_title="Word Automator Admin", page_icon="📝", layout="wide")

st.title("📝 Word Automator - Admin Dashboard")

# --- SIDEBAR: ADD NEW RULE ---
st.sidebar.header("➕ Add New Rule")
with st.sidebar.form("add_rule_form", clear_on_submit=True):
    new_label = st.text_input("Button Label", placeholder="e.g., Fix 'dont'")
    new_pattern = st.text_input("Word to Find", placeholder="e.g., dont")
    new_replacement = st.text_input("Replace With", placeholder="e.g., don't")
    submit_button = st.form_submit_button("Save Rule")

if submit_button:
    if new_label and new_pattern and new_replacement:
        payload = {"label": new_label, "pattern": new_pattern, "replacement": new_replacement}
        try:
            res = requests.post(API_URL, json=payload)
            if res.status_code in [200, 201]:
                st.sidebar.success(f"Added: {new_label}")
                st.rerun()
            else:
                st.sidebar.error(f"Error: {res.status_code}")
        except Exception as e:
            st.sidebar.error(f"Connection failed: {e}")

# --- MAIN AREA: MANAGE RULES ---
st.subheader("Current Live Rules")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        rules_data = response.json()
        if rules_data:
            df = pd.DataFrame(rules_data)
            display_df = df[['id', 'label', 'pattern', 'replacement']]
            st.table(display_df)
            
            st.divider()
            st.subheader("🗑️ Delete a Rule")
            rule_to_delete = st.selectbox("Select Rule to Remove", options=df['id'].tolist(), 
                                          format_func=lambda x: f"ID {x}: {df[df['id']==x]['label'].values[0]}")
            
            if st.button("Confirm Delete"):
                delete_res = requests.delete(f"{API_URL}/{rule_to_delete}")
                if delete_res.status_code == 200:
                    st.success("Rule deleted!")
                    st.rerun()
        else:
            st.write("No rules found.")
except Exception as e:
    st.error(f"API Error: {e}")
