# LangServe Hub

Packages that can be easily hosted by LangServe using the `langserve` cli.

## Hacky How-To

Still working through some global virtual environment bugs for the cli. For now, the following works for me:
```bash
# install custom versions of langserve and langchain
pip install --upgrade langservehub

# this is only required because this repo is currently private
export GITHUB_PAT="<github-personal-access-token>"

langservehub new my-app
cd my-app

poetry install

# if you have problems with poe, use `poetry run poe ...` instead
poe add simple/pirate

poe list

poe start
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

Let's say you add the pirate package with `poe add simple/pirate`.

First this downloads the simple/pirate package to simple/pirate

Then this adds a `poetry` path dependency, which gets picked up from `add_package_routes`.