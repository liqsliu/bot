#!/bin/bash

#for matterbridge inMessage tengo
#cmd := os.exec("/run/user/1000/mt_in.sh", msgText, msgUsername, msgChannel, msgAccount)


if [[ "$2" == "blockthismessage" ]]; then
  exit 0
fi

if [[ "$1" == "" ]]; then
  exit 0
fi



URL="$1"

block_msg(){
  # echo -n "blockthismessage"
  exit 0
}

# cmd := os.exec("/home/liqsliu/sh", msgText, msgUsername, msgChannel, msgAccount)
# $4:telegram.mytelegram



# echo "$LABLE ${2}:"



#xmpp
if [[ "$4" == "xmpp.myxmpp" || "$4" == "xmpp.myxmpp2" ]]; then
  if [[ $(echo "$URL" | head -n1 | grep -c -P "^>") -eq 1 && $(echo "$URL" | sed '/^[^>]/,$!d' | grep -c -P "^>") -eq 0 && $(echo "$URL" | sed -n '/^>/!p' | sed -n '/^$/!p' | wc -l) -ge 1 ]]; then
    #URL=$( echo "$URL" | sed "s/^> \[/\n> \[/" )
    URL=$( echo "$URL" | sed '/^[^>]/,$!d')
  fi

#telegram
elif [[ "$4" == "telegram.mytelegram" ]]; then
  if [[ "$2" == "Telegram" ]]; then
    block_msg
  fi
  if [[ "${URL:0:15}" == "Forwarded from " ]]; then
#    URL=$( echo "${URL}" | sed -r '1s/[^:]+: //' )
    block_msg
  fi

  if [[ $(echo "$URL" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
    #skip nick
    URL=$(echo "$URL" | sed '/^> reply_from_telegram$/,$d';)
  fi

#matrix
elif [[ "$4" == "matrix.mymatrix" ]]; then

log_msg(){

  echo "#### in ####"
  local i=0
  for i in "$@"
  do
    echo -n "||$i"
  done
  echo
  echo
}

#log_msg "$@" &>> ~/tera/mt.log

  if [[ "$2" == "coybot beta" ]]; then
    block_msg
  fi
  if [[ $(echo "$URL" | grep -c -G "^$" ) -ge 1 && $(echo "$URL" | head -n 1 | grep -c -G "^>" ) -eq 1 && $(echo "$URL" | sed '0,/^$/d' | grep -c -P "^>") -eq 0 && $(echo "$URL" | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$URL" | sed '/^$/,$d' | wc -l ) ]]; then
    URL=$( echo "$URL" | sed -E '/^([^$>]|>[^ ])/,$!d' )
  elif [[ $(echo "$URL" | sed '/^> [^>]/,$!d' | grep -c -G "^$" ) -ge 1 && $(echo "$URL" | head -n 1 | grep -c -G "^> " ) -eq 1 && $(echo "$URL" | sed '/^$/,$d' | grep -c -P "^> ") -ge 1 && $(echo "$URL" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$URL" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | wc -l ) ]]; then
    URL=$( echo "$URL" | sed -E '/^([^$>]|>[^ ])/,$!d' )
  fi

else
#  URL="$LABLE ${2}: $URL"
:
fi


echo -n "$URL"
exit 0
