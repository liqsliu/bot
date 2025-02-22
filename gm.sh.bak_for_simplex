#!/bin/bash
#get msg for tox and run cmd
#export SH_PATH=/run/user/1000/bot
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}


run_sh(){
# [[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
export LOG="$HOME/mt.log"
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE=$LOG || export LOG_FILE=/dev/null
  # local res=${1}
  # local ll=${2:-cmd.sh}
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
    bash "$SH_PATH/sm.sh" "C bot" "E: $?
$(
cat "$SH_PATH/.ERROR"
echo "---"
echo "$out"
)" 4240 &>> $LOG
fi
  }
  if [[ "$ll" == cmd.sh ]]; then
    if [[ -n "$out" ]]; then
      echo "$out"
      busy=1
    fi
  fi
}
# get msg from simplex
# res=$(curl -m 2 -s http://127.0.0.1:4250) || exit 0
# if [[ "$res" != "[]" ]]; then
#   # bash "$SH_PATH/run_sh.sh" "$res" sm_simplex.sh
#   ll=sm_simplex.sh
#   run_sh
#   busy=1
# fi


#res="[]"
# for cmd
res=$(curl -m 2 -s http://127.0.0.1:4240/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
  ll=cmd.sh
  run_sh
fi


min=2

if [[ "$busy" == "1" ]]; then
  busy=$min
elif ! [[ -e "$SH_PATH/.BUSY" ]]; then
  busy=$min
else
max=50 #3s
max2=150
  busy=$(cat "$SH_PATH/.BUSY")
  # busy=$[busy*2]
  if [[ $busy -ge $max2 ]]; then
    sleep 3
  elif [[ $busy -ge $max ]]; then
    busy=$[busy+1]
    busy2=$[(busy-max)*(busy-max)*(busy-max)/35714]
    sleep 0.2
    # echo sleep2 $[busy2/10].$[busy2%10] 1>&2
    sleep $[busy2/10].$[busy2%10]
  else
    busy=$[busy+1]
    sleep 0.2
  fi
  # echo $busy 1>&2
  # sleep $[busy/10].$[busy%10]
fi
echo $busy > "$SH_PATH/.BUSY"
# nohup bash "$SH_PATH/bgm.sh" &>/dev/null &
