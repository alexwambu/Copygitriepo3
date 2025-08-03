import os
import subprocess

def clone_private_repo(repo_path: str, dest_dir: str = "repo") -> dict:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"status": "error", "message": "GITHUB_TOKEN is not set in environment"}

    repo_url = f"https://{token}:x-oauth-basic@github.com/{repo_path}"

    if os.path.exists(dest_dir):
        subprocess.run(["rm", "-rf", dest_dir])

    try:
        result = subprocess.run(["git", "clone", repo_url, dest_dir], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"status": "success", "message": f"Repo cloned to ./{dest_dir}"}
        else:
            return {
                "status": "error",
                "message": f"Failed to clone repo. Git says: {result.stderr}"
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}
