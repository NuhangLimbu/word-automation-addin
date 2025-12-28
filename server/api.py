import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel

app = FastAPI()

# 1. Enable CORS
# Essential for MS Word to allow the Task Pane to talk to this Python API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development; narrow this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Supabase Config (Safe Fetching)
# We fetch by LABEL (Key), not the actual secret value
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Safety Check: Prevents the "NoneType" crash you had earlier
if not SUPABASE_URL or not SUPABASE_KEY:
    print("CRITICAL: Supabase environment variables are missing!")
    supabase = None
else:
    # Initialize the client only if variables exist
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 3. Path Logic for Monorepo
# Finds the /dist folder (React) sitting outside the /server folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# --- API ROUTES ---

@app.get("/rules")
def get_rules():
    if not supabase:
        return {"error": "Supabase not configured in Render environment variables."}
    try:
        # Fetches your automation rules from Supabase
        response = supabase.table("rules").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

# --- SERVING THE FRONTEND (For MS Word Task Pane) ---

@app.get("/index.html")
async def serve_index():
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

@app.get("/")
async def serve_root():
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Python API is running, but React 'dist' folder was not found."}

# Mount static files (JS/CSS) last
if os.path.exists(DIST_DIR):
    app.mount("/", StaticFiles(directory=DIST_DIR, html=True), name="static")