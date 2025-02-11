#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}


FILE_PATH=$2

upload_to_ipfs(){
  local GATEWAY_URL=$1
  local MAX_UPLOAD_TIME=60
  # local FILE_PATH=$2

  local HASH_CID=$(ipfs add --cid-version 1 -n -Q "$FILE_PATH")

  try_time=0
  delay_time=0
  while true
  do
#        [[ -z "$hash" ]] && res=$(curl -m $MAX_UPLOAD_TIME -s -X POST --compressed -F file=@"$FILE_PATH" https://snap1.d.tube/api/v0/add) && hash=$(echo "$res" | jq -r '.Hash' ) || nohup curl -m $(( 2 * MAX_UPLOAD_TIME )) -s -X POST --compressed -F file=@"$FILE_PATH" https://snap1.d.tube/api/v0/add &>/dev/null &
    if ps -ax|grep -v grep | grep curl | grep /api/v0/add  &>/dev/null ; then
      delay_time=$(( $delay_time + 1 ))
      if [[ $delay_time -ge 60 ]]; then
        return 1
        break
      fi
      sleep 1
      continue
    fi
    delay_time=0
#    if [[ "$(curl -m 3 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/version | tail -n 1)" == "200" ]] ; then
#echo  "check:  $GATEWAY_URL/api/v0/add " 
#echo  "check: $(curl -m 3 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/add)" 
    if [[ "$(curl -m 3 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/add | tail -n 1)" == "400" ]] ; then
      local existed=0
      # if [[ "$GATEWAY_URL" == "https://ipfs.infura.io:5001" ]] ; then
      #   if [[ "$(curl -m 2 --max-filesize 1 -s -o /dev/null -w '%{http_code}' https://${HASH_CID}.ipfs.infura-ipfs.io | tail -n 1)" == "200" ]] ; then
      #     existed=1
      #     hash=$HASH_CID
      #   fi
      # elif [[ "$GATEWAY_URL" == "http://127.0.0.1:5001" ]] ; then
      #   if [[ "$(curl -m 2 --max-filesize 1 -s -o /dev/null -w '%{http_code}' https://127.0.0.1/ipfs/${HASH_CID} | tail -n 1)" == "200" ]] ; then
      #     existed=1
      #     hash=$HASH_CID
      #   fi
      # else
      #   if [[ "$(curl -m 2 --max-filesize 1 -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/ipfs/$HASH_CID | tail -n 1)" == "200" ]] ; then
      #     existed=1
      #     hash=$HASH_CID
      #   fi
      # fi
      

      if [[ "$(curl -m 2 --max-filesize 1 -s -o /dev/null -w '%{http_code}' $(get_gateways $GATEWAY_URL | sed "s/GATEWAY_URL/$GATEWAY_URL/1" | sed "s/HASH_CID/$HASH_CID/1") | tail -n 1)" == "200" ]] ; then
        existed=1
        hash=$HASH_CID
      fi


      if [[ $existed -eq 0 ]]; then
        hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add?cid-version=1" | jq -r '.Hash' )
      fi







#      hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" $GATEWAY_URL/api/v0/add | jq -r '.Hash' )
#      hash=$(curl -m $MAX_UPLOAD_TIME -s -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add?cid-version=1" | jq -r '.Hash' )
      if [[ -n "$hash" ]]; then
        echo "$hash"
        break
      fi
#      nohup curl -m $(( 2 * MAX_UPLOAD_TIME )) -s -X POST --compressed -F file=@"$FILE_PATH" https://snap1.d.tube/api/v0/add &>/dev/null &
    fi
    try_time=$(( $try_time + 1 ))
    if [[ $try_time -ge 2 ]]; then
      break
    fi
    sleep 5

  done
  [[ -n "$hash" ]] && return 0 || return 1
}







get_gateways(){
#check 400
#   GATEWAY_URL=https://gateway.originprotocol.com; curl -m 5 -X POST -w '%{http_code}' $GATEWAY_URL/api/v0/add -v



local IPFS_GATEWAYS="
https://ipfs.infura.io:5001 https://HASH_CID.ipfs.infura-ipfs.io/ 2

https://snap1.d.tube GATEWAY_URL/ipfs/HASH_CID 1

https://gateway.originprotocol.com GATEWAY_URL/ipfs/HASH_CID 1





http://127.0.0.1:5001 http://127.0.0.1:8080/ipfs/HASH_CID 1
https://liuu.tk GATEWAY_URL/ipfs/HASH_CID 1


"

if [[ "$1" == "" ]]; then
  echo "$IPFS_GATEWAYS" | sed '/^ *$/d' | cut -d" " -f1
elif [[ $(echo "$IPFS_GATEWAYS" | grep -c -G "^$1 ") -eq 1 ]]; then
  local gateway=$(echo "$IPFS_GATEWAYS" | grep -G "^$1 ")
  if [[ -z "$2" ]]; then
    echo "$gateway" | cut -d" " -f2
  else
    :
  fi


fi








}

auto_to_all(){


  for i in $(get_gateways)
  do
    # upload_to_ipfs $i "$FILE_PATH" "$(get_gateways $i)" && return 0
    upload_to_ipfs $i "$FILE_PATH" && return 0
  done

  return 1
  upload_to_ipfs https://snap1.d.tube || upload_to_ipfs https://ipfs.infura.io:5001 || upload_to_ipfs http://127.0.0.1:5001 || upload_to_ipfs https://liuu.tk
            
  hash=$( bash "$SH_PATH/upload_to_ipfs.sh" https://snap1.d.tube "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://ipfs.infura.io:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" http://127.0.0.1:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://liuu.tk "$FILE_PATH" )
}



upload_to_ipfs "$@"

# auto_to_all

