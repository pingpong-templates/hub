import typer
from typing import Annotated
from pathlib import Path

from tomllib import load as load_toml
from tomllib import loads as loads_toml
from tomli_w import dump as dump_toml

import shutil

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def new(name: Annotated[str, typer.Argument(help="The name of the folder to create")]):
    # copy over template from ./project-template
    project_template_dir = Path(__file__).parent.parent / "project_template"
    destination_dir = Path.cwd() / name
    shutil.copytree(project_template_dir, destination_dir)


if __name__ == "__main__":
    app()
