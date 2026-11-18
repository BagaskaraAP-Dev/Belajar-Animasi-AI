#!/usr/bin/env bash
# Pasang font Bangers (judul) dari npm, konversi WOFF -> TTF. Poppins & DejaVu Sans Mono dipasang lewat paket OS / Google Fonts.
set -euo pipefail
tmp=$(mktemp -d); cd "$tmp"
npm pack @fontsource/bangers -q >/dev/null && tar xzf fontsource-bangers-*.tgz
mkdir -p ~/.fonts
python3 -c "from fontTools.ttLib import TTFont; f=TTFont('package/files/bangers-latin-400-normal.woff'); f.flavor=None; f.save('$HOME/.fonts/Bangers-Regular.ttf')"
fc-cache -f >/dev/null && fc-list | grep -i bangers
