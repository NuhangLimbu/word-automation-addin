import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. SECURITY MIDDLEWARE (Fixes "Refused to Connect" & "Blank Screen")
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Allows Word to embed your site and lets your app talk to AI services
    csp_policy = (
        "default-src 'self' https://*.onrender.com; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://appsforoffice.microsoft.com; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' https://generativelanguage.googleapis.com https://*.supabase.co; "
        "frame-ancestors 'self' https://*.officeapps.live.com https://*.office.com https://office.live.com;"
    )
    
    response.headers["Content-Security-Policy"] = csp_policy
    
    # Explicitly allow framing by removing the block header
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]
        
    return response

# 2. CORS SETTINGS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. PATH LOGIC
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# 4. SERVING FRONTEND FILES
if os.path.exists(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

@app.get("/")
async def serve_index():
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Ensure 'npm run build' was successful."}

# Catch-all for React routing
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    file_path = os.path.join(DIST_DIR, full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(DIST_DIR, "index.html"))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)