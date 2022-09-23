import logging
import subprocess

logger = logging.getLogger(__name__)

UPSTREAM_URL = "https://github.com/kForth/OctoPluginStats.git"
GIT_DESC_FILE = ".git/description"

# Init git repository
if "{{ cookiecutter.initialize_git_repo | lower }}".strip().startswith("y"):
    logger.debug("Initializing Git Repo")

    # Init repo
    subprocess.call(["git", "init"])
    subprocess.call(["git", "remote", "add", "upstream", UPSTREAM_URL])
    subprocess.call(["git", "fetch", "upstream"])

    # Initial commit
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "Initial commit"])

    # Name Repo
    with open(GIT_DESC_FILE, "w+") as file:
        file.write("{{cookiecutter.repo_name}}")
