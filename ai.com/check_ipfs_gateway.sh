#!/bin/bash
check_ipfs_gateway(){
  local MAX_WAIT_TIME=10
  if [[ "$1" == read || -z "$1" ]]; then
    if [[ "$(curl -m $MAX_WAIT_TIME -s "$2/ipfs/bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqic223w5sk3m" | tail -n 1)" == "Hello from IPFS Gateway Checker" ]] ; then
      return 0
    fi
  elif [[ "$1" == write ]]; then
    # if [[ "$(curl -m $MAX_WAIT_TIME -X POST -s -o /dev/null -w '%{http_code}' "$2/api/v0/add" | tail -n 1)" == "400" ]] ; then
    #   return 0
    # elif [[ "$(curl -m $MAX_WAIT_TIME -X POST -s -o /dev/null -w '%{http_code}' "${2}:5001/api/v0/add" | tail -n 1)" == "400" ]] ; then
    #   return 0
    # fi
    #file argument 'path' is required
    if [[ "$(curl -m $MAX_WAIT_TIME -X POST -s "$2/api/v0/add")" == "file argument 'path' is required" ]] ; then
      return 0
    elif [[ "$(curl -m $MAX_WAIT_TIME -X POST -s "${2}:5001/api/v0/add")" == "file argument 'path' is required" ]] ; then
      return 0
    fi
  fi
  return 1
}
check_ipfs_gateway "$@"