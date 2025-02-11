#!/bin/bash


#echo "$@" >> ~/tera/t.log


# bash tg.sh getcid

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}



PRIVATE_KEYS_PATH="${HOME}/.ssh/private_keys.txt"

#wtfipfsbot
TELEGRAM_BOT_TOKEN_WTFIPFS=$(grep TELEGRAM_BOT_TOKEN_WTFIPFS "$PRIVATE_KEYS_PATH")
TELEGRAM_BOT_TOKEN_WTFIPFS=${TELEGRAM_BOT_TOKEN_WTFIPFS#* }
#liqsliu_bot
TELEGRAM_BOT_TOKEN_LIQSLIU=$(grep TELEGRAM_BOT_TOKEN_LIQSLIU "$PRIVATE_KEYS_PATH")
TELEGRAM_BOT_TOKEN_LIQSLIU=${TELEGRAM_BOT_TOKEN_LIQSLIU#* }


get_data(){
  local parse_mode=""
  if [[ $(echo "$@" | wc -l) -le 1 ]]; then
#    text="$(printf "%q" "${@}")"
    text="$(printf "%q" "${*}")"
  else
    text="$(printf "%q" "${*}")"
    #text="${text:2}"
    text="${text#\$\'}"
    text="${text%\'}"
    text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  fi
  cat << EOF
{
"chat_id": "$CID",
"text": "$text",
EOF
  if [[ "$isreply" == "1" && "$msgid" != "0" ]]; then
cat << EOF
"reply_to_message_id": "$msgid",
EOF
  fi
  cat << EOF
"disable_web_page_preview": "true"
}
EOF
#"disable_web_page_preview": "false"

}
get_md_old(){
  text="$*"
  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

  text="$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )"
  text="$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )"
  text="$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )"
  text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"

  # text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  cat << EOF
$text
EOF
}




conv_md(){
  text="$1"
  [[ "$2" == "MarkdownV2" ]] && {

  text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )
  text=$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )
  text=$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )
  text=$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )
  text=$(echo "$text" | cut -d ']' --output-delimiter='\]' -f 1- )
  text=$(echo "$text" | cut -d '(' --output-delimiter='\(' -f 1- )
  text=$(echo "$text" | cut -d ')' --output-delimiter='\)' -f 1- )
  text=$(echo "$text" | cut -d '~' --output-delimiter='\~' -f 1- )
  text=$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )
  text=$(echo "$text" | cut -d '>' --output-delimiter='\>' -f 1- )
  text=$(echo "$text" | cut -d '#' --output-delimiter='\#' -f 1- )
  text=$(echo "$text" | cut -d '+' --output-delimiter='\+' -f 1- )
  text=$(echo "$text" | cut -d '-' --output-delimiter='\-' -f 1- )
  text=$(echo "$text" | cut -d '=' --output-delimiter='\=' -f 1- )
  text=$(echo "$text" | cut -d '|' --output-delimiter='\|' -f 1- )
  text=$(echo "$text" | cut -d '{' --output-delimiter='\{' -f 1- )
  text=$(echo "$text" | cut -d '}' --output-delimiter='\}' -f 1- )
  text=$(echo "$text" | cut -d '.' --output-delimiter='\.' -f 1- )
  text=$(echo "$text" | cut -d '!' --output-delimiter='\!' -f 1- )

  } || {
    [[ "$2" == "HTML" ]] && {
    text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
    text="$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )"
    text="$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )"
    text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"
    text="$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )"

    } || {
    text=$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )
    text=$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )
    text=$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )
    text=$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )
    text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )
    }
  }
  cat << EOF
$text
EOF
}

get_data_mdv2(){
  text="$1"
  version_flag="$2"
  [[ -z "$2" ]] && version_flag="MarkdownV2"

  [[ "$3" == "raw" ]] && {
    text=$(conv_md "$text" $version_flag)
  }
  if [[ "$isreply" == "1" && "$msgid" == "0" ]]; then
#    if [[ $( echo "$msg_reply" | head -n1 | grep -c -P '^[A-Z] \?: [^$]' ) -eq 1 ]]; then
    if [[ $( echo "$msg_reply" | head -n1 | grep -c -P '^X \?: [^$]' ) -eq 1 ]]; then
      msg_reply="${msg_reply:5}"
    fi
    text="$( conv_md "$( echo "$msg_reply" | sed 's/^/> /' )" $version_flag )

$text"
  fi
  text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )
  text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )
  cat << EOF
{"chat_id": "$CID",
"text": "$text",
EOF
  if [[ "$isreply" == "1" && "$msgid" != "0" ]]; then
    msgid=$(conv_md "$msgid" $version_flag)
    msgid=$(echo "$msgid" | cut -d '\' --output-delimiter='\\' -f 1- )
    msgid=$(echo "$msgid" | cut -d '"' --output-delimiter='\"' -f 1- )
cat << EOF
"reply_to_message_id": "$msgid",
"allow_sending_without_reply": "true",
EOF
  fi
  cat << EOF
"parse_mode": "$version_flag",
"disable_web_page_preview": "true"}
EOF
}
get_data_md(){
  get_data_mdv2 "$1"
}

get_data_mdv1(){
  get_data_mdv2 "$1" "Markdown"
}

get_data_html(){
  get_data_mdv2 "$1" "HTML"
}


bu_get_msg_id(){
#  | jq -c --arg text "我" '.result[] | select(.message.text == $text)|.message.message_id'

local msgs=$(curl $PROXY https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?offset=-16)
local msg_id=$(echo "$msgs"  | jq -c --arg text "$1" '.result[] | select(.message.text == $text)|.message.message_id')
if [[ -n "$id" ]]; then
  echo $id
else
  return 1
fi

}




netstat -ntlp 2>/dev/null | grep "127.0.0.1:1080" &>/dev/null && PROXY="-x socks5h://127.0.0.1:1080"





get_data_old(){
text="$(echo "$*" | cut -d '\' --output-delimiter='\\' -f 1- )"
text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"

  cat << EOF
{
  "chat_id": "$CID",
"text": "$text",
  "disable_web_page_preview": "false"
}
EOF
}



TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN_LIQSLIU"

if [[ "$1" == "settoken" ]]; then
  if [[ "$2" == "wtfipfs" ]]; then
    TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN_WTFIPFS"
  else
    TELEGRAM_BOT_TOKEN="$2"
  fi
  shift
  shift
fi


    CID="113130580"
if [[ "$1" == "setcid" ]]; then
  if [[ "$2" == "vps_info" ]]; then
    CID="-520672657"
  elif [[ "$2" == "me" ]]; then
    CID="113130580"
  elif [[ "$2" == "wtfipfs" ]]; then
    CID="-1001193563578"
  elif [[ "$2" == "tw" ]]; then
    CID="-1001439521181"
  elif [[ "$2" == "rs" ]]; then
    CID="-1001137152439"
  else
    CID="$2"
  fi
  shift
  shift
fi


get_msgid(){
#  python3 "$SH_PATH//tg.py" "$1" "$2" "$CID" $TELEGRAM_API_ID $TELEGRAM_API_HASH
  python3 "$SH_PATH//get_msg.py" id "$1" "$2" "$CID"
}

isreply=0
msgid=0
msg_reply=""
if [[ "$1" == "--reply" && -n "$4" ]]; then
  isreply=1
  shift
  [[ "${2}" == "bot" ]] && msg_reply="$1" || msg_reply="T $2: $1"
  msgid=$(get_msgid "$1" "$2") || msgid=0
  [[ -z "$msgid" ]] && msgid=0
  shift
  shift
fi

#echo "$msgid"&&exit




if [[ "$1" == "getcid" ]]; then

  curl $PROXY https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates
  # curl $PROXY https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?offset=-1
#  curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getChat?chat_id=@wtfipfs"

elif [[ "$2" == "image_url" ]]; then
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data --markdown-mode "$*")" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &> /dev/null || exit 1
elif [[ "$2" == "send_photo" ]]; then
#  -d '{"chat_id": "'"$CID"'", "photo": "'"$1"'", "caption": "'"$3image"'"}' \
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d '
      {
        "chat_id": "'"$CID"'",
        "photo": "'"$*"'",
        "caption": "'"$3image"'",
        "disable_web_page_preview": '"false"'
      }' \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendPhoto &> /dev/null || exit 1

elif [[ "$1" == "--mdraw" ]]; then
  shift
#  echo "markdown: $(get_data_mdv2 "$*")"
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data_mdv2 "$*" MarkdownV2 raw)" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &> /dev/null || exit 1
elif [[ "$1" == "--md" ]]; then
  shift
#  echo "markdown: $(get_data_mdv2_orig "$*")"
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data_md "$*")" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &> /dev/null || exit 1
#  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &>> ~/tera/t.log || exit 1
#  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage
elif [[ "$1" == "--html" ]]; then
  shift
#  echo "markdown: $(get_data_mdv2 "$*")"
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data_html "$*")" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &> /dev/null || exit 1
else

  #curl -X POST \
#   -d '{"chat_id": "'"$CID"'", "text": "'"$*"'"}' \
#        "parse_mode": "'"MarkdownV2"'",
#	"text": "'"$(get_str "$*")"'",
#        "text": "'"$*"'",
#	\"text\": \"$(printf " %q" "${@}")\",
#	text="$(printf " %q" "${@}")"
  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data "$*")" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage &> /dev/null || exit 1


fi

