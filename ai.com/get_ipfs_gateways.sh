#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
LP=${LP:-/var/www/dav/tmp}
DOMAIN=${DOMAIN:-liuu.tk}





  # https://ipfs.github.io/public-gateway-checker/
  # https://ipfs.github.io/public-gateway-checker/gateways.json

  # bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqic223w5sk3m
  # https://ipfs.io/ipfs/bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqic223w5sk3m?now=1628057241949
  # Hello from IPFS Gateway Checker

# get_gateways_from_github(){
# local ALL_GATEWAYS=$(curl -m 15 -s https://ipfs.github.io/public-gateway-checker/gateways.json)
# [[ -z "$ALL_GATEWAYS"]] && return 1
# local GATEWAY_URL=
# local i=0
# for (( ; ; i++ ))
# do
#   local GATEWAY_URL=$(echo "$ALL_GATEWAYS" | jq -r ".[$i]")
#   [[ "$GATEWAY_URL" == "null" ]] && break
#   GATEWAY_URL=${GATEWAY_URL%/ipfs/:hash}
#   if bash "$SH_PATH/check_ipfs_gateway.sh" $1 "$GATEWAY_URL"; then
#     echo "$GATEWAY_URL GATEWAY_URL/ipfs/HASH_CID 1"
#   fi
# done
# }

get_ipfs_gateways(){
local ALL_GATEWAYS=$(curl -m 15 -s https://ipfs.github.io/public-gateway-checker/gateways.json)
[[ -z "$ALL_GATEWAYS" ]] && return 1
local GATEWAY_URL=
echo > "$LP/ipfs_gateways_$1.txt"
local i=0
for (( ; ; i++ ))
do
  local GATEWAY_URL=$(echo "$ALL_GATEWAYS" | jq -r ".[$i]")
  [[ "$GATEWAY_URL" == "null" ]] && break
  GATEWAY_URL=${GATEWAY_URL%/ipfs/:hash}
  nohup bash "$SH_PATH/get_ipfs_gateways_b.sh" $1 "$GATEWAY_URL" &>/dev/null &
done
GATEWAY_URL="https://snap1.d.tube"
nohup bash "$SH_PATH/get_ipfs_gateways_b.sh" $1 "$GATEWAY_URL" &>/dev/null &
GATEWAY_URL="http://127.0.0.1"
nohup bash "$SH_PATH/get_ipfs_gateways_b.sh" $1 "$GATEWAY_URL" &>/dev/null &
GATEWAY_URL="https://$DOMAIN"
nohup bash "$SH_PATH/get_ipfs_gateways_b.sh" $1 "$GATEWAY_URL" &>/dev/null &
}

#get_gateways_from_github read/write
get_ipfs_gateways "$@"
