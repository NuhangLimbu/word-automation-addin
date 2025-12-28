import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS so your React Frontend and Streamlit can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from Render Environment Variables
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

# Data model for the Rule
class Rule(BaseModel):
    label: str
    pattern: str
    replacement: str

@app.get("/")
def home():
    return {"message": "Word Automator API is Live!"}

# GET all rules (Used by Word Add-in and Admin Dashboard)
@app.get("/rules")
def get_rules():
    response = supabase.table("rules").select("*").execute()
    return response.data

# POST a new rule (Used by Admin Dashboard)
@app.post("/rules")
def add_rule(rule: Rule):
    response = supabase.table("rules").insert(rule.dict()).execute()
    return response.data

# DELETE a rule (Used by Admin Dashboard)
@app.delete("/rules/{rule_id}")
def delete_rule(rule_id: int):
    response = supabase.table("rules").delete().eq("id", rule_id).execute()
    return {"status": "success", "message": f"Rule {rule_id} deleted"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)