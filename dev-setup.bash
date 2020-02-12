#!/usr/bin/env bash

# Get the directory where this script lives
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"
pip_args=(--no-warn-script-location --upgrade --upgrade-strategy eager)
PYTHON="python3"
PIP="venv/bin/pip3"
if [[ $(uname) =~ "MINGW" ]]; then
    PYTHON="python"
    PIP="venv/Scripts/pip"
fi
[[ ! -d venv ]] && $PYTHON -m venv venv
PYTHON=$(dirname $PIP)/python
$PYTHON -m pip install --upgrade pip wheel
$PIP install -r requirements.txt ${pip_args[@]}
if [[ ! $(uname) =~ "MINGW" ]]; then
    $PIP install ipython pdbpp ${pip_args[@]}
else
    $PIP install ipython ${pip_args[@]}
fi
$PYTHON setup.py develop
