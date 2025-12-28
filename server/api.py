import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. THE CRITICAL FIX: Security Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Allows Word to 'frame' your app and allows your app to talk to AI APIs
    csp_policy = (
        "default-src 'self' https://*.onrender.com; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://appsforoffice.microsoft.com; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' https://generativelanguage.googleapis.com https://*.supabase.co; "
        "frame-ancestors 'self' https://*.officeapps.live.com https://*.office.com https://office.live.com;"
    )
    
    response.headers["Content-Security-Policy"] = csp_policy
    
    # FIXES: "Refused to connect" - removes the block on iframes
    if "X-Frame-Options" in response.headers:
        del response.headers["X-Frame-Options"]
        
    return response

# 2. CORS (standard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. STATIC FILES SETUP
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")

if os.path.exists(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

@app.get("/")
async def serve_index():
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Dist folder not found. Build may have failed."}

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