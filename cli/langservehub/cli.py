import os
import typer
import asyncio
from typing import Annotated, Optional, List
from pathlib import Path

from tomllib import load as load_toml
from tomllib import loads as loads_toml
from tomli_w import dump as dump_toml
from urllib import request

import subprocess

import base64
import asyncio

BASE_URL = "https://api.github.com/repos/langchain-ai/langserve-hub/contents/"

from github import Github, Auth

g = Github(auth=Auth.Token(token=os.environ["GITHUB_PAT"]))


async def download_github_path(path: str, local_dest: str):
    repo = g.get_repo("langchain-ai/langserve-hub")
    # recursively download all files in path

    base_path = Path(path)
    local_base_path = Path(local_dest)
    try:
        local_base_path.mkdir(exist_ok=False)
    except FileExistsError:
        print(FileExistsError(f"Error: Directory {local_base_path} already exists"))
        return

    # todo: split into collecting directories
    # and then tqdm downloading files
    async def _download_github_path(subdir: Path = Path("")):
        github_path = base_path / subdir
        local_path = local_base_path / subdir
        contents = repo.get_contents(str(github_path))

        if isinstance(contents, List):
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

    print(f"Successfully downloaded {path} to {local_dest}")


app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def new(
    name: Annotated[
        Optional[str], typer.Argument(help="The name of the folder to create")
    ] = None
):
    # copy over template from ./project-template
    download("cli/project-template", name)


def download(
    package: Annotated[
        str, typer.Argument(help="The package in LangServe Hub like `simple/pirate`")
    ],
    localpath: Annotated[
        Optional[str], typer.Argument(help="The local path to download to")
    ] = None,
):
    if localpath is None:
        localpath = package.split("/")[-1]
    asyncio.run(download_github_path(package, localpath))


if __name__ == "__main__":
    app()
