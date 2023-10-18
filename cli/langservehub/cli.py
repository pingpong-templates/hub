import typer
from typing import Annotated, Optional
from pathlib import Path

import shutil
import re
import subprocess

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _git_get_root(destination_dir: Optional[Path]) -> Optional[Path]:
    """Get the root of the git repository."""
    try:
        path_out = (
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                cwd=None
                if destination_dir is None
                else str(destination_dir.absolute()),
            )
            .stdout.decode()
            .strip()
        )
        if path_out:
            return Path(path_out)

    except Exception:
        pass

    return None


@app.command()
def new(name: Annotated[str, typer.Argument(help="The name of the folder to create")]):
    # copy over template from ../project_template
    project_template_dir = Path(__file__).parent.parent / "project_template"
    destination_dir = Path.cwd() / name
    shutil.copytree(project_template_dir, destination_dir)


package_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(package_app, name="package")


@package_app.command("new")
def package_new(
    name: Annotated[str, typer.Argument(help="The name of the folder to create")]
):
    # copy over template from ../package_template
    project_template_dir = Path(__file__).parent.parent / "package_template"
    destination_dir = Path.cwd() / name
    shutil.copytree(project_template_dir, destination_dir)

    git_root = _git_get_root(destination_dir)
    relative_path = None if git_root is None else destination_dir.relative_to(git_root)

    package_description: str = typer.prompt("Package Description", default="")
    github_repo: str = typer.prompt("Github Repo", default="langchain-ai/langserve-hub")

    if relative_path is None:
        installation_command = f"# <Fill this out before publishing>\n# poe add ..."
    elif github_repo == "langchain-ai/langserve-hub":
        installation_command = f"poe add {relative_path}"
    else:
        installation_command = f"poe add --repo={github_repo} {relative_path}"

    package_name_split = name.split("/")
    default_package_name = re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        (
            package_name_split[-2]
            if len(package_name_split) > 1 and package_name_split[-1] == ""
            else package_name_split[-1]
        ),
    )

    package_name = name
    export_module = typer.prompt("Module Name", default=default_package_name)

    # replace template strings
    pyproject = destination_dir / "pyproject.toml"
    pyproject_contents = pyproject.read_text()
    pyproject.write_text(
        pyproject_contents.replace("__package_name__", package_name)
        .replace("__export_module__", export_module)
        .replace("__package_description__", package_description)
    )

    # move module folder
    package_dir = destination_dir / export_module
    shutil.move(destination_dir / "package_template", package_dir)

    # replace readme
    readme = destination_dir / "README.md"
    readme_contents = readme.read_text()
    readme.write_text(
        readme_contents.replace("__package_name__", package_name)
        .replace("__installation_command__", installation_command)
        .replace("__package_description__", package_description)
    )


if __name__ == "__main__":
    app()
