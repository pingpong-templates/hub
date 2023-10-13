import os
import typer
from typing import Annotated, Optional
from pathlib import Path

from tomllib import load as load_toml
from tomli_w import dump as dump_toml
from urllib import request

import subprocess


app = typer.Typer(no_args_is_help=True, add_completion=False)


class PyProject:
    def __init__(self, data: dict, path: str | None):
        self.data = data
        self.path = path

    @classmethod
    def load(cls, path: str):
        with open(path, "rb") as f:
            data = load_toml(f)
        return cls(data, path)

    @classmethod
    def from_url(cls, url: str):
        try:
            with request.urlopen(url) as f:
                data = load_toml(f)
            return cls(data, None)
        except request.HTTPError as e:
            raise ValueError(f"Consider updating your GITHUB_TOKEN") from e

    def save(self):
        if self.path is None:
            raise ValueError("Cannot save a PyProject that was not loaded from a file")
        with open(self.path, "wb") as f:
            dump_toml(self.data, f)

    def _get_langserve_path_dict(self):
        return self.data["tool"].get("langserve", {}).get("paths", {})

    def _set_langserve_path_dict(self, path_dict):
        langserve = self.data["tool"].get("langserve", {})
        langserve["paths"] = path_dict
        self.data["tool"]["langserve"] = langserve

    def is_langserve(self):
        return "langserve" in self.data["tool"]

    def add_langserve_path(self, path: str, module_name: str):
        paths = self._get_langserve_path_dict()
        paths[path] = module_name
        self._set_langserve_path_dict(paths)

    def remove_langserve_path(self, path: str):
        paths = self._get_langserve_path_dict()
        paths.pop(path)
        self._set_langserve_path_dict(paths)

    def get_langserve_paths(self):
        return self._get_langserve_path_dict()

    def get_langserve_export(self):
        chain = self.data["tool"].get("langserve", {}).get("export")
        if chain is None:
            raise ValueError("No chain was exported at `tool.langserve.export`")
        return chain


def _load_pyproject():
    curr_proj_pyproject = Path("pyproject.toml")
    return PyProject.load(curr_proj_pyproject)


@app.command()
def list():
    curr_data = _load_pyproject()
    langserve = curr_data["tool"].get("langserve", {})
    for k, v in langserve.items():
        typer.echo(f"{k} -> {v}")


@app.command()
def remove(path: str):
    curr_data = _load_pyproject()
    curr_data.remove_langserve_path(path)
    curr_data.save()


def _package_to_poetry(package: str):
    package_type = "hub"
    if package.startswith(".") or package.startswith("/"):
        # package_type = "path"
        return package

    # if it's hub, have to add base path
    return f"https://github.com/langchain-ai/langserve-hub.git#subdirectory={package}"


def _package_to_pyproject(package: str):
    if package.startswith(".") or package.startswith("/"):
        # package_type = "path"
        return f"{package}/pyproject.toml"
    tokenparam = (
        ""
        if not os.environ.get("GITHUB_TOKEN")
        else f"?token={os.environ['GITHUB_TOKEN']}"
    )
    return f"https://raw.githubusercontent.com/langchain-ai/langserve-hub/main/{package}/pyproject.toml{tokenparam}"


@app.command()
def add(
    package: Annotated[
        str, typer.Argument(help="The package in LangServe Hub like `simple/pirate`")
    ],
    path: Annotated[
        Optional[str],
        typer.Argument(help="The api path to mount the chain at like `/pirate`"),
    ] = None,
):
    # get pyproject
    package_pyproject_url = _package_to_pyproject(package)
    package_pyproject = PyProject.from_url(package_pyproject_url)

    # validate it's langserve-compatible
    if not package_pyproject.is_langserve():
        raise ValueError(
            f"Package {package} does not have a `tool.langserve` section in its pyproject.toml"
        )

    package_path = _package_to_poetry(package)
    # poetry add it
    typer.echo(f"Adding {package}")
    subprocess.run(f"poetry add {package_path}", shell=True)

    # validate it's a langserve package

    typer.echo(f"Successfully added {package}")

    # poetry install it from git
    api_path = path or "/{package}"

    pyproject = _load_pyproject()
    pyproject.add_langserve_path(api_path, package_pyproject.get_langserve_export())

    pyproject.save()


@app.command()
def serve():
    typer.echo("Validating dependencies and installing missing ones")
    subprocess.run("poetry install", shell=True)
    typer.echo("Successfully installed missing dependencies")

    curr_data = _load_pyproject()
    langserve = curr_data["tool"].get("langserve", {})

    from fastapi import FastAPI
    import uvicorn
    from langserve import add_routes

    fastapp = FastAPI()

    for k, v in langserve.items():
        mod = __import__(v)
        chain = mod.chain
        add_routes(fastapp, chain, path=k)

    uvicorn.run(fastapp, host="localhost", port=8000)


if __name__ == "__main__":
    app()
