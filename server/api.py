# --- SERVING THE FRONTEND ---

# 1. Mount the static files (CSS, JS, Images) FIRST
if os.path.exists(DIST_DIR):
    # We mount this to /assets or specific folders if needed, 
    # but mounting to root works if we handle the index file carefully.
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

# 2. Explicitly serve index.html for the root
@app.get("/")
async def serve_root():
    index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": f"Frontend build not found at {index_path}. Check Render build logs."}

# 3. Catch-all for React Routing (Optional but helpful)
@app.get("/{full_path:path}")
async def serve_any(full_path: str):
    file_path = os.path.join(DIST_DIR, full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    # Fallback to index.html for SPA routing
    return FileResponse(os.path.join(DIST_DIR, "index.html"))