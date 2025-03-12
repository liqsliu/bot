#!/bin/bash
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
export LOG_FILE=${LOG_FILE:-/dev/null}
export LOG=${LOG:-$HOME/mt.log}

MAX_BYTES=1371
split_msg(){
  local text=$1
  echo "$text"
  return

if [[ $(echo -n "$text" | wc -c) -gt $MAX_BYTES ]]; then
  tmp=$(echo "$TEXT" | head -n1)
  name_re=$(echo "$TEXT" | head -n1 | grep -o -P ".*?: " | head -n1 )
  TEXT=${TEXT:${#name_re}}
  echo -n "$name_re"; echo -n "${tmp::64} 💾"; echo "$TEXT" | curl -m 8 -s -F "c=@-" "https://fars.ee/?u=1"
else
  echo "$text"
fi
}


get_msg(){
  local username=$1
  local text=$2
  # local msg
  if [[ -z "$URL" || "$URL" == "null" ]]; then
    if [[ -z "$text" ]]; then
      return 1
      # continue
    else
      # bash "$SH_PATH/change_long_text.sh" "$username$text"
      split_msg "$username$text"
    fi
  else
    if [[ -n "$gateway" ]]; then
      Comment=$(echo "$restmp" | jq -r ".Extra.file[0].Comment")
      if [[ -z "$Comment" ]]; then
        # bash "$SH_PATH/change_long_text.sh" "$username$text $URL"
        split_msg "$username$text $URL"
      else
        # bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL"
        split_msg "$username$text$Comment: $URL"
      fi
    fi
  fi
  # echo "$msg"
}


parse_msg(){
  local restmp=$res
  echo "start to check restmp: $restmp" &>> $LOG_FILE
  TEXT=$(echo "$restmp" | jq -r ".text")
#    echo "$text" | sed '/^[^>]/,$d'
#    text=$(echo "$text" | sed '/^[^>]/,$!d')
  NAME=$(echo "$restmp" | jq -r ".username")
#    username="$(echo "$text" | head -n1 | cut -s -d ":" -f1 ): "
#    text=$(echo "$text" | cut -d" " -f3-)
#    text="${text:${#username}}"
  gateway=$(echo "$restmp" | jq -r ".gateway")
  username=$(echo "$NAME" | tail -n1)

  text=$TEXT
  [[ "${username:0:2}" != "C " ]] && [[ "${username: -5}" != "bot: " ]] && {
    QT=$(echo "$NAME" | sed -e '/^> [^>]/!d')
    qt=$(echo "$QT" | sed -e 's/^> //')
    if [[ -n "$qt" ]]; then
      text="$TEXT

$qt"
    else
      text="$TEXT"
    fi
  }
  if [[ "$gateway" == "gateway1" ]]; then
    URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
    get_msg "*${username% }* " "$text"
    # msg=$(get_msg "**${username% }** " "$text")
    # if [[ "$username" != "O bot: " ]]; then
    # if [[ "${username:0:2}" != "O " ]]; then
    # account=$(echo "$restmp" | jq -r ".account")
    # # if [[ "${username:0:2}" != "T " ]]; then
    # if [[ "${account}" != "api.tox" ]]; then
    #   # msg=$(get_msg "$username" "$text") || continue
    #   echo "send to tox: $msg" &>> $LOG_FILE
    #   echo "$msg"
    # fi
    # if [[ "${username:0:2}" != "Q " ]]; then
    #   bash "$SH_PATH/mqtt.sh" "$msg"
    # fi
  elif [[ "$gateway" == "test" ]]; then
    # echo 2 > "$SH_PATH/.BUSY"
    if [[ -e "$SH_PATH/.BUSY" ]]; then
      rm "$SH_PATH/.BUSY"
    fi
  fi
}

my_cmd(){
  export LOG="$HOME/mt.log"
  [[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE=$LOG || export LOG_FILE=/dev/null
  local e=0
  [[ -e "$SH_PATH/.ERROR" ]] && rm "$SH_PATH/.ERROR"
  local out=$("$@" 2> "$SH_PATH/.ERROR") || e=$?
  [[ -f "$SH_PATH/.ERROR" ]] && [[ -n "$(cat "$SH_PATH/.ERROR")" ]] && {
    echo "res=$res" &>> $LOG
    if [[ -e "$SH_PATH/DEBUG" ]]; then
      local d=$(bash -x "$@" 2>&1) || e=$?
      echo "d=$d" &>> $LOG
      bash "$SH_PATH/sm.sh" "C bot" "$(
      echo '#DEBUG'
      echo "$d"
      echo '#DEBUG'
      echo "---"
      echo "E: $e"
      )" 4240 test &>> $LOG_FILE
    else
      bash "$SH_PATH/sm.sh" "C bot" "E: $? $(
      cat "$SH_PATH/.ERROR"
      echo "---"
      echo "$out"
      )" 4240 &>> $LOG
    fi
  }
  if [[ -n "$out" ]]; then
    echo "$out"
  fi
}


ff="${SH_PATH}/.gm.sh.fifo"
mkfifo "$ff"
exec 6<>"$ff"
rm -f "$ff"

curl --buffer -N -s http://127.0.0.1:4241/api/stream 1>&6 2> "$SH_PATH/.ERROR" &

# while read -r line; do
# done < `curl -s curl http://localhost:4242/api/stream`
# done <<< `ping -c 9 localhost`
#
# https://stackoverflow.com/a/36368249
# curl --buffer -N -s http://127.0.0.1:4241/api/stream | while read -r res; do
while read -u6 -r res; do
if [[ -f "$SH_PATH/.ERROR" ]]; then
  err=$(cat "$SH_PATH/.ERROR")
  rm "$SH_PATH/.ERROR"
  [[ -n "$err" ]] && {
    bash "$SH_PATH/sm.sh" "C bot" "E:$(
    echo "$err"
    echo "---"
    echo "$out"
    )" 4240 &>> $LOG
  }
fi
# date
# echo "got: $res"
res=$(echo "$res" | jq 'del(.Extra.file[0].Data)') &>/dev/null || continue
my_cmd parse_msg
echo
echo
echo "EOF_FOR_TOX"
done

exec 6>&-


