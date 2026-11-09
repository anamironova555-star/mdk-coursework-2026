#!/usr/bin/env bash
set -eu
TARGET="${1:?Укажите каталог для архива}"
mkdir -p "$TARGET/source"
printf 'user1\n' > "$TARGET/source/users.txt"
printf 'order1\n' > "$TARGET/source/orders.txt"
printf 'product1\n' > "$TARGET/source/products.txt"
cd "$TARGET"
tar -czf backup.tar.gz source/
sha256sum backup.tar.gz > backup.sha256
