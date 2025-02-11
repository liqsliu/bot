#!/bin/bash
# https://api.muxiaoguo.cn/
#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
#SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}


get_text(){
  [[ $( echo "$*" | wc -l ) -gt 1 ]] && text=$(echo "$*" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g") || text="$*"
  text=$(echo "$text" | cut -d $'\t' --output-delimiter='\t' -f 1- | cut -d '"' --output-delimiter='\"' -f 1- )
cat <<EOF
{"text":"${text}"}
EOF
}

#https://github.com/itorr/nbnhhsh
nbnhhsh(){
  if [[ -z "$1" ]]; then
    echo "能不能好好说话？(翻译看不懂的拼音缩写)"
#    echo ".hhsh \$text"
    echo "用法: .hhsh 缩写"
    echo "https://github.com/itorr/nbnhhsh"
    echo "https://lab.magiconch.com/api/nbnhhsh/guess"
  else
    res=$( curl -s -XPOST -H 'Content-Type: application/json' -d "$(get_text "$@")" https://lab.magiconch.com/api/nbnhhsh/guess )
    # res=$( curl -v -XPOST -H 'Content-Type: application/json' -d "$(get_text "$@")" https://lab.magiconch.com/api/nbnhhsh/guess )

    echo -n $(echo "$res" | jq -r ".[0].name")
    echo -n ":"
    # echo "$res" | jq -r ".[0].trans[0]"
    local i
    for (( i=0 ; i<64 ; i++   ))
    do
      local trans=$(echo "$res" | jq -r ".[0].trans[$i]")
      [[ "$trans" == "null" ]] && break || echo -n " $trans"
    done
    echo
  fi
}


nbnhhsh "$@"
