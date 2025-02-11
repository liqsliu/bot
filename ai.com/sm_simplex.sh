#!/bin/bash
#send msg of simplex to mt

export LOG_FILE=${LOG_FILE:-/dev/null}
export LOG=${LOG:-$HOME/mt.log}


send_msg_mt(){
# local username=$(echo "$1"|head -n1|cut -d':' -f1)
# local text=$(echo "$1"|sed '1s/^[^:]*://')
local username=$(echo "$1"|head -n1)
local text=$(echo "$1"|sed '1d')
bash "$SH_PATH/sm.sh" "$username" "$text" 4247 $gateway
}

# res=$(curl -m 3 -s 127.0.0.1:4250) || exit 1
# # echo "got from sx: $res" &>> $LOG_FILE
# if [[ "$res" == "[]" ]]; then
#   exit
# fi


res=$1
if [[ "$res" == "[]" ]]; then
  exit 0
fi
gateway=${2:-gateway1}

tmp=$res
while true
do
  if [[ -z "$tmp" ]]; then
    break
  else
    msg=$(echo "$tmp" | sed '/^_MSG_END_$/,$d')
    send_msg_mt "$msg" 2>> $LOG 1>> $LOG_FILE
  fi
  tmp=$(echo "$tmp" | sed '1,/^_MSG_END_$/d')
done
