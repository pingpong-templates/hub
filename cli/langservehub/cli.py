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
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")


package_app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(package_app, name="package")


@package_app.command("new")
def package_new(
    name: Annotated[str, typer.Argument(help="The name of the folder to create")]
):
    computed_name = name if name != "." else Path.cwd().name
    destination_dir = Path.cwd() / name if name != "." else Path.cwd()

    # copy over template from ../package_template
    project_template_dir = Path(__file__).parent.parent / "package_template"
    shutil.copytree(project_template_dir, destination_dir, dirs_exist_ok=name == ".")

    package_name_split = computed_name.split("/")
    package_name_last = (
        package_name_split[-2]
        if len(package_name_split) > 1 and package_name_split[-1] == ""
        else package_name_split[-1]
    )
    default_package_name = re.sub(
        r"[^a-zA-Z0-9_]",
        "_",
        package_name_last,
    )

    # replace template strings
    pyproject = destination_dir / "pyproject.toml"
    pyproject_contents = pyproject.read_text()
    pyproject.write_text(
        pyproject_contents.replace("__package_name__", default_package_name)
    )

    # move module folder
    package_dir = destination_dir / default_package_name
    shutil.move(destination_dir / "package_template", package_dir)

    # replace readme
    readme = destination_dir / "README.md"
    readme_contents = readme.read_text()
    readme.write_text(
        readme_contents.replace("__package_name_last__", package_name_last)
    )


if __name__ == "__main__":
    app()
