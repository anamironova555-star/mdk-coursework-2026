#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
check "JSON no_extra_fields" python3 "$ROOT/validate.py" users "$DATA/users.json"
finish
