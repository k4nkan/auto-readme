"""test script for ats and github api"""

import os
import sys
import requests

GITHUB_API_TOKEN = os.environ["GITHUB_API_TOKEN"]
HEADERS = {"Authorization": f"Bearer {GITHUB_API_TOKEN}"}


def get_repo_tree(user: str, repo: str) -> dict:
    """func for get repo data and tree data"""
    url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"

    try:
        res = requests.get(url, headers=HEADERS, timeout=10).json()

    except Exception as e:
        print(e)
        sys.exit(1)

    tree = res.get("tree", [])

    root = {}
    for item in tree:
        path_parts = item["path"].split("/")
        current = root
        for part in path_parts[:-1]:
            current = current.setdefault(part, {})
        if item["type"] == "tree":
            current[path_parts[-1]] = {}
        else:
            current[path_parts[-1]] = None

    return root


def main() -> None:
    """main func"""
    args = sys.argv
    user_name = args[1]
    repo_name = args[2]

    structure = get_repo_tree(user_name, repo_name)

    print(structure)


if __name__ == "__main__":
    main()
