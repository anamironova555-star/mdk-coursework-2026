#!/usr/bin/env bash
set -eu
TARGET="${1:?Укажите каталог результатов STLC}"
for section in 01_planning 02_design 03_environment 04_execution 05_reporting 06_closure; do mkdir -p "$TARGET/$section"; done
echo "STLC-структура создана: $TARGET"
