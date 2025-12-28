import os
from fastapi import FastAPI
from supabase import create_client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# This allows your Netlify frontend to talk to your Render API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use Environment Variables (Set these on Render.com settings)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://fcmmokhuidixdfgetiab.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-key-here")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"message": "Word Automator API is Live!"}

@app.get("/rules")
def get_rules():
    # This fetches rules from your Supabase cloud table
    response = supabase.table("rules").select("*").execute()
    return response.data

@app.post("/rules")
async def add_rule(rule: dict):
    # This saves a new rule to Supabase
    response = supabase.table("rules").insert(rule).execute()
    return response.data
