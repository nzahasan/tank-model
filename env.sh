#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )"
export PYTHONPATH=$SCRIPT_DIR:$PYTHONPATH
echo "Added ${SCRIPT_DIR} in PYTHONPATH"
