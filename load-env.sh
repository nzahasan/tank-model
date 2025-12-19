#!/usr/bin/env bash

# load model environment for testing purposes only

BASE_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )"

SCRIPTS_DIR=$BASE_DIR/scripts

export PYTHONPATH=$BASE_DIR:$PYTHONPATH

export PATH=$SCRIPTS_DIR:$PATH

echo "Added ${BASE_DIR} in PYTHONPATH"
echo "Added ${SCRIPTS_DIR} in PATH"

