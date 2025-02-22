#!/bin/bash
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
if [[ -z "$1" ]]; then
  echo ".qw text"
  exit
fi

python3 "$SH_PATH/"qw.py "$*" | sed 1d
