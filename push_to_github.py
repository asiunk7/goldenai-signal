import requests
import os
import base64

def push_signal_to_github(filename):
    with open(filename, "r") as file:
        content = file.read()

    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")  # format: username/repo
    path = "signal.json"

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get SHA of existing file if any
    sha = None
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json().get("sha")

    data = {
        "message": "update signal",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    if sha:
        data["sha"] = sha

    put_response = requests.put(url, headers=headers, json=data)
    if put_response.status_code in [200, 201]:
        print("✅ signal.json pushed to GitHub.")
    else:
        print("❌ Failed to push:", put_response.text)
