# LangServe Hub

Packages that can be easily hosted by LangServe using the `langserve` cli.

## Hacky How-To

Still working through some global virtual environment bugs for the cli. For now, the following works for me:
```bash
# from langserve-hub dir
alias langserve="python $(pwd)/cli/langservehub/cli.py"
cd cli
poetry install
source .venv/bin/activate

# go to "fake" new project
cd ../newproject

# get your github token by clicking "raw" on this file
# and copying the token queryparam
# https://github.com/langchain-ai/langserve-hub/blob/main/simple/pirate/pyproject.toml

# this is only because it's a private repo
# pretty sure a PAT also works

export GITHUB_TOKEN="<token>"

# add pirate endpoint
langserve add simple/pirate

# serve
langserve serve
```

## Data Format

What makes these packages work?

- Poetry
- pyproject.toml files

### Installable Packages

Everything is a Poetry package currently. This allows poetry to manage our dependencies for us :).

In addition to normal keys in the `pyproject.toml` file, you'll notice an additional `tool.langserve` key ([link](https://github.com/langchain-ai/langserve-hub/blob/main/simple/pirate/pyproject.toml#L13-L15)).

This allows us to identify which module and attribute to import as the chain/runnable for the langserve `add_routes` call.

### Apps (with installed langserve packages)

Let's say you add the pirate package with `langserve add simple/pirate`.

This adds a `poetry` dependency like:
```
[tool.poetry.dependencies.pirate]
git = "https://github.com/langchain-ai/langserve-hub.git"
subdirectory = "simple/pirate"
```

And also mounts the path like
```
[tool.langserve.paths]
"/simple/pirate" = [
    "pirate",
    "chain",
]
```
Where `pirate` is the module, and `chain` is the attr (i.e. `from pirate import chain`)