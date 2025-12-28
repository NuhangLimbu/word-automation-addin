import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

# 1. Enable CORS for local testing and Office
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Supabase Config (Ensure these are in Render Env Vars)
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(URL, KEY)

# 3. Path Logic: Look "up" one level from /server to find /dist
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# --- API ROUTES ---
@app.get("/rules")
def get_rules():
    response = supabase.table("rules").select("*").execute()
    return response.data

# --- THE 404 FIX: SERVING THE FRONTEND ---
@app.get("/index.html")
async def serve_index():
    # This sends the actual HTML file to MS Word
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

@app.get("/")
async def serve_root():
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

# Mount the rest of the assets (JS/CSS)
if os.path.exists(DIST_DIR):
    app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="static")