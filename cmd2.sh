#!/bin/bash
#background cmd

export LOG_FILE=${LOG_FILE:-/dev/null}
export LOG=${LOG:-$HOME/mt.log}

export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
# export DOMAIN=$(cat "$SH_PATH/DOMAIN")
export DOMAIN=${DOMAIN:-$(cat "$SH_PATH/DOMAIN")}

[[ -z "$3" ]] && exit 0
gateway=$1
username=$2
text=$3

send(){
  local text=$1
  # curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "$1" $gateway)" http://127.0.0.1:4240/api/message
  # bash "$SH_PATH/sm.sh" "C bot" "$text" 4240 $gateway
  bash "$SH_PATH/sm.sh" "C bot" "$text" 4249 $gateway
}

log2(){
  r=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
  if [[ "$e" -ne 0 ]]; then
  echo "E: $e" >> $LOG
  fi
  echo "fail to run cmd
text=$text
error=$r
out=$out
" >> $LOG
}

log0(){
  set -x
  # cmds $text 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  bash "$SH_PATH/bcmd.sh" "$@" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  out=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
  log2
}

# out=$(cmds $text 2>"$SH_PATH/error") && e=$? || {
# bash "$SH_PATH/bcmd.sh" "$@" 2>> $LOG 1>> $LOG_FILE
out=$(bash "$SH_PATH/bcmd.sh" "$@" 2>"$SH_PATH/error") && e=$? || {
  e=$?
  [[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
    log0 "$@"
    # push_err "E: failed to run cmd: $text|$e|$r"
  } || {
    log2
  }
  text=$3
  send "E: failed to run cmd: $text|$e|$r|$out" 2>> $LOG 1>> $LOG_FILE
  exit
}

if [[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]]; then
  if [[ -e "$SH_PATH/DEBUG" ]]; then
    log0 "$@"
  else
    log2
  fi
fi

text=$out

if [[ -n "$r" ]]; then
  text="$text
--
E: $r"
#   [[ -z "$text" ]] && exit 0
fi
if [[ -z "$text" ]]; then
  exit 0
  text=None
fi
# text=$(echo "$text"|sed 's/\r//g')
# text=$(echo "$text" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
echo "b1 :|$text|" >> $LOG_FILE
  # [[ -z "$text" ]] && exit
  # text=$(bash "$SH_PATH/gene_res.sh" "$text" $gateway)
#  res=$(curl -s -XPOST -H 'Content-Type: application/json' -d "$text" http://127.0.0.1:4243/api/message)
# bash "$SH_PATH/sm.sh" bot "$text" 4240 $gateway || echo "E: $?"
send "$text" 2>> $LOG 1>> $LOG_FILE
