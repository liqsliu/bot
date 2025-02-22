#!/bin/bash

if [[ "$2" == "blockthismessage" ]]; then
    exit 0
fi

if [[ "$2" == "" ]]; then
  exit 0
fi
#cmd2 := os.exec("/run/user/1000/mt_out_name.sh", msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent)
block_msg(){
  exit 0
}

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

URL="$1"
NAME="$2"

if [[ -n "$4" ]] ; then
  if [[ "$9" == "xmpp" ]] ; then
    if [[ "$2" == "C twitter: " ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' )
    elif [[ "$2" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /')
    elif [[ "$NAME" == "M rssbot: " ]]; then
      NAME=$(echo "$URL" | cut -d ":" -f 1)
      URL=$(echo "$URL" | cut -d ":" -f 2-)
      NAME="**${NAME}:** "
      echo -n "$NAME"
    fi
  elif [[ "$9" == "irc" ]] ; then
#    echo -n "$(echo "$2" | tail -n1)"
    URL=$(echo "$URL" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
      if [[ "$(echo "$2" | wc -l)" -ge 3 ]]; then
        QT=$(echo "$2" | head -n 1 | sed 's/> //' )
        URL="$URL RE: $QT"
      fi
  elif [[ "$9" == "matrix" ]] ; then
    if [[ "$2" == "C twitter: " ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' | sed '2s/^/\n/')
    elif [[ "$2" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' | sed '2s/^/\n/')
    elif [[ "$2" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' | sed '2s/^/\n/')
    else
      # if [[ -n "$(echo "$2" | sed '$d')" ]]; then
      if [[ "$(echo "$2" | wc -l)" -ge 3 ]]; then
        echo "$2" | sed '$d'
      fi
    fi
#    echo -n "$(echo "$2" | tail -n1)"
    NAME=$(echo "$NAME" | tail -n1)
    NAME=$(echo "$NAME" | cut -d ":" -f 1)
    NAME="**${NAME}:** "
    echo -n "$NAME"
  elif [[ "$9" == "zulip" ]] ; then
    if [[ "$2" == "C twitter: " ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' )
    elif [[ "$2" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /')
    elif [[ "$2" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /')
    fi
  elif [[ "$9" == "discord" ]] ; then
    if [[ "$2" == "C twitter: " ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /' )
    elif [[ "$2" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /')
    elif [[ "$2" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      URL=$(echo "$URL" | sed '2,$s/^/> /')
    fi
    if [[ "$(echo "$2" | wc -l)" -ge 3 ]]; then
      echo "$2" | sed '$d'
    fi
  elif [[ "$9" == "telegram" ]] ; then
    if [[ "$2" == "C twitter: " ]]; then
      exit 0 # another bot
    fi
    if [[ "$2" == "C twitter: " ]]; then
      URL='.>)\`'
    elif [[ "$3" == "api.tg" && "$11" != "gateway0" ]]; then
      URL='.>)\`'
    elif [[ $(echo "$NAME" | wc -l) -ge 3 ]]; then
#      NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME" | tail -n1 | sed 's/ / */' | sed 's/: $/*: /' )
      last=$(echo "$NAME" | tail -n1)

      NAME=${last%: *}
      P=${NAME:0:1}
      NAME=${NAME:2}
      NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME")
      NAME="$P *${NAME}*: "

      qt_text=$(echo "$2" | sed '/^> /!d' | sed 's/^> //')
      line1=$(echo "$qt_text" | head -n1)

      if [[ "${line1:0:2}" == "T " || "${line1%%: *}" == "C twitter" ]]; then

        msg_text=$(echo "${line1#*: }"; echo "$qt_text" |sed '1d')
        msg_text=$(echo "$msg_text" | sed -r '$s|: https://liuu\.tk/[a-zA-Z0-9_./?=%-]+$||')

#        msg_sender=$(echo "$2" | head -n1 | cut -d' ' -f3- | cut -d':' -f1 )
        msg_sender="${line1%%: *}"
        msg_sender="${msg_sender#* }"


      else
        msg_sender="bot"
        if [[ $( echo "$line1" | grep -c -P '^[A-Z] .*: .*' ) -eq 1 ]]; then
          msg_text=$qt_text
        else
          msg_text="$P ?: $qt_text"
        fi
      fi
      bash "$SH_PATH/tg.sh" settoken wtfipfs setcid "${10}" "--reply" "$msg_text" "$msg_sender" "--md" "$NAME$(bash "$SH_PATH/text2markdown.sh" "$1")"
      URL='.>)\`'
    else
      URL=$(bash "$SH_PATH/text2markdown.sh" "$URL")
    fi
  fi
fi

echo -n "$URL"
