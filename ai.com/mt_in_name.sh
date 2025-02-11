#!/bin/bash
#for matterbridge inMessgae temgo ( change username )
#cmd := os.exec("/run/user/1000/mt_in.sh", msgText, msgUsername, msgChannel, msgAccount)



if [[ "$2" == "blockthismessage" ]]; then
    echo -n "$2"
    exit 0
fi
NAME="$2"
if [[ -z "${NAME}" ]]; then
#  echo -n "$2"
  exit 0
fi

[[ $( echo "${NAME}" | wc -l ) -ge 3 ]] && echo -n "$2" && exit 0
[[ "${NAME:0:1}" == ">" ]] && echo -n "$2" && exit 0
[[ "${NAME:0:2}" == "> " ]] && echo -n "$2" && exit 0
[[ "${NAME:1:1}" == " " ]] && [[ "${NAME: -2}" == ": " ]] && echo -n "$2" && exit 0

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

URL="$1"

log_msg(){
  echo "#### in ####"
  local i=0
  for i in "$@"
  do
    echo -n "||$i"
  done
  echo
  echo "#### end ####"
}

block_msg(){
#    log_msg "$@" &>> ~/tera/mt.log
  echo -n "blockthismessage"
    # test_cmd || true
    # echo test_error 1>&2
  # exit 1
  exit 0
}




# cmd := os.exec("/home/liqsliu/twitter_to_text.sh", msgText, msgUsername, msgChannel, msgAccount)
# $4:telegram.mytelegram


LABLE="C"
# echo "$LABLE ${NAME}:"
# if [[ "$4" == "xmpp.myxmpp" ]]; then


if [[ "${1}" == "testbl" ]]; then
  if [[ "${3}" == "nagonuqo" ]]; then
    block_msg
  fi
fi



case $4 in
# xmpp.myxmpp|xmpp.myxmpp2)
xmpp.*)
  LABLE="X"
  if [[ $(echo "$URL" | head -n1 | grep -c -P "^>") -eq 1 && $(echo "$URL" | sed '/^[^>]/,$!d' | grep -c -P "^>") -eq 0 && $(echo "$URL" | sed -n '/^>/!p' | sed -n '/^$/!p' | wc -l) -ge 1 ]]; then
#URL=$( echo "$URL" | sed "s/^> \[/\n> \[/" )

    #reply before msg
    # URL=$( echo "$URL" | sed '/^[^>]/,$!d'; echo; echo "$URL" | sed '/^[^>]/,$d' )
    #reply before msg
    #URL=$( echo "$URL" | sed '/^[^>]/,$d'; echo; echo -n "$LABLE ${NAME}: "; echo "$URL" | sed '/^[^>]/,$!d' )
    #for name
    # URL=$( echo "$URL" | sed '/^[^>]/,$d'; echo -ne "\n"; echo "$LABLE ${NAME}: " )
    QT=$( echo "$URL" | sed -n '/^> /p')
    if [[ "$(echo "$QT"|head -n1)" == "> bot wrote:" ]]; then
      QT=$( echo "$QT" | sed '1d')
#    elif [[ "$(echo "$QT"|head -n1|grep -c -P '^> [a-zA-Z0-9_]+ wrote:$')" -eq "1" ]]; then
    elif [[ "$(echo "$QT"|head -n1|grep -c -P '^> .+ wrote:$')" -eq "1" ]]; then
      nick=$(echo "$QT"|head -n1|cut -d ' ' -f2)
      QT=$( echo "$QT" | sed '1d')
      QT=$( echo "$QT" | sed "1s/^> /> X ${nick}: /")
    elif [[ "$(echo "$QT"|head -n1)" == "> bot:" ]]; then
      # monocles
      QT=$( echo "$QT" | sed '1,2d')
    elif [[ "$(echo "$QT"|head -n1|grep -c -P '^> .+:$')" -eq "1" && "$(echo "$QT"|sed -n '2p'|grep -c -P '^> [0-9]{4}-[0-9]{2}-[0-9]{2}  [0-9]{2}:[0-9]{2}')" -eq "1" ]]; then
      # monocles
      nick=$(echo "$QT"|head -n1|cut -d ' ' -f2)
      QT=$( echo "$QT" | sed '1,2d')
      QT=$( echo "$QT" | sed "1s/^> /> X ${nick} /")
    fi
  fi
  ;;
# elif [[ "$4" == "telegram.mytelegram" ]]; then
telegram.mytelegram)
  LABLE="T"
  if [[ "$2" == "Telegram" ]]; then
# https://github.com/42wim/matterbridge/pull/1272
#    echo "block the msg" &>> ~/tera/test_tengo.log
    echo -n "blockthismessage"
    # echo -n "bot"
    exit 0
  fi

  if [[ "${URL:0:15}" == "Forwarded from " ]]; then
    # echo -n "bot"
    echo -n "blockthismessage"
    exit 0
  fi



  if [[ $(echo "$URL" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
    QT=$( python3 "$SH_PATH/get_msg.py" reply_msg "$(echo "$URL" | sed '/^> reply_from_telegram$/,$d')" "$2" "$3" ) || QT=""
    [[ -z "$QT" ]] && QT=$( echo "$URL" | sed '0,/^> reply_from_telegram$/d' )
    QT=$(echo "$QT" | sed '1s/^T bot: //' | sed 's/^/> /' )

  fi

  if [[ "$NAME" == "Group" ]]; then
    NAME="liqsliu"
  elif [[ "$NAME" == "‏⁠‎ l​i​q​s‏l​i​u​‎" ]]; then
    NAME="liqsliu"
  fi
  ;;
# elif [[ "$4" == "matrix.mymatrix" ]]; then
# matrix.mymatrix)
matrix.*)
  LABLE="M"
#  log_msg "$@" &>> ~/tera/mt.log

_chang_name_from_bifrost(){
  # local matrix_name=$1
  if [[ "$(echo "${matrix_name%%=40*}" | wc -m )" -le 2 ]]; then
    matrix_name=${matrix_name%%=2f*}
    matrix_name=$(echo "${matrix_name}" | sed "s/=40/@/")
  else
    matrix_name=${matrix_name%%=40*}
  fi
  # echo -n "$matrix_name"
}
chang_name_from_bifrost(){
  # local matrix_name=$1
  if [[ "${matrix_name: -12}" == ":libera.chat" ]]; then
    LABLE=I
  elif [[ "${matrix_name: -13}" == ":aria-net.org" ]]; then
    if [[ "${matrix_name:0:9}" == "_bifrost_" ]]; then
      LABLE="X"
      matrix_name=${matrix_name:9}
      _chang_name_from_bifrost
    fi
  elif [[ "${matrix_name: -11}" == ":matrix.org" ]]; then
    if [[ "${matrix_name:0:6}" == "_xmpp_" ]]; then
      LABLE="X"
      matrix_name=${matrix_name:6}
      _chang_name_from_bifrost
      return 0
    elif [[ "${matrix_name%%=40*}" == "_neb_rssbot_" ]]; then
      LABLE="M"
      # NAME="rssbot"
      matrix_name=rssbot
      return 0
    fi
    return 1
  elif [[ "${matrix_name##*:}" == "t2bot.io" ]]; then
    if [[ "${matrix_name:0:9}" == "_discord_" ]]; then
      block_msg
      LABLE="D"
    elif [[ "${matrix_name:0:9}" == "telegram_" ]]; then
      block_msg
      LABLE="T"
    fi
  else
    return 1
  fi
}


chang_name_from_matrix(){
  # local matrix_name=$1
  # if is_bifrost "$matrix_name"; then
    # matrix_name=$(chang_name_from_bifrost "$matrix_name")
  if chang_name_from_bifrost; then
    :
  else
    # if [[ "$(echo "$matrix_name" | cut -d':' -f2 )" == "matrix.org" ]]; then
    if [[ "${matrix_name##*:}" == "matrix.org" ]]; then
      matrix_name=$(echo "$matrix_name" | cut -d':' -f1)
    else
      # if [[ "$(echo "$matrix_name" | cut -d':' -f1 | wc -m )" -gt 3 ]]; then
      if [[ "$(echo "${matrix_name%%:*}" | wc -m )" -gt 3 ]]; then
        matrix_name=$(echo "$matrix_name" | cut -d':' -f1)
      fi
    fi
  fi
  # echo -n "$matrix_name"
}

chang_name_for_qt_from_matrix(){
  local qt_tmp=$1
  username=$(echo "$qt_tmp" | head -n1 | grep -o -P "> <@[a-zA-Z0-9_]+:[0-9a-zA-Z.-]+\.[a-zA-Z]+> ")
  if [[ -n "$username" ]]; then
#      qt_tmp=$(echo "$qt_tmp" | sed "1s|^$username||" )
    qt_tmp=$(echo "$qt_tmp" | sed "1s|$username|matrix_username|" )
    username=$(echo "$username" | cut -d"@" -f2 | cut -d ">" -f1 )
    username=$(chang_name_from_matrix "$username")
#      qt_tmp=$( echo -n "> M ${username}: "; echo "$qt_tmp")
    username="> M ${username}: "
    qt_tmp=$(echo "$qt_tmp" | sed "1s|matrix_username|$username|" )
  fi
  echo -n "$qt_tmp"

}

  # NAME=$(chang_name_from_matrix "$NAME")
  matrix_name=$NAME
  chang_name_from_matrix
  NAME=$matrix_name

  # # aria-net's bug
  # if [[ "$3" == "#ipfsrss:matrix.org" ]]; then
  #   if [[ "$NAME" != "rssbot" ]]; then
  #     block_msg
  #   fi
  # fi

  #for reply from matrix
  if [[ $(echo "$URL" | grep -c -G "^$" ) -ge 1 && $(echo "$URL" | head -n 1 | grep -c -G "^>" ) -eq 1 && $(echo "$URL" | sed '0,/^$/d' | grep -c -P "^>") -eq 0 && $(echo "$URL" | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$URL" | sed '/^$/,$d' | wc -l ) ]]; then
    # URL=$( echo "$URL" | sed "1s/^> <@wtfipfs:matrix.org> /> /" )



#    QT=$( echo "$URL" | sed "1s/^> <@wtfipfs:matrix.org> /> /" | sed '/^$/,$d' )
    QT=$( echo "$URL" | sed "1s/^> <@wtfipfs:matrix.org> /> /" )
    QT=$( echo "$QT" | sed -E '/^([^$>]|>[^ ])/,$d' )
#    username=$(echo "$QT" | head -n1 | grep -o -P "^> <@[a-zA-Z0-9_]+:[0-9a-zA-Z.-]+\.[a-zA-Z]+> ")

    QT=$(chang_name_for_qt_from_matrix "$QT")

  elif [[ $(echo "$URL" | sed '/^> [^>]/,$!d' | grep -c -G "^$" ) -ge 1 && $(echo "$URL" | head -n 1 | grep -c -G "^> " ) -eq 1 && $(echo "$URL" | sed '/^$/,$d' | grep -c -P "^> ") -ge 1 && $(echo "$URL" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$URL" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | wc -l ) ]]; then

    # just quote
#    QT=$( echo "$URL" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' )
#    QT=$( echo "$URL" | sed '/^[^$>]/,$d' | sed '/^>[^ ]/,$d' )
    QT=$( echo "$URL" | sed -E '/^([^$>]|>[^ ])/,$d' )
    QT=$(chang_name_for_qt_from_matrix "$QT")
  fi
  ;;
zulip.myzulip)
  LABLE="Z"
  # if [[ $(echo "$URL" | grep -c -P "^\[.*\]\(/user_uploads/.*\)$" ) -eq 1 ]]; then
  #   URL="${URL%](/user_uploads/*}](https://wtfipfs.zulipchat.com/user_uploads/${URL##*](/user_uploads/}"
  # fi
  ;;
api.tox)
  LABLE="O"
  ;;
irc.myirc)
  LABLE="I"
  ;;
irc.irc2p)
  LABLE="2"
  ;;
discord.mydiscord)
  LABLE="D"
      # block_msg
  # if [[ "$3" == "wtfipfs" ]]; then
    # if [[ "${NAME##*#}" == "0000" ]]; then
  if echo "${NAME}" | grep -q -P ".+#[0-9]{4}$"; then
    NAME=${NAME%#*}
  else
    block_msg
  fi
  if [[ "$2" == "Telegram Bridge" ]]; then
      echo -n "blockthismessage"
      exit 0
#    if [[ "${URL:0:15}" == "Forwarded from " ]]; then
    if [[ "${URL:0:31}" == "Forwarded message from channel " ]]; then
      echo -n "blockthismessage"
      exit 0
    fi
  fi

  ;;
api.in)
  LABLE="0"
  ;;
api.cmd)
  LABLE="C"
  ;;
api.cmdres)
  LABLE="C"
  ;;
api.tg)
  LABLE="T"
  ;;
*)
  LABLE="R"
  ;;
esac

if [[ "$(echo "$QT" | head -n1 | grep -c -G "^> >" )" -eq 1 ]]; then
#    if [[ "$(echo "$QT" | grep -c -G "^> $" )" -eq 1 ]]; then
#    QT=$( echo "$QT" | sed '0,/^> $/d' )

#    QT=$( echo "$URL" | sed '/^[^$>]/,$d' | sed '/^>[^ ]/,$d' )
  QT=$( echo "$QT" | sed '/^> [^>]/,$!d' )
fi

#QT=$( echo "$URL" | sed '/^$/,$d')
if [[ "$(echo "$QT" | tail -n1 | grep -c -G "^$" )" -eq 1 ]]; then
  QT=$( echo "$QT" | sed '$d')
fi


if [[ "$LABLE" == "0" ]]; then
echo -n "${NAME}: "
else
[[ -z "$QT" ]] && echo -n "$LABLE ${NAME}: " || echo -n "$QT

$LABLE ${NAME}: "
fi
