#!/bin/bash

# Exit script on first error
set -e

# Check if pylint is installed
if ! pip list | grep ruff; then
    # Upgrade pip and install pylint if not installed
    python -m pip install --upgrade pip
    pip install ruff
fi

# Run pylint on all Python files in the repository
#find . -name "*.py" -print0 | xargs -0 pylint
ruff check .