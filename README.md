# LangServe Hub

Packages that can be easily hosted by LangServe using the `langserve` cli.

## Hacky How-To

Still working through some global virtual environment bugs for the cli. For now, the following works for me:
```bash
# this assumes you have github ssh set up
pip install --upgrade langservehub
# alternative: pip install --upgrade git+https://github.com:langchain-ai/langserve-hub.git#subdirectory=cli

# this is only required because this repo is currently private
export GITHUB_PAT="<github-personal-access-token>"

langservehub new my-app
cd my-app/packages

# download a package for editing
langservehub download simple/pirate

# install it in the app
cd ../app
poetry install
langservehub add ../packages/pirate

# also add a url package
langservehub add rag/chroma-rag

# start the server
langservehub serve
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