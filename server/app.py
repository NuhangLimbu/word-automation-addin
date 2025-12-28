import streamlit as st
import sqlite3
import pandas as pd

# Connect to the shared database in the root folder
DB_PATH = '../database.sqlite'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create the rules table
    c.execute('''CREATE TABLE IF NOT EXISTS rules 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  find TEXT NOT NULL, 
                  replace TEXT NOT NULL, 
                  category TEXT)''')
    # Create a logs table to track usage later
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  action TEXT, 
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

st.set_page_config(page_title="Word Automator Admin", layout="wide")
init_db()

st.title("🛠️ Word Automator: Admin Control")

tab1, tab2 = st.tabs(["Manage Rules", "Usage Logs"])

with tab1:
    st.header("Correction Rules")
    
    # Form to add a new rule
    with st.expander("➕ Add New Rule"):
        with st.form("rule_form"):
            col1, col2 = st.columns(2)
            find_text = col1.text_input("Find this text:")
            replace_text = col2.text_input("Replace with:")
            category = st.selectbox("Category", ["Grammar", "Style", "Legal", "Branding"])
            
            if st.form_submit_button("Save Rule"):
                if find_text and replace_text:
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO rules (find, replace, category) VALUES (?, ?, ?)", 
                                 (find_text, replace_text, category))
                    conn.commit()
                    conn.close()
                    st.success(f"Rule added: {find_text} -> {replace_text}")
                    st.rerun()
                else:
                    st.error("Please fill in both fields.")

    # Table to view and edit rules
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM rules", conn)
    conn.close()

    if not df.empty:
        st.subheader("Active Rules")
        st.info("You can edit the table below directly and save changes.")
        edited_df = st.data_editor(df, num_rows="dynamic", key="editor")
        
        if st.button("Update All Rules"):
            conn = sqlite3.connect(DB_PATH)
            edited_df.to_sql("rules", conn, if_exists="replace", index=False)
            conn.close()
            st.success("Database updated!")
    else:
        st.write("No rules found. Add your first rule above!")

with tab2:
    st.header("Activity History")
    conn = sqlite3.connect(DB_PATH)
    logs_df = pd.read_sql("SELECT * FROM logs ORDER BY timestamp DESC", conn)
    conn.close()
    st.dataframe(logs_df, use_container_width=True)