#!/bin/bash
# get cmd string
# out cmd return

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}



cmds(){
  local cmd="$*"
  # if [[ "${cmd:0:5}" == ".cmd " ]]; then
  if [[ "$1" == ".cmd" ]]; then
    cmd=${cmd#\'cmd }
    local iscmd=1
  fi

  if [[ "$cmd" == "ping" || "$cmd" == ".ping" ]]; then
    echo pong
  elif [[ "$1" == "help" || "$1" == ".help" || "$1" == ".h" ]]; then
  	if [[ -z "$2" ]]; then
      [[ -e "$SH_PATH/group_help.txt" ]] && cat "$SH_PATH/group_help.txt" || echo "E: no group_help.txt"
  	else
      [[ -e "$SH_PATH/group_help_${2}.txt" ]] && cat "$SH_PATH/group_help_$2.txt" || echo "E: no group_help_${2}.txt"
	fi
  elif [[ "$1" == ".ping" && $(echo $2 | grep -c -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+") -eq 1 ]]; then
    echo -n $(ping -c 1 $(echo $2 | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" ) | cut -d "=" -s -f4 | cut -d " " -f1 | cut -d"." -f1)
    echo ms
  elif [[ "$1" == ".dig" ]]; then
    shift
    [[ -z "$2" ]] && echo "$(dig +short "$@" || echo "E: $?" )" || echo "$(dig "$@" || echo "E: $?" )"
  elif [[ "$1" == ".google" ]]; then
    shift
    bash "$SH_PATH/google.sh" "$@" || echo "E: $?"
  elif [[ "$1" == ".tw" ]]; then
  	if [[ -z "$2" ]]; then
      echo ".tw \$URL [all|tmp|*only dtube]"
    else
      shift
      bash "$SH_PATH/twitter_to_text.sh" "$@" || echo "E: $?"
    fi
  elif [[ "$1" == ".ip" || "${1:0:5}" == ".nali" ]]; then
  	if [[ -z "$2" ]]; then
      echo "ip nali nali-cat nali-dig nali-mtr nali-nslookup nali-ping nali-tracepath nali-traceroute"
    else
      if [[ "$1" == ".ip" ]]; then
        if [[ $(echo "$2" | grep -c -P "[0-9a-z.-]+\.[a-z]+") -eq 1 ]]; then
          nali-dig +short "$(echo "$2" | grep -o -P "[0-9a-z.-]+\.[a-z]+")" || echo "E: $?"
        else
          nali "$2" || echo "E: $?"
        fi
      else
        nali=${1:1}
        shift
        "$nali" "$@" || echo "E: $?"
      fi
    fi
  elif [[ "$1" == ".ipfs" ]]; then
  	if [[ -z "$2" ]]; then
      echo ".ipfs \$URL [all|tmp|*only dtube]"
    else
      echo "ipfs for: $2"
      bash "$SH_PATH/file_to_ipfs.sh" "$(bash "$SH_PATH/link_to_file.sh" $2)" "${3}" || echo "E: $?"
    fi
  elif [[ "$1" == ".type" ]]; then
  	if [[ -z "$2" ]]; then
      echo ".type \$URL"
    else
      bash "$SH_PATH/link_to_file.sh" "$2" type|| echo "E: $?"
    fi
  elif [[ "$1" == ".note" ]]; then
    shift
    bash "$SH_PATH/note.sh" "$(echo "$res" | jq -r ".username")" "$@" || echo "E: $?"
  else
    if [[ "$iscmd" == "1" ]]; then
      echo "E: unknown cmd > $cmd"
    fi
  fi
}

text=$1
res=$2
cmds $text
