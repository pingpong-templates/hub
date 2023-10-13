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