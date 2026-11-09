#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
check "JSON schema" python3 "$ROOT/validate.py" config "$DATA/config.json"
finish
