from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# THIS IS THE FIX FOR THE BLANK SCREEN
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    # This allows the app to load inside Word's frame and talk to your APIs
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' https://*.onrender.com; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://appsforoffice.microsoft.com; "
        "style-src 'self' 'unsafe-inline'; "
        "connect-src 'self' https://generativelanguage.googleapis.com https://*.supabase.co; "
        "frame-ancestors 'self' https://*.officeapps.live.com https://*.office.com https://office.live.com;"
    )
    return response

# Standard CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)