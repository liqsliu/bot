#!/bin/bash
#background cmd

SH_PATH=${SH_PATH:-$(
  cd $(dirname ${BASH_SOURCE[0]})
  pwd
)}

cmds() {
  if [[ "$1" == "ping" || "$1" == ".ping" ]]; then
    echo pong
    return 0
  fi
  if [[ "${1:0:1}" != "." ]]; then
    return 0
  fi
  case ${1:1} in
  help | h)
    if [[ -z "$2" ]]; then
      [[ -e "$SH_PATH/group_help.txt" ]] && cat "$SH_PATH/group_help.txt" || echo "E: no group_help.txt"
    else
      [[ -e "$SH_PATH/group_help_${2}.txt" ]] && cat "$SH_PATH/group_help_$2.txt" || echo "E: no group_help_${2}.txt"
    fi
    ;;
  ping)
    echo -n $(ping -W 5 -c 1 $(echo $2 | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+") | cut -d "=" -s -f4 | cut -d " " -f1 | cut -d"." -f1)
    echo ms
    ;;
  dig)
    shift
    [[ -z "$2" ]] && echo "$(dig +short "$@" || echo "E: $?")" || echo "$(dig "$@" || echo "E: $?")"
    ;;
  google)
    shift
    bash "$SH_PATH/google.sh" "$@" || echo "E: $?"
    ;;
  tw)
    if [[ -z "$2" ]]; then
      echo ".tw \$URL [all|tmp|*only dtube]"
    else
      shift
      bash "$SH_PATH/twitter_to_text.sh" "$@" || echo "E: $?"
    fi
    ;;
  ip | nali*)
    if [[ -z "$2" ]]; then
      echo "ip nali nali-cat nali-dig nali-mtr nali-nslookup nali-ping nali-tracepath nali-traceroute"
    else
      if [[ "$1" == ".ip" ]]; then
        if [[ $(echo "$2" | grep -c -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1) -eq 1 ]]; then
          echo ".nali-dig +short $(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)"
          echo -n "src=us: "
          nali-dig +short "$(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)" || echo "E: $?"
          echo -n "src=cn: "
          nali-dig @8.8.8.8 +subnet=114.114.114.114/24 +short "$(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)" || echo "E: $?"
        elif [[ $(echo "$2" | grep -c -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+") -eq 1 ]]; then
          echo "$(echo "$2" | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")"
          echo -n "纯真: "
          nali "$(echo "$2" | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")" | grep -o -P "\[.*\]" | grep -o -P "[^[\]]+" || echo "E: $?"
          echo -n "木小果: "
          curl -s "https://api.muxiaoguo.cn/api/ip?ip=$(echo "$2" | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")&type=b" | jq -r ".data.Geographical_location" || echo "E: $?"
        else
          echo "W: 格式不正确: $2"
        fi
      else
        nali=${1:1}
        shift
        "$nali" "$@" || echo "E: $?"
      fi
    fi
    ;;
  ipfs)
    if [[ -z "$2" ]]; then
      echo ".ipfs \$URL [all|tmp|*only dtube]"
    else
      echo "ipfs for: $2"
      bash "$SH_PATH/file_to_ipfs.sh" "$(bash "$SH_PATH/link_to_file.sh" $2)" "${3}" || echo "E: $?"
    fi
    ;;
  tq)
    if [[ -z "$2" ]]; then
      echo ".tq 北京"
    else
      shift
      bash "$SH_PATH/muxiaoguo.sh" tianqi "$@"
    fi
    ;;
  tr)
    if [[ -z "$2" ]]; then
      echo ".tr 你好"
    else
      shift
      bash "$SH_PATH/muxiaoguo.sh" Tn_google "$@"
    fi
    ;;
  type)
    if [[ -z "$2" ]]; then
      echo ".type \$URL"
    else
      bash "$SH_PATH/link_to_file.sh" "$2" type || echo "E: $?"
    fi
    ;;
  note)
    shift
    bash "$SH_PATH/note.sh" "$username" "$@" || echo "E: $?"
    ;;
  uptime)
    if [[ -z "$2" ]]; then
      uptime
    fi
    ;;
  testcmd)
    if [[ -z "$2" ]]; then
      nali-dig -h
    fi
    ;;
  *)
    echo "E: unknown cmd > $*"
    ;;
  esac
}

gateway=$1
username=$2
text=$3
res=$4

text=$(cmds $text)
[[ -n "$text" ]] && {
  res=$(curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "$text" $gateway)" http://127.0.0.1:4243/api/message)
  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "E: $(echo "$res" | jq -r ".message")" $gateway)" http://127.0.0.1:4243/api/message
  else
    [[ -z "$(echo "$res" | jq -r ".text")" ]] && curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "E: empty message" $gateway)" http://127.0.0.1:4243/api/message
  fi
}
