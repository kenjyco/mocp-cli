#!/usr/bin/env bash

# Get the directory where this script lives
DIR="$(cd "$(dirname "$0")" && pwd)"

[[ ! -d "venv" ]] && python3 -m venv venv && venv/bin/pip3 install --upgrade pip wheel
venv/bin/pip3 install -r requirements.txt --upgrade
