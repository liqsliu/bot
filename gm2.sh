#!/bin/bash
#get msg for tox and run cmd
#export SH_PATH=/run/user/1000/bot
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

run_sh(){
export LOG="$HOME/mt.log"
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE=$LOG || export LOG_FILE=/dev/null
  local e=0
  rm "$SH_PATH/.ERROR"
  # echo bash "$SH_PATH/$ll" "$res" &>> $LOG_FILE
  # bash "$SH_PATH/$ll" "$res" 1> "$SH_PATH/.STDOUT" 2> "$SH_PATH/.ERROR" || e=$?
  local out=$(bash "$SH_PATH/$ll" "$res" 2> "$SH_PATH/.ERROR") || e=$?
  [[ -f "$SH_PATH/.ERROR" ]] && [[ -n "$(cat "$SH_PATH/.ERROR")" ]] && {
    echo "res=$res" &>> $LOG
    if [[ -e "$SH_PATH/DEBUG" ]]; then
      local d=$(bash -x "$SH_PATH/$ll" "$res"  2>&1) || e=$?
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



res=$1
ll=cmd.sh
run_sh
