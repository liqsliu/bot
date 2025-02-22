#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
LP=${LP:-/var/www/dav/tmp}

if bash "$SH_PATH/check_ipfs_gateway.sh" "$1" "$2"; then
  echo "$2 GATEWAY_URL/ipfs/HASH_CID 1" >> "$LP/ipfs_gateways_$1.txt"
fi