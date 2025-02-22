#!/bin/bash
SH_PATH=${SH_PATH-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}

gateway=$1
username=$2
text=$3

res=$4

if [[ "$gateway" != "gateway2" && $(echo "$text" | wc -l) -eq 1 ]]; then
    if [[ $(echo "$text" | grep -c -P "^https://twitter\.com/[a-zA-Z0-9_./?=%-]+$") -eq 1 ]]; then
      text=".tw $text"
    elif [[ $(echo "$text" | grep -c -P "^https://liuu\.tk/[a-zA-Z0-9_./?=%-]+$") -eq 1 ]]; then
      text=".ipfs $text only"
    elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-z.-]+\.[a-z]+(:[0-9]+)?/?[\S]*$") -eq 1 ]]; then
      text=".type $text"
    fi
  fi
fi



# text=$(bash "$SH_PATH/cmd.sh" "$@")
# text=$(bash "$SH_PATH/cmd.sh" "$text" )
text=$(bash "$SH_PATH/cmd.sh" "$text" "$res" )
[[ -n "$text" ]] && curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "$text" $gateway )" http://127.0.0.1:4243/api/message &>/dev/null
