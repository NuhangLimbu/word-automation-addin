from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# ... other imports ...

app = FastAPI()

# ADD THIS MIDDLEWARE TO FIX THE CSP BLOCKS
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # This header allows Word to run your scripts and talk to your AI
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' https://python-3-cxjw.onrender.com; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://appsforoffice.microsoft.com; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' https://generativelanguage.googleapis.com https://*.supabase.co; "
        "frame-ancestors 'self' https://*.officeapps.live.com https://*.office.com;"
    )
    return response

# Ensure CORS is still there
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)