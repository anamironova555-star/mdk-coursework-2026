#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
reject_broken() {
    test -s "$DATA/broken.json" && ! python3 "$ROOT/validate.py" syntax "$DATA/broken.json"
}
check "users.json синтаксически корректен" python3 "$ROOT/validate.py" syntax "$DATA/users.json"
check "broken.json отклонён" reject_broken
finish
