#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/check.sh"
check "users.json существует" test -s "$DATA/users.json"
check "config.json существует" test -s "$DATA/config.json"
finish
