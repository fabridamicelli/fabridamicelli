import pathlib
import requests
import base64

CURR_DIR = pathlib.Path(".").resolve()


owner = "fabridamicelli"
repo = "cronex.nvim"
file_path = "scripts/downloads/last_month.txt"


def get_n_downloads(owner, repo, file_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url)
    if response.status_code == 200:
        file_data = response.json()
        content = file_data["content"]
        decoded_content = base64.b64decode(content).decode("utf-8")
        return int(decoded_content)
    raise Exception(f"Failed to retrieve file content: {response.status_code}")


n_downloads = get_n_downloads(owner, repo, file_path)
start = """<img src="https://img.shields.io/badge/downloads/month-"""
new = f"""<img src="https://img.shields.io/badge/downloads/month-{n_downloads}-blue" height="16"><br>"""

readme = CURR_DIR / "README.md"
new_lines = []
for line in readme.read_text().splitlines():
    if line.startswith(start):
        new_lines.append(new)
    else:
        new_lines.append(line)
new_readme = "\n".join(new_lines)
readme.write_text(new_readme)
