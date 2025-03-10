#!/bin/bash

tgp
cd ~/bot/ && bash init.sh || exit 1

cd ~/

while true; do
#./matterbridge "$@" || bash tg.sh "matterbridge exit $?"
./mt "$@"
r=$?
# bash tg.sh "matterbridge exit $?"
# bash ~/bot/sm.sh "C cmd" "mt stopped" 4249 test
echo "res: $r"
date
if [[ "$r" -eq 143 ]]; then
  echo "killed by pkill"
  echo 'restart ...'
elif [[ "$r" -eq 0 ]]; then
  echo 'wtf ...'
else
  echo 'stop ...'
  break
fi

sleep 1
done

exit 0

TTY=$(tty)
echo $TTY
msg=$( ./matterbridge 2>&1 | tee $TTY )

#./matterbridge 2>&1 | tee ~/tera/mt.log
#msg=$(cat ~/tera/mt.log)


bash tg.sh "$msg"



exit 0






exit

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

#log_msg "$@" &>> ~/tera/test_tengo.log

URL="$1"

# cmd := os.exec("/home/liqsliu/sh", msgText, msgUsername, msgChannel, msgAccount)
# $4:telegram.mytelegram

if [[ "$URL" == "" ]]; then
#  echo -n "$LABLE ${2}: "
  exit 0
fi


# echo "$LABLE ${2}:"



#xmpp
if [[ "$4" == "xmpp.myxmpp" ]]; then
  if [[ $(echo "$URL" | head -n 1 | grep -c -P "^>" ) -eq 1 && $(echo "$URL" | sed '/^[^>]/,$d' | grep -c -P "^>") -eq $(echo "$URL" | grep -c -P "^>") && $(echo "$URL" | sed '/^[^>]/,$!d' | wc -l) -ge 1 ]]; then

    #URL=$( echo "$URL" | sed "s/^> \[/\n> \[/" )

    #reply before msg
    # URL=$( echo "$URL" | sed '/^[^>]/,$!d'; echo; echo "$URL" | sed '/^[^>]/,$d' )
    #reply before msg
    #URL=$( echo "$URL" | sed '/^[^>]/,$d'; echo; echo -n "$LABLE ${2}: "; echo "$URL" | sed '/^[^>]/,$!d' )
    #skip nick
    URL=$( echo "$URL" | sed '/^[^>]/,$!d' )
  fi

#telegram
elif [[ "$4" == "telegram.mytelegram" ]]; then
  if [[ "$2" == "Telegram" ]]; then
    if [[ "${URL:0:22}" == "Forwarded from unknown" ]]; then
      URL="${URL:24}"
    fi
  fi
  if [[ $(echo "$URL" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
#URL=$( echo "$URL" | sed "s/^> \[bot\] /> /" )
#  URL=$(echo "$URL" | sed '/^> repley_from_telegram$/,$d'; echo; echo "$URL" | sed '0,/^> repley_from_telegram$/d' | sed 's/^/> /g' | sed 's/^> \[bot\] /> /')

    #reply before msg
    # URL=$(echo "$URL" | sed '/^> repley_from_telegram$/,$d'; echo; echo "$URL" | sed '0,/^> repley_from_telegram$/d' | sed 's/^/> /g' | sed 's/^> bot: /> /')
    #reply after msg
    #URL=$(echo "$URL" | sed '0,/^> reply_from_telegram$/d' | sed 's/^/> /g' | sed 's/^> bot: /> /'; echo; echo -n "$LABLE ${2}: "; echo "$URL" | sed '/^> reply_from_telegram$/,$d';)
    #skip nick
    URL=$(echo "$URL" | sed '/^> reply_from_telegram$/,$d';)
  fi

#matrix
elif [[ "$4" == "matrix.mymatrix" ]]; then
  if [[ $(echo "$URL" | grep -c -G "^$" ) -ge 1 && $(echo "$URL" | head -n 1 | grep -c -G "^>" ) -eq 1 && $(echo "$URL" | sed '0,/^$/d' | grep -c -P "^>") -eq 0 && $(echo "$URL" | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$URL" | sed '/^$/,$d' | wc -l ) ]]; then
  #for reply from matrix
    # URL=$( echo "$URL" | sed "s/^> <@wtfipfs:matrix.org> /> /" )

    #reply before msg
    # URL=$( echo "$URL" | sed '0,/^$/d'; echo; echo "$URL" | sed '/^$/,$d' )
    #reply after msg
    #URL=$( echo "$URL" | sed '/^$/,$d'; echo; echo -n "$LABLE ${2}: "; echo "$URL" | sed '0,/^$/d' )
    #skip nick
    URL=$( echo "$URL" | sed '0,/^$/d' )
  fi

else
#  URL="$LABLE ${2}: $URL"
:
fi


echo -n "$URL"
