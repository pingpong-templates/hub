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

# add pirate endpoint
langserve add simple/pirate

# serve
langserve serve
```