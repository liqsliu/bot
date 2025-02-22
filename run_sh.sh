#!/bin/bash

export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null

run_sh(){
  local res=${1}
  local ll=${2:-cmd.sh}
  local e=0
  rm "$SH_PATH/.ERROR"
  # echo bash "$SH_PATH/$ll" "$res" &>> $LOG_FILE
  bash "$SH_PATH/$ll" "$res" 1> "$SH_PATH/.STDOUT" 2> "$SH_PATH/.ERROR" || e=$?
  [[ -f "$SH_PATH/.ERROR" ]] && [[ -n "$(cat "$SH_PATH/.ERROR")" ]] && {
    bash "$SH_PATH/sm.sh" "C bot" "E: $?
$( cat "$SH_PATH/.STDOUT"
echo "---"
cat "$SH_PATH/.ERROR" )" 4240 &>> $LOG_FILE
  }
}

run_sh "$@"

