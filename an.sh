#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}


if [[ -z "$1" ]]; then
  echo ".an \$url"
  echo ".an --all \$url"
  echo
  echo "https://github.com/oduwsdl/archivenow"
else
  archivenow "$@"
fi
