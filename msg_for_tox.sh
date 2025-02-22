#!/bin/bash

#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

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
    text=$(echo "$restmp" | jq -r ".text")
#    echo "$text" | sed '/^[^>]/,$d'
#    text=$(echo "$text" | sed '/^[^>]/,$!d')
    username=$(echo "$restmp" | jq -r ".username")

#    username="$(echo "$text" | head -n1 | cut -s -d ":" -f1 ): "
#    text=$(echo "$text" | cut -d" " -f3-)
#    text="${text:${#username}}"
    gateway=$(echo "$restmp" | jq -r ".gateway")
    if [[ "$gateway" == "gateway1" ]]; then
    # if true; then
      # if [[ "$username" != "O bot: " ]]; then
      if [[ "${username:0:2}" != "O " ]]; then
        if [[ "$gateway" != "gateway2" ]]; then
          URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
          if [[ -z "$URL" || "$URL" == "null" ]]; then
            if [[ -z "$text" ]]; then
              continue
            else
              #            [[ "$gateway" == "gateway1" ]] && echo -n "$(echo "$text" | sed "s/^/$username/g")"
              # [[ "$gateway" == "gateway1" ]] && echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
              # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
              echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
            fi
          else
            # if [[ "$gateway" == "gateway1" ]]; then
            if [[ -n "$gateway" ]]; then
              Comment=$(echo "$restmp" | jq -r ".Extra.file[0].Comment")
              if [[ -z "$Comment" ]]; then
  #              echo -n "$username$text$URL"
                # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")"
                echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")"
              else
                # text="$username$Comment: $URL"
                # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")"
                echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")"
              fi
            fi
          fi
        fi
      fi
    fi


            # if [[ "$gateway" == "gateway1" ]]; then
            # if [[ -n "$gateway" ]]; then
            #   gateway=gateway11
            # fi


    # continue # run cmd by python: mybots.py. but not running now
    # ########################################################


  fi

done
