#!/bin/bash

export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
#DOMAIN=${DOMAIN:-liuu.tk}
export DOMAIN=${DOMAIN:-$(cat "$SH_PATH/DOMAIN")}
# LP=${LP:-/var/www/dav/tmp}
LP=${LP:-$HOME/tera/tmp}
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-64000000}


export IPFS_PATH="/home/liqsliu/tera/var/ipfs"

PRIVATE_KEYS_PATH="${HOME}/vps/private_keys.txt"
IPFS_API_KEY=$(grep IPFS_API_KEY "$PRIVATE_KEYS_PATH")
IPFS_API_KEY=${IPFS_API_KEY#* }


#ipfs
get_gateways(){

#check 400
#   GATEWAY_URL=https://ipfs.stibarc.com; curl -m 5 -X POST -w '%{http_code}' $GATEWAY_URL/api/v0/add -v
# https://infura-ipfs.io GATEWAY_URL/ipfs/HASH_CID 0 1
# https://ipfs.smartholdem.io GATEWAY_URL/ipfs/HASH_CID 0 0
# https://snap1.d.tube GATEWAY_URL/ipfs/HASH_CID 0 0
# https://ipfs.infura.io:5001 https://HASH_CID.ipfs.infura-ipfs.io/ 1 1
# http://127.0.0.1:5001 http://127.0.0.1:8080/ipfs/HASH_CID 0 0
# https://$DOMAIN GATEWAY_URL/ipfs/HASH_CID 0 0

# https://api.nft.storage/upload https://HASH_CID.ipfs.nftstorage.link/ 1 0 ${IPFS_API_KEY}
# upload_URL(need /api/v0/add) IPFS_URL cid_version gfwed [token]
#
# https://ipfs.pixura.io/api/v0/add https://ipfs.pixura.io/ipfs/HASH_CID 0 0
# https://cdn.ipfsscan.io/api/v0/add https://ipfs.crossbell.io/ipfs/HASH_CID 0 0
# https://cdn.ipfsscan.io/api/v0/add https://cdn.ipfsscan.io/ipfs/HASH_CID 0 0
# https://cdn.ipfsscan.io/api/v0/add https://gateway.ipfsscan.io/ipfs/HASH_CID 0 0
# https://cdn.ipfsscan.io/api/v0/add https://4everland.io/ipfs/HASH_CID 0 0
local IPFS_GATEWAYS="
https://ipfs.pixura.io/api/v0/add https://ipfs.pixura.io/ipfs/HASH_CID 0 0
"
# curl 'https://cdn.ipfsscan.io/api/v0/add' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Requested-With: XMLHttpRequest' -H 'Content-Type: multipart/form-data; boundary=---------------------------30114403322458380701248967467' -H 'Origin: https://cdn.ipfsscan.io' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'sec-ch-ua-platform: "Windows"' -H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not=A?Brand";v="24"' -H 'sec-ch-ua-mobile: ?0' -H 'Priority: u=0' --data-binary $'-----------------------------30114403322458380701248967467\r\nContent-Disposition: form-data; name="file"; filename="\xe5\x9b\xbe\xe7\x89\x87.png"\r\nContent-Type: image/png\r\n\r\n-----------------------------30114403322458380701248967467--\r\n'
# https://ipfs.crossbell.io/ipfs/QmRJpSm6cPHnqUqonBMSviJLSQ6Cnzx2AieadFnkxf5UXs?filename=图片.png
# curl 'https://cdn.ipfsscan.io/api/v0/add' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'X-Requested-With: XMLHttpRequest' -H 'Content-Type: multipart/form-data; boundary=---------------------------68793484727637958703343046544' -H 'Origin: https://cdn.ipfsscan.io' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'sec-ch-ua-platform: "Windows"' -H 'sec-ch-ua: "Google Chrome";v="125", "Chromium";v="125", "Not=A?Brand";v="24"' -H 'sec-ch-ua-mobile: ?0' -H 'Priority: u=0' -H 'TE: trailers' --data-binary $'-----------------------------68793484727637958703343046544\r\nContent-Disposition: form-data; name="file"; filename="\xe5\x9b\xbe\xe7\x89\x87.png"\r\nContent-Type: image/png\r\n\r\n-----------------------------68793484727637958703343046544--\r\n'

if [[ "$1" == "" ]]; then
  echo "$IPFS_GATEWAYS" | shuf | sed '/^ *$/d' | cut -d" " -f1
elif [[ $(echo "$IPFS_GATEWAYS" | grep -c -G "^$1 ") -eq 1 ]]; then
  local gateway=$(echo "$IPFS_GATEWAYS" | grep -G "^$1 ")
  if [[ -z "$2" ]]; then
    echo "$gateway" | cut -d" " -f2
  elif [[ "$2" == "cid_version" ]]; then
    echo "$gateway" | cut -d" " -f3
  elif [[ "$2" == "gfwed" ]]; then
    echo "$gateway" | cut -d" " -f4
  elif [[ "$2" == "token" ]]; then
    echo "$gateway" | cut -d" " -f5
  else
    :
  fi
fi

}

ipfs_hash_to_urls() {
  local path=$1
  local hash=${path%%\?*}
  hash=${hash%%/*}
  local cid=$hash
  local hash2=$(ipfs cid base32 $hash)
  local cid2=$hash2
#  local path_2=${path#*\?}
  local path2=${path#*$hash}
  path2=${path2#/}
  ipfs_urls="以下链接内容相同，如果第一个链接打不开请用第二个。另外，某些链接可能要过几分钟才能打开 
https://ipfs.crossbell.io/ipfs/$path
https://snap1.d.tube/ipfs/$path
https://cf-ipfs.com/ipfs/$path
https://dweb.link/ipfs/$path
https://ipfs.jbb.one//ipfs/$path
https://ipfs.smartsignature.io//ipfs/$path
https://10.via0.com/ipfs/$path
https://gateway.originprotocol.com/ipfs/$path
https://jorropo.net/ipfs/$path
https://ipfs.2read.net/ipfs/$path
https://$hash2.ipfs.cf-ipfs.com/$path2
https://$hash2.ipfs.dweb.link/$path2
https://$hash2.ipfs.ipfs.stibarc.com/$path2
https://ipfs.stibarc.com/ipfs/$path
https://hardbin.com/ipfs/$path
https://gateway.pinata.cloud/ipfs/$path
https://ipfs.jeroendeneef.com/ipfs/$path
https://ninetailed.ninja/ipfs/$path
https://ipfs.eternum.io/ipfs/$path
下面链接用浏览器可以打开，不要用微信 
https://ipfs.greyh.at/ipfs/$path
下面链接一般是打不开的 
https://cloudflare-ipfs.com/ipfs/$path
https://ipfs.privacytools.io/ipfs/$path
https://ipfs.infura.io/ipfs/$path
http://127.0.0.1/ipfs/$path
http://$cid2.ipfs.localhost/$path2
https://contributionls.github.io/public-gateway-checker/?cid=$cid
https://contributionls.github.io/public-gateway-checker/?cid=$cid2
https://gateway.ipfs.io/ipfs/$path
https://ipfs.io/ipfs/$path "
  echo "$ipfs_urls"

null="
https://ipfs.globalupload.io/$path
https://ipfs.dweb.tools/ipfs/$path 
"

}











upload_to_ipfs_gateway(){
  local GATEWAY_URL=$1
  local MAX_UPLOAD_TIME=60
  # local FILE_PATH=$2


  for ((i=0;i<9;i++)); do
    [[ -e $IPFS_PATH/repo.lock ]] || break
    echo "waiting for release..." 1>&2
    sleep 3
  done
  # not get cid for speed up vps
  if [[ "$(get_gateways $GATEWAY_URL cid_version)" == 1 ]]; then
    local cid_version="?cid-version=1"
    local HASH_CID=$(ipfs add --cid-version 1 -n -Q "$FILE_PATH")
  else
    local cid_version=
    local HASH_CID=$(ipfs add -n -Q "$FILE_PATH")
  fi

  local token=$(get_gateways $GATEWAY_URL token)

  local try_time=0
  local delay_time=0
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
    local host=${GATEWAY_URL#https://}
    local host=${host#http://}
    local host=${host%%/*}
    # opts="-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Origin: ${GATEWAY_URL%%/*}//$host'"
    opts=''
    if [[ -n "$debug" ]]; then
      echo "opts: $opts"
    fi
#    if [[ "$(curl -m 3 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/version | tail -n 1)" == "200" ]] ; then
#echo  "check:  $GATEWAY_URL/api/v0/add " 
#echo  "check: $(curl -m 3 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/add)" 
    # res_code=$(curl -m 5 -X POST -s -o /dev/null -w '%{http_code}' $GATEWAY_URL/api/v0/add | tail -n 1 2>/dev/null )
    res_code=$(curl -m 5 -X POST -s -o /dev/null -w '%{http_code}' $opts $GATEWAY_URL | tail -n 1 2>/dev/null )
    if [[ "$res_code" == "411" ]] || [[ "$res_code" == "401" ]] || [[ "$res_code" == "400" ]] || [[ "$res_code" == "403" ]]; then
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
      
      if [[ -n "$HASH_CID" && "$(curl -m 5 --max-filesize 1 -s -o /dev/null -w '%{http_code}' "$(get_gateways $GATEWAY_URL | sed "s|GATEWAY_URL|$GATEWAY_URL|1" | sed "s|HASH_CID|$HASH_CID|1")" | tail -n 1 2>/dev/null )" == "200" ]] ; then
        existed=1
        hash=$HASH_CID
        if [[ -n "$debug" ]]; then
          echo "existed: $hash"
        fi
      fi

      if [[ $existed -eq 0 ]]; then
        if [[ -n "$debug" ]]; then
          echo "not existed: $hash"
        fi
        # if [[ "$GATEWAY_URL" == 'https://api.nft.storage/upload' ]]; then
        # if [[ -n "$token" ]]; then
        if false; then
          if [[ -n "$debug" ]]; then
            echo "token: $token"
          fi
          if [[ "$GATEWAY_URL" == 'https://api.nft.storage/upload' ]]; then
            # local res=$(curl -m $MAX_UPLOAD_TIME -H "Authorization: Bearer ${token}" -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL" )
            # echo "res: $res" >&2
            # hash=$(echo "$res" | jq -r '.value.cid' )
            # echo "hash: $hash" >&2
            hash=$(curl -m $MAX_UPLOAD_TIME -H "Authorization: Bearer ${token}" -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL" | jq -r '.value.cid' )
          else
            hash=$(curl -m $MAX_UPLOAD_TIME -H "Authorization: Bearer ${token}" -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL${cid_version}" | jq -r '.Hash' )
          fi
        else
          # hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add${cid_version}" | jq -r '.Hash' 2>/dev/null )
          # hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add${cid_version}" | jq -r '.Hash')
          # hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" $opts "$GATEWAY_URL${cid_version}" | jq -r '.Hash')
          res=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" $opts "$GATEWAY_URL${cid_version}")
          if [[ -n "$debug" ]]; then
            cat <<EOF
curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" $opts "$GATEWAY_URL${cid_version}"
---
$res
EOF
          hash=$(echo "$res" | jq -r '.Hash')
          fi
        fi
      fi







#      hash=$(curl -m $MAX_UPLOAD_TIME -s --compressed -X POST -F file=@"$FILE_PATH" $GATEWAY_URL/api/v0/add | jq -r '.Hash' )
#      hash=$(curl -m $MAX_UPLOAD_TIME -s -X POST -F file=@"$FILE_PATH" "$GATEWAY_URL/api/v0/add?cid-version=1" | jq -r '.Hash' )
      if [[ -n "$hash" ]]; then
        # echo "$hash"
        real_ipfs_url=$(get_gateways $GATEWAY_URL | sed "s|GATEWAY_URL|$GATEWAY_URL|1" | sed "s|HASH_CID|$hash|1")
        break
      fi
#      nohup curl -m $(( 2 * MAX_UPLOAD_TIME )) -s -X POST --compressed -F file=@"$FILE_PATH" https://snap1.d.tube/api/v0/add &>/dev/null &
      try_time=$(( $try_time + 1 ))
      if [[ $try_time -ge 2 ]]; then
        break
      fi
      sleep 2
    else
      if [[ -n "$debug" ]]; then
        echo "res error: $res_code"
      fi
      break
    fi

  done
  [[ -n "$hash" ]] && return 0 || return 1
}












auto_to_all(){

  for i in $(get_gateways)
  do
    # upload_to_ipfs_gateway $i "$FILE_PATH" "$(get_gateways $i)" && return 0
    upload_to_ipfs_gateway "$i" "$FILE_PATH" && return 0
  done

  return 1
  upload_to_ipfs_gateway https://snap1.d.tube || upload_to_ipfs_gateway https://ipfs.infura.io:5001 || upload_to_ipfs_gateway http://127.0.0.1:5001 || upload_to_ipfs_gateway https://liuu.tk
            
  hash=$( bash "$SH_PATH/upload_to_ipfs.sh" https://snap1.d.tube "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://ipfs.infura.io:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" http://127.0.0.1:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://liuu.tk "$FILE_PATH" )
}















FILE_PATH="$1"
# debug="$2"
# if [[ -n "$debug" ]]; then
if [[ "$2" = debug ]]; then
  debug=1
  echo "debug: on"
fi

hash=""
real_ipfs_url=

file_to_ipfs() {
  local FILE_PATH="$1"
  local fn=${FILE_PATH##*/}

  flag=0
  if [[ -e "$FILE_PATH" ]]; then
    if [[ "$(du -b -- "$FILE_PATH" | cut -f1)" -gt 0 ]]; then
      if [[ "$(du -b -- "$FILE_PATH" | cut -f1)" -lt $MAX_SHARE_FILE_SIZE ]]; then
        local hash=""
        local MAX_UPLOAD_TIME=30
#          hash=$( bash "$SH_PATH/upload_to_ipfs.sh" https://snap1.d.tube "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://ipfs.infura.io:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" http://127.0.0.1:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://liuu.tk "$FILE_PATH" )
          # hash=$( bash "$SH_PATH/upload_to_ipfs.sh" https://ipfs.infura.io:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://snap1.d.tube "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" http://127.0.0.1:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://liuu.tk "$FILE_PATH" )
          # hash=$(auto_to_all)
        auto_to_all || {
          # hash=$( cd ~/nft-storage-quickstart && node ntf.storage.mjs "$FILE_PATH" wtfipfs "$fn" |grep -o -P 'baf[a-z0-9]+'|head -n1 ) && real_ipfs_url="https://$hash.ipfs.nftstorage.link/"
          hash=$( cd ~/vps/nft.storage && node nft.storage.mjs "$FILE_PATH" wtfipfs "$fn" |grep -o -P 'baf[a-z0-9]+'|head -n1 ) && real_ipfs_url="https://$hash.ipfs.nftstorage.link/"
        } || {
          echo "E: no open ipfs gateway" >&2
          [[ -e "$LP/$fn" ]] || cp "$FILE_PATH" "${LP}/"
          echo "tmp link: https://$DOMAIN/$(bash "$SH_PATH/"urldecode.sh "$fn")" >&2
        }

        if [[ -z "$hash" ]]; then
          :
        else
          :
#          nohup echo $( bash "$SH_PATH/upload_to_ipfs.sh" https://snap1.d.tube "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://ipfs.infura.io:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" http://127.0.0.1:5001 "$FILE_PATH" || bash "$SH_PATH/upload_to_ipfs.sh" https://liuu.tk "$FILE_PATH" ) &>/dev/null &
        fi
#        [[ -z "$hash" ]] && hash=$(ipfs add --cid-version 1 -n -Q "$FILE_PATH")
        # ipfs_url="https://$hash.ipfs.infura-ipfs.io/?filename=$(bash "$SH_PATH/"urldecode.sh "$fn")"
        ipfs_url="${real_ipfs_url}?filename=$(bash "$SH_PATH/urlencode.sh" "$fn")"
        # [[ -z "$hash" ]] && hash=$(ipfs add -n -Q "$FILE_PATH") && ipfs_url="https://ipfs.io/ipfs/$hash?filename=$(bash "$SH_PATH/urldecode.sh" "$fn")"
        # [[ -z "$hash" ]] && hash=$(ipfs add -n -Q "$FILE_PATH") && ipfs_url="https://ipfs.crossbell.io/ipfs/$hash?filename=$(bash "$SH_PATH/urldecode.sh" "$fn")"
        [[ -z "$hash" ]] && hash=$(ipfs add -n -Q "$FILE_PATH") && ipfs_url="https://ipfs.crossbell.io/ipfs/$hash"
        [[ -z "$hash" ]] && echo "E: empty cid" && return 1
        #    ipfs_url="https://ipfs.io/ipfs/$hash?filename=$(bash "$SH_PATH/"urldecode.sh "$fn")"
#        ipfs_url="https://snap1.d.tube/ipfs/$hash?filename=$(bash "$SH_PATH/"urldecode.sh "$fn")"
#        ipfs_url="https://ipfs.infura.io/ipfs/$hash?filename=$(bash "$SH_PATH/"urldecode.sh "$fn")"
        # echo "ipfs: $ipfs_url"
        if [[ "$2" == "tmp" ]]; then
          [[ -e "$LP/$fn" ]] || cp "$FILE_PATH" "${LP}/"
          # cd "${LP}/"
          # echo "tmp: https://$DOMAIN/$(bash "$SH_PATH/"urldecode.sh "$fn")"
          echo "https://$DOMAIN/$(bash "$SH_PATH/"urldecode.sh "$fn")"
        elif [[ "$2" == "all" ]]; then
          ipfs_hash_to_urls "$hash?filename=$(bash "$SH_PATH/"urldecode.sh "$fn")"
          [[ -e "$LP/$fn" ]] || cp "$FILE_PATH" "${LP}/"
          echo "tmp: https://$DOMAIN/$(bash "$SH_PATH/"urldecode.sh "$fn")"
        else
          echo "$ipfs_url"
        fi
      else
        echo "too big file"
        [[ -e "$LP/$fn" ]] || cp "$FILE_PATH" "${LP}/"
        echo "tmp: https://$DOMAIN/$(bash "$SH_PATH/"urldecode.sh "$fn")"
        return 1
      fi
    else
      echo "empty file"
      return 2
    fi
  else
    echo "no file"
    return 3
  fi

}
file_to_ipfs "$@"
