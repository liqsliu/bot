#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
# DOMAIN=${DOMAIN:-liuu.tk}
DOMAIN=$(cat DOMAIN)
LP=${LP:-/var/www/dav/tmp}
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-15000000}





run_trans() {

#trans -brief "${@}"
trans "${@}"

}


help(){
  echo "翻译
默认: 非中文翻译为中文，中文则翻译为英文
详情: https://github.com/soimort/translate-shell"
}


[[ -z "$1" || "$1" == "help" ]] && help && exit 0


#-identify

#sl="-s auto"
# tl="-t en"
tl=""

#is_dic="-brief -j"
opts="-brief -j"
#file_path=$(date "+%Y%m%d_%H%M%S").ts
file_path="$LP/$(date "+%Y%m%d_%H%M%S").mp3"

#src_lang=$(trans -id -j "${@}" | awk '/Code/{print $2}')
[[ "$is_id" -ne 1 ]] && src_lang=$(trans -brief -id -j "${@}" 2>/dev/null)
#echo $src_lang

if [[ "$src_lang" == "zh-CN" ]]; then
  tl="-t en"
elif [[ "$src_lang" == "zh-TW" ]]; then
  tl="-t en"
else
  tl="-t zh-CN"
fi

run_trans $tl $opts "${*}"

