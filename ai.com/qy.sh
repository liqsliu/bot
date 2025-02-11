#!/bin/bash


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd -P )}


export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"



_(){
  # curl -m 19 -s "http://api.qingyunke.com/api.php?key=free&appid=0&msg=$(bash "$SH_PATH/urlencode.sh" "$*")" || exit $?
  local res=$(curl -m 19 -s "http://api.qingyunke.com/api.php?key=free&appid=0&msg=$(bash "$SH_PATH/urlencode.sh" "$*")") && {

    local result=$(echo "$res"|jq -r ".result")
    if [[ "$result" = 0 ]]; then
      local content=$(echo "$res"|jq -r ".content")
      echo "$content"
    else
      echo "$res"
    fi

    return
    true
  } || exit $?
  echo
}


if [[ -z "$2" ]]; then
  echo "$1"
  echo "$1 help"
  echo "$1 \$str"
  echo '---'
  echo '菲菲内置多种功能，通过发送命令可执行特殊操作
★★ 示例 ★★
　查询天气预报信息，示例：天气 深圳
手机、ＩＰ地址归属，示例：归属 手机或IP
　　　邮政编码及地区查询：邮编 514000
　　计算简单的算术，示例：计算 15+13
　　　查询成语介绍，示例：成语 一心一意
按歌曲名称查询歌词，示例：歌词 歌曲名称
　　中译英、英译中，示例：翻译 i love you
　查询星座今日运势，示例：星座 天秤座
　查询星座介绍请直接发送：天秤座
汉字五笔拼音笔画查询示例：礡字
　　想看笑话，请直接发送：笑话'
  echo '---'
  echo '---'
  echo 'qingyunke.com'
# elif [[ "$2" == "on" ]]; then
#   :
else
  shift
  # ai "$@"
  _ "$*" | sed 's/{br}/\n/g'
fi

