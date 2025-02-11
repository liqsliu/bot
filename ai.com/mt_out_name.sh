#!/bin/bash

if [[ "$2" == "blockthismessage" ]]; then
    # echo -n "bot"
    echo -n "$2"
    exit 0
fi

if [[ "$2" == "" ]]; then
  exit 0
fi

#cmd2 := os.exec("/run/user/1000/mt_out_name.sh", msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent)
log_msg(){
  echo "#### out ####"
  echo "msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent"
  local i=0
  for i in "$@"
  do
    echo -n "||$i"
  done
  echo
  echo "#### end ####"
}

block_msg(){
  # echo "blockthismessage"
  echo -n "blockthismessage"
  exit 0
}


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

URL="$1"
NAME="$2"


if [[ -n "$4" ]] ; then
  if [[ "$9" == "xmpp" ]] ; then
    if [[ "$NAME" == "M rssbot: " ]]; then
      # forbid msg from ipfsrss sent by rssbot
      # if [[ "${11}" == "gateway1" ]]; then
      #   block_msg
      # fi
      exit 0
    fi
    [[ $(echo "$NAME" | wc -l) -ge 3 ]] && echo "$NAME" | sed '/^[^>]/d'
    NAME=$(echo "$NAME" | tail -n1)
    # NAME=$(echo "$NAME" | cut -d ":" -f 1)
    NAME=${NAME%: }
    NAME="**${NAME}:** "
  elif [[ "$9" == "telegram" ]] ; then
    if [[ "${10}" == "-1001193563578" ]] ; then
      block_msg
    fi
    [[ $(echo "$NAME" | wc -l) -ge 3 ]] && bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | sed '/^$/,$d')" && echo
    NAME=$(bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | tail -n1)")
    # echo -n "*$(echo "$NAME" | cut -d' ' -f 2- | sed '$s|: $||')*: "
    M=$(echo "$NAME" | cut -d' ' -f1)
    NAME=$(echo "$NAME" | cut -d' ' -f 2-)
    NAME=${NAME%: }
    echo -n "$M *$NAME*: "

    NAME=''
  elif [[ "$9" == "irc" ]] ; then
    NAME=$(echo "$NAME" | tail -n1)
  elif [[ "$9" == "matrix" ]] ; then
    if [[ "${5}" == "-1001193563578" ]] ; then
      if [[ "${10}" == "#ipfs:mozilla.org" ]] ; then
        block_msg
      fi
    fi
    tmp=$NAME
    NAME=$(echo "$NAME" | tail -n1)
    # NAME=$(echo "$NAME" | cut -d ":" -f 1)
    NAME=${NAME%: }
    NAME="**${NAME}:** "
    qt=$(echo "$tmp" | sed '$d')
    [[ -n "$qt" ]] && NAME="$qt
$NAME"
    if [[ -z "$1" ]]; then
#      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && [[ $(echo "$NAME" | grep -c -G '^$') -ge 1 ]] && echo "$NAME" | tail -n1 && echo "$NAME" | sed '/^$/,$d' && NAME=""
      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && NAME=$(echo "$NAME" | tail -n1; echo "$NAME" | sed '/^$/,$d')
    elif [[ "$1" == "Forwarded from unknown: " && $(echo "$NAME" | wc -l) -eq 1 ]] ; then
      :
    else
      NAME=""
    fi

  elif [[ "$9" == "discord" ]] ; then
    if [[ "${10}" == "wtfipfs" ]] ; then
      if [[ "${5}" == "#wtfipfs:matrix.org" ]] ; then
        block_msg
      fi
    elif [[ "${10}" == "wtfipfs2" ]] ; then
      # if [[ "${3}" != "api.in" ]] ; then
      if [[ "${5}" == "#ipfs:mozilla.org" ]] ; then
        block_msg
      fi
      if [[ "${5}" == "-1001193563578" ]] ; then
        block_msg
      fi
    fi
#     if [[ "$2" == "C twitter: " ]]; then
#       :
# #      NAME="bot"
#     else
#     fi
    NAME=$(echo "$NAME" | tail -n1)
    NAME="${NAME:0:-2}"
  fi
fi
echo -n "$NAME"
