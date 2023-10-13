from urllib import request
import base64
import asyncio

BASE_URL = "https://api.github.com/repos/langchain-ai/langserve-hub/contents/"

from github import Github
from pathlib import Path

g = Github()


async def download_github_path(path: str, local_dest: str):
    repo = g.get_repo("langchain-ai/langserve-hub")
    # recursively download all files in path

    base_path = Path(path)
    local_base_path = Path(local_dest)

    local_base_path.mkdir(exist_ok=True)

    # todo: split into collecting directories
    # and then tqdm downloading files
    async def _download_github_path(subdir: Path = Path("")):
        github_path = base_path / subdir
        local_path = local_base_path / subdir
        contents = repo.get_contents(str(github_path))

        if isinstance(contents, list):
            # is a folder, mkdir and iterate
            local_path.mkdir(exist_ok=True)
            # todo: parallelize
            await asyncio.gather(
                *[_download_github_path(subdir / content.name) for content in contents]
            )
        else:
            # is a file, save
            print(f"Downloading {github_path} to {local_path}")
            with open(local_path, "wb") as f:
                content = contents.content
                f.write(base64.b64decode(content))

    await _download_github_path()
