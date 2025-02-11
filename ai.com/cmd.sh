#!/bin/bash


export LOG_FILE=${LOG_FILE:-/dev/null}
export LOG=${LOG:-$HOME/mt.log}

# echo cmd start >> ~/tera/mt_msg.log
#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname "${BASH_SOURCE[0]}") || exit; pwd )}


get_msg(){
  local username=$1
  local text=$2
  # local msg
  if [[ -z "$URL" || "$URL" == "null" ]]; then
    if [[ -z "$text" ]]; then
      return 1
      # continue
    else
      bash "$SH_PATH/change_long_text.sh" "$username$text"
    fi
  else
    if [[ -n "$gateway" ]]; then
      Comment=$(echo "$restmp" | jq -r ".Extra.file[0].Comment")
      if [[ -z "$Comment" ]]; then
        bash "$SH_PATH/change_long_text.sh" "$username$text $URL"
      else
        bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL"
      fi
    fi
  fi
  # echo "$msg"
}







send_msg_to_simplex(){
# [[ -e "$SH_PATH/DEBUG" ]] && set -x
# [[ -e "$SH_PATH/DEBUG" ]] && set +x
# get msg from simplex to mt
# curl -m 300 -s -XPOST -d "msg from mt" 127.0.0.1:4250
# res=$(curl -m 1 -s 127.0.0.1:4250) || exit 0
 # &>> $LOG_FILE
# local res=$(curl -m 2 -s -XPOST -d "$*"  127.0.0.1:4250) || return 1

local NAME=$username
# local QT=qt
local TEXT=$text

    if [[ "$NAME" == "M rssbot: " ]] || [[ "$NAME" == "M feeds: " ]]; then
      NAME=${TEXT%%:*}
      TEXT=${TEXT#*: }
    else


      NAME="*${NAME% }* "
      # if [[ -n "$QT" ]]; then
        # QT=$(echo "$QT" | sed '/^[^>]/d'; echo )
#         NAME="$QT
# ${NAME}"
      # fi
    fi
  local msg=$(get_msg "$NAME" "$TEXT") || return
echo "send to sx: $msg" &>> $LOG
local res=$(curl -m 5 -s -XPOST -d "$msg"  127.0.0.1:4250) || return 1
echo "got from sx: $res" &>> $LOG_FILE
bash "$SH_PATH/sm_simplex.sh" "$res" 2>> $LOG 1>> $LOG_FILE
echo "send to sx end" &>> $LOG
}



bcmd(){
  local text=$1
  local username=$2
  [[ -z "${username}" ]] && return 0
  local gateway=$3
  local restmp=$4



  # local account=$(echo "$restmp" | jq -r ".account")

  # [[ "$username" == "C bot: " ]] && continue
  # [[ "$username" == "C xmppbot: " ]] && continue
  # [[ "$username" == "C titlebot: " ]] && continue
  # [[ "$username" == "C twitter: " ]] && continue
  # [[ $(echo "$text" | wc -l) -ne 1 ]] && continue
# qt_text=$(echo "$username" | sed '/^> /!d' | sed 's/^> //')
# [[ -n "$qt_text" ]] && qt_text="
# $qt_text"
  # username=$(echo "$username" | tail -n1 )

  # if [[ "$gateway" != "gateway2" && $(echo "$text" | wc -l) -eq 1 ]]; then
  # if [[ $(echo "$text" | wc -l) -eq 1 ]]; then
  #   # if [[ "$gateway" == "gateway1" ]]; then
  #   #   gateway=gateway11
  #   # fi
  #   if [[ "$text" == "ping" ]]; then
  #     text=".ping"
  #   # elif [[ -z "${username}" ]]; then
  #   #   # continue
  #   #   return 0
  #   # elif [[ "$text" == "help" ]]; then
  #   #   # text=".help"
  #   #   nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" ".help" "$restmp" &>/dev/null &
  #   #   sleep 3
  #   # elif [[ $(echo "$text" | grep -c -P "^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$") -eq 1 ]]; then
  #   #   :
  #     # text=".tw $text" # not work because of fordiben by twitter
  #   # elif [[ $(echo "$text" | grep -c -P "^https://wtfipfs\.eu\.org/[a-zA-Z0-9_./?=%-]+$") -eq 1 ]]; then
  #   #   text=".ipfs $text only"
  #   # elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(jpe?g|png|mp4|gif|txt)$") -eq 1 ]]; then
  #   #   text=".ipfs $text only"
  #   # elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*$") -eq 1 ]]; then
  #   #   text=".type $text autocheck"
  #   fi
  # # else
  # #   # [[ -z "${username}" ]] && continue
  # #   [[ -z "${username}" ]] && return 0
  # fi
  # nohup bash "$SH_PATH/cmd2.sh" "$gateway" "$username" "$text" "$restmp" "$qt" 2>> $LOG 1>> $LOG_FILE &
  nohup bash "$SH_PATH/cmd2.sh" "$gateway" "$username" "$text" "$restmp" 2>> $LOG 1>> $LOG_FILE &
}





#[[ "$(echo "$res" | jq ".[0]")" != "null" ]] && bash "$SH_PATH/cmd.sh" "$res"
#
# echo "cmd > arg: $*" >> /tmp/cmd.log

res=$1
i=0
for (( ; i < 4; i++)); do
  restmp=$(echo "$res" | jq ".[$i]")
  if [[ "$restmp" == "null" ]]; then
    break
  else
echo "start to check restmp: $restmp" &>> $LOG_FILE
    TEXT=$(echo "$restmp" | jq -r ".text")
#    echo "$text" | sed '/^[^>]/,$d'
#    text=$(echo "$text" | sed '/^[^>]/,$!d')
    NAME=$(echo "$restmp" | jq -r ".username")

#    username="$(echo "$text" | head -n1 | cut -s -d ":" -f1 ): "
#    text=$(echo "$text" | cut -d" " -f3-)
#    text="${text:${#username}}"
    gateway=$(echo "$restmp" | jq -r ".gateway")
  # continue # run cmd by python: mybots.py. but not running now
  # ########################################################

    username=$(echo "$NAME" | tail -n1)

    [[ "${username:0:2}" != "C " ]] && [[ "${username: -5}" != "bot: " ]] && {
    QT=$(echo "$NAME" | sed -e '/^> [^>]/!d')
    qt=$(echo "$QT" | sed -e 's/^> //')
    if [[ -n "$qt" ]]; then
      text="$TEXT

$qt"
    else
      text="$TEXT"
    fi
      # bcmd "$text" "$username" "$gateway" "$restmp"
      nohup bash "$SH_PATH/cmd2.sh" "$gateway" "$username" "$text" "$restmp" 2>> $LOG 1>> $LOG_FILE &
    }

    # continue


    if [[ "$gateway" == "gateway1" ]]; then
      URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
      # if [[ "${username:0:2}" != "S " ]]; then
      #   # bash "$SH_PATH/run_sh.sh" "[$restmp]" msg_for_simplex.sh
      #   # send_msg_to_simplex "$username$text"
      #   # send_msg_to_simplex "$msg" 2>> $LOG 1>> $LOG_FILE
      #   send_msg_to_simplex 2>> $LOG 1>> $LOG_FILE
      # fi
      msg=$(get_msg "$username" "$text") || continue
      # if [[ "$username" != "O bot: " ]]; then
      # if [[ "${username:0:2}" != "O " ]]; then
      if [[ "${username:0:2}" != "T " ]]; then
        # msg=$(get_msg "$username" "$text") || continue
        echo "send to tox: $msg" &>> $LOG_FILE
        echo "$msg"
      fi
      # if [[ "${username:0:2}" != "Q " ]]; then
      #   bash "$SH_PATH/mqtt.sh" "$msg"
      # fi
    elif [[ "$gateway" == "test" ]]; then
      # echo 2 > "$SH_PATH/.BUSY"
      if [[ -e "$SH_PATH/.BUSY" ]]; then
        rm "$SH_PATH/.BUSY"
      fi
    fi

  fi

done
# [[ -e "$SH_PATH/DEBUG" ]] && set -x

# [[ -e "$SH_PATH/DEBUG" ]] && set +x






