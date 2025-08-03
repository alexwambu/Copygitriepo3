from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from clone_repo import clone_private_repo

app = FastAPI()

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
