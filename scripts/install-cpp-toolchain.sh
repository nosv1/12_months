#!/usr/bin/env bash
# Install and verify the C++ toolchain on Ubuntu 24.04 (WSL2).
# Usage: ./scripts/install-cpp-toolchain.sh   (prompts for sudo password)
set -euo pipefail

sudo apt-get update
sudo apt-get install -y build-essential cmake gdb valgrind

echo
echo "== verify =="
for tool in gcc g++ make cmake gdb valgrind; do
    if command -v "$tool" >/dev/null; then
        printf '%-9s %s\n' "$tool" "$("$tool" --version | head -1)"
    else
        printf '%-9s MISSING\n' "$tool"
        exit 1
    fi
done
