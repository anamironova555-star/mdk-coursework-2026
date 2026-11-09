#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
for file in "$DATA"/*.json; do
    check "UTF-8 $(basename "$file")" python3 -c 'import pathlib,sys; pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")' "$file"
done
finish
