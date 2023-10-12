import typer
from typing import Annotated
from pathlib import Path

from tomllib import load as load_toml
from tomli_w import dump as dump_toml

import subprocess

HUB_BASE_PATH = "/Users/erickfriis/langchain/langserve-hub/"

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _load_pyproject():
    curr_proj_pyproject = Path("pyproject.toml")
    with open(curr_proj_pyproject, "rb") as f:
        curr_data = load_toml(f)
        return curr_data


def _dump_pyproject(curr_data):
    curr_proj_pyproject = Path("pyproject.toml")
    with open(curr_proj_pyproject, "wb") as f:
        dump_toml(curr_data, f)


@app.command()
def add(
    location: Annotated[
        str, typer.Argument(help="The slug in LangServe Hub like `simple/pirate`")
    ]
):
    # poetry install it from git
    path = f"{HUB_BASE_PATH}{location}"
    # poetry add it
    print(f"Adding {location}")
    subprocess.run(f"poetry add {path}", shell=True)
    print(f"Successfully added {location}")

    pyproject = f"{path}/pyproject.toml"
    with open(pyproject, "rb") as f:
        data = load_toml(f)

    name = data["tool"]["poetry"]["name"]

    module_name = name.replace("-", "_")

    # load current pyproject.toml
    curr_data = _load_pyproject()

    langserve = curr_data["tool"].get("langserve", {})
    langserve[f"/{name}"] = module_name
    curr_data["tool"]["langserve"] = langserve

    _dump_pyproject(curr_data)


@app.command()
def serve():
    print("Validating dependencies and installing missing ones")
    subprocess.run("poetry install", shell=True)
    print("Successfully installed missing dependencies")

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
