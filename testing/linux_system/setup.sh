#!/usr/bin/env bash
set -eu
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "${QA_RUN:-$ROOT/.logs}"
echo "Среда подготовлена: ${QA_RUN:-$ROOT/.logs}"
