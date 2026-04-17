import os
import subprocess
from pathlib import Path

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
SHARDS_DIR = Path("shards")

# Embed token in remote so push works without interactive auth
subprocess.run(["git", "remote", "set-url", "origin",
                f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPOSITORY}.git"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
subprocess.run(["git", "config", "user.name", "github-actions"], check=True)

base = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                      capture_output=True, text=True, check=True).stdout.strip()

for tf_file in sorted(SHARDS_DIR.glob("*.tf")):
    branch = f"shard/{tf_file.stem}"
    subprocess.run(["git", "checkout", "-b", branch], check=True)
    subprocess.run(["git", "add", str(tf_file)], check=True)
    subprocess.run(["git", "commit", "-m", f"add {tf_file.stem}"], check=True)
    subprocess.run(["git", "push", "origin", branch], check=True)
    subprocess.run(["git", "checkout", base], check=True)
    print(f"pushed {branch}")
