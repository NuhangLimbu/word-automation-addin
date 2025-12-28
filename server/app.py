import streamlit as st
import requests

API_URL = "https://word-automation-addin.onrender.com/rules"

st.title("🛡️ Rule Manager")

with st.form("new_rule"):
    find_text = st.text_input("Text to Find")
    replace_text = st.text_input("Replace With")
    submit = st.form_submit_button("Add Rule")

    if submit:
        payload = {"find_text": find_text, "replace_text": replace_text, "category": "Auto"}
        res = requests.post(API_URL, json=payload)
        if res.status_code == 200:
            st.success("Rule added to Cloud!")
        else:
            st.error("Failed to connect.")

st.subheader("Current Cloud Rules")
rules = requests.get(API_URL).json()
st.table(rules)