import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for Netlify
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from Environment Variables
URL = os.environ.get("SUPABASE_URL", "https://fcmmokhuidixdfgetiab.supabase.co")
KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

class Rule(BaseModel):
    find_text: str
    replace_text: str
    category: str = "General"

@app.get("/")
def home():
    return {"message": "Word Automator API is Live!"}

@app.get("/rules")
def get_rules():
    response = supabase.table("rules").select("*").execute()
    return response.data

@app.post("/rules")
def add_rule(rule: Rule):
    response = supabase.table("rules").insert(rule.dict()).execute()
    return response.data