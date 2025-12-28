import os
import httpx
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()

# 1. Enable CORS
# Essential for MS Word to allow the Task Pane to talk to this Python API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Environment Variables & Supabase Config
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("CRITICAL: Supabase environment variables are missing!")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. Path Logic for Monorepo
# Finds the /dist folder (React) sitting one level above the /server folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# --- API ROUTES ---

@app.get("/rules")
def get_rules():
    if not supabase:
        return {"error": "Supabase not configured."}
    try:
        response = supabase.table("rules").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

# SECURE AI PROXY ROUTE
# This handles the summarization so your Gemini Key stays hidden on Render
@app.post("/api/summarize")
async def proxy_summarize(request: Request):
    data = await request.json()
    user_text = data.get("text")
    
    if not GEMINI_API_KEY:
        return {"error": "Gemini API Key is not set in Render Environment Variables."}

    model_id = "gemini-2.0-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": f"Summarize this text concisely for a Word document: {user_text}"}]}]
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=20.0)
            return response.json()
        except Exception as e:
            return {"error": f"AI Request failed: {str(e)}"}

# --- SERVING THE FRONTEND ---

@app.get("/index.html")
async def serve_index():
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

@app.get("/")
async def serve_root():
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Python API is running, but React 'dist' folder was not found. Check build logs."}

# Mount static files (JS/CSS) last
if os.path.exists(DIST_DIR):
    app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="static")