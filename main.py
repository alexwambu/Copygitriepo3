from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from clone_repo import clone_private_repo

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head><title>GBT Deployment Backend</title></head>
      <body>
        <h1>✅ GBT Deploy Backend is Live</h1>
        <p>Use <code>POST /deploy</code> with JSON payload to trigger a deployment.</p>
      </body>
    </html>
    """

@app.post("/deploy")
async def deploy(request: Request):
    try:
        data = await request.json()
        repo_path = data.get("repo_url")
        domain = data.get("domain")
        logo = data.get("logo")

        if not repo_path:
            return JSONResponse({"status": "error", "message": "Missing repo_url"}, status_code=400)

        result = clone_private_repo(repo_path)

        if result["status"] != "success":
            return JSONResponse(result, status_code=500)

        return JSONResponse({
            "status": "success",
            "message": "Cloning completed successfully",
            "details": result,
            "domain": domain,
            "logo": logo
        })

    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
