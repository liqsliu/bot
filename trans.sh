#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
DOMAIN=${SH_PATH:-$(cat "$SH_PATH/DOMAIN"))}
LP=${LP:-${HOME}/tera/tmp}
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-15000000}





run_trans() {

#trans -brief "${@}"
trans "${@}"

}


help(){
  echo "翻译
默认: 非中文翻译为中文，中文则翻译为英文
用法: .trans [-brief] [-s zh] [-t en] [zh:en] \$text
自定义参数： .trans -j ...
帮助： .trans -h
翻译引擎: 列出(-S)，指定(-e)
详情: https://github.com/soimort/translate-shell"
}


[[ -z "$1" || "$1" == "help" ]] && help && exit 0


#-identify

#sl="-s auto"
# tl="-t en"
tl=""

#is_dic="-brief -j"
# opts="-brief -j"
opts="-j"
#file_path=$(date "+%Y%m%d_%H%M%S").ts
file_path="$LP/$(date "+%Y%m%d_%H%M%S").mp3"

for i in "$@";do
  if [[ "$i" == "-j" ]]; then
    opts=""
  elif [[ "$i" == "-d" ]]; then
    opts=""
  elif [[ "$i" == "-brief" ]]; then
    opts=""
  elif [[ "$i" == "-id" ]]; then
    # opts="-j"
    is_id=1
  fi
done
for i in "$@";do
  if [[ "$i" == "-t" ]]; then
    tl="1"
  elif [[ "$i" == "-sp" ]]; then
    tl="1"
    is_play=1
    opts="$opts -download-audio-as $file_path"
  elif [[ "$i" == "-p" ]]; then
    is_play=1
    opts="$opts -download-audio-as $file_path"
  elif echo "$i" | grep -P ":[a-z]{2,3}(-[A-Z]{2})?$" &>/dev/null; then
    tl="1"
  elif [[ "$i" == "-e" ]]; then
    opts="-j"
  fi
done

#src_lang=$(trans -id -j "${@}" | awk '/Code/{print $2}')
[[ "$is_id" -ne 1 ]] && src_lang=$(trans -brief -id -j "${@}")
#echo $src_lang

#if [[ -z "$sl" && -z "tl" ]]; then
if [[ -z "$tl" ]] && [[ -n "$opts" ]]; then
  if [[ "$src_lang" == "zh-CN" ]]; then
    tl="-t en"
  elif [[ "$src_lang" == "zh-TW" ]]; then
    tl="-t en"
  else
    tl="-t zh-CN"
  fi
else
  tl=""
fi



#echo run_trans $opts $tl  "${@}"
run_trans $tl $opts "${@}"

#[[ "$is_play" -eq 1 ]] && bash "$SH_PATH/"file_to_ipfs.sh "$file_path"
[[ "$is_play" -eq 1 ]] && echo "https://$DOMAIN/${file_path##*/}" || true

