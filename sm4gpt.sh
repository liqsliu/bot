#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

fn=${1-gpt_res}
text=$(cat "$SH_PATH/$fn") && rm "$SH_PATH/$fn"
gateway=${2-gateway1}
nohup bash "$SH_PATH/sm2.sh" "C bot" "$text" "4249" "$gateway" &> /dev/null &
