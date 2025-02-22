#!/bin/bash



get_data(){
  cat << EOF
{"chat_id": "$CID",
"sender_chat_id": "$CHAT"}
EOF

}
PRIVATE_KEYS_PATH="${HOME}/.ssh/private_keys.txt"
#liqsliu_bot
TELEGRAM_BOT_TOKEN_LIQSLIU=$(grep TELEGRAM_BOT_TOKEN_LIQSLIU "$PRIVATE_KEYS_PATH")
TELEGRAM_BOT_TOKEN_LIQSLIU=${TELEGRAM_BOT_TOKEN_LIQSLIU#* }

  TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN_LIQSLIU
  CID="$2"
  CHAT="$3"

  curl $PROXY -X POST -H 'Content-Type: application/json' \
    -d "$(get_data "$*")" \
  https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/banChatSenderChat



