#!/bin/bash
# https://api.muxiaoguo.cn/
#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}



# res=$(curl -s "https://api.muxiaoguo.cn/api/Tn_google?word=${*}&ta=${ta}&se=${se}")
# res=$(curl -s "https://api.muxiaoguo.cn/api/${FUNCNAME[0]}?word=${*}&ta=${ta}&se=${se}")

res=
get_res(){
  [[ -z "$1" ]] && res=$(curl "$@" -s "https://api.muxiaoguo.cn/api/${FUNCNAME[1]}") || res=$(curl -s "https://api.muxiaoguo.cn/api/${FUNCNAME[1]}?$1")
  # res=$(curl -s "https://api.muxiaoguo.cn/api/${FUNCNAME[1]}?$1")
  if [[ "$(echo "$res" | jq -r ".msg")" == "success" ]]; then
    return 0
  elif echo "$res" | jq -r ".msg" &>/dev/null; then
    echo "API: $(echo "$res" | jq -r ".msg")"
    return 1
  else
    echo "E: RES: $res"
    return 0
  fi
}


#https://api.muxiaoguo.cn/api/dujitang
dujitang(){
  if [[ "$1" == "help" ]]; then
    echo "毒鸡汤"
    echo ".dj"
  else
    get_res || return 1
    echo "$res" | jq -r ".data.comment"
  fi
}
Tn_google(){
  if [[ -z "$1" ]]; then
    echo "谷歌翻译"
    echo ".tr 你好"
  else
    if [[ "$1" == "-s" ]]; then
      shift
      local ta=$1
      shift
      local se=$1
      shift
      get_res "word=${*}&ta=${ta}&se=${se}" || return 1
    else
      get_res "word=${*}&se=en" || return 1
    fi
    echo "$res" | jq -r ".data.Translation"
  fi
}
tianqi(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "查询天气"
    echo ".tq 北京"
  else
    get_res "city=$(bash "$SH_PATH/urlencode.sh" "${*}")&type=1" || return 1
    echo "$(echo "$res" | jq -r ".data.cityname")天气: $(echo "$res" | jq -r ".data.weather") $(echo "$res" | jq -r ".data.temp")°C $(echo "$res" | jq -r ".data.SD") $(echo "$res" | jq -r ".data.WD") $(echo "$res" | jq -r ".data.WS") $(echo "$res" | jq -r ".data.wse") $(echo "$res" | jq -r ".data.time")"
  fi
}




#https://api.muxiaoguo.cn/api/QrcodeRT?url=https://api.muxiaoguo.cn/assets/img/qrcode.png
QrcodeRT(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "识别二维码"
    echo ".qrd \$URL"
  else
    if [[ "$1" == "post" ]]; then
      shift
      get_res "" -m 5 --compressed -F "file=@\"$(bash "$SH_PATH/link_to_file.sh" "$1")\"" || return 1
    else
      get_res "url=${1}" || return 1
    fi
    echo "$res" | jq -r ".data.content"
  fi
}





#https://github.com/qloog/lnmp100.github.io/blob/master/content/note/many-methods-to-generate-a-qr-code.md
#https://chart.googleapis.com/chart?cht=qr&chs=200x200&choe=UTF-8&chld=L%7C4&chl=http://www.lnmp100.com/

#https://api.muxiaoguo.cn/api/Qrcode?frame=1&e=L&text=木小果&size=200
# https://api.muxiaoguo.cn/api/Qrcode?frame=1&e=L&text=%E6%9C%A8%E5%B0%8F%E6%9E%9C&size=200
Qrcode(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "生成二维码"
    echo ".qr \$text"
  else
    local text=$(bash "$SH_PATH/urlencode.sh" "${*}")
    echo -n "https://api.muxiaoguo.cn/api/${FUNCNAME[0]}?"
    echo "frame=1&e=L&type=img&text=${text}&size=500"
    echo
    echo "https://chart.googleapis.com/chart?cht=qr&chs=200x200&choe=UTF-8&chld=L%7C4&chl=${text}"
  fi
}


fuckQrcode(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "生成二维码"
    echo ".qr \$text \$size \$e \$type \$frame"
  else
    local text=$(bash "$SH_PATH/urlencode.sh" "${1}")
    echo -n "https://api.muxiaoguo.cn/api/${FUNCNAME[0]}?"
    if [[ -z "$2" ]]; then
      echo "frame=1&e=L&text=${text}&size=200"
    else
      local size=${2-500}
      local e=${3-L}
      local type=${4-img}
      local frame=${5-1}
      echo "frame=${frame}&e=${e}&type=${type}&text=${text}&size=${size}"
    fi
  fi
}


#https://api.muxiaoguo.cn/api/chaojiping?url=api.muxiaoguo.cn
chaojiping(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "超级Ping"
    echo ".cjp \$domain"
  else
    local domain="$(echo "$1" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)"
    get_res "url=${domain}" || return 1
    i=0
    for (( ; ; i++)); do
      restmp=$(echo "$res" | jq ".data[$i]")
      if [[ "$restmp" == "null" ]]; then
        break
      fi
      echo "$restmp" | jq -r ".monitor_name" | xargs echo -n; echo -n " "
      
      echo "$restmp" | jq -r ".response_ip" | xargs echo -n; echo -n " "
      echo "$restmp" | jq -r ".ping" | xargs echo -n; echo -n " "
      echo "$restmp" | jq -r ".min" | xargs echo -n; echo -n " "
      echo "$restmp" | jq -r ".avg" | xargs echo -n; echo -n " "
      echo "$restmp" | jq -r ".max" | xargs echo -n;echo
    done


  fi
}




#https://api.muxiaoguo.cn/api/ICP?url=qq.com

ICP(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "ICP备案查询"
    echo ".icp \$domain"
  else
    local domain="$(echo "$1" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)"
    get_res "url=${domain}" || return 1
    echo "$res" | jq -r ".data.url" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.license" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.nature" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.organizer_name" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.website_home" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.website_name" | xargs echo -n; echo -n " "
    echo "$res" | jq -r ".data.audit_time" | xargs echo -n; echo

  fi
}





# 模板
#https://api.muxiaoguo.cn/api/hybrid?word=xswl
# hybrid(){
#   if [[ -z "$1" ]]; then
#     echo "网络词字典"
#     echo ".wtf \$缩写"
#   else
#     get_res "?word=$1" || return 1
#     echo "$res" | jq -r ".data.content"
#   fi
# }



#https://api.muxiaoguo.cn/api/hybrid?word=xswl
hybrid(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "网络词字典"
    echo ".wtf \$缩写"
  else
    # get_res "word=$(bash "$SH_PATH/urlencode.sh" "${*}")" || return 1
    # get_res "word=${*}" || return 1
    # local name=$(echo "$res" | jq -r ".data[0].name")
    # local desc=$(echo "$res" | jq -r ".data[0].desc")
    # local imgurl=$(echo "$res" | jq -r ".data[0].imgurl")
    # if [[ "$desc" != "null" ]]; then
    #   echo "${name}: $desc"
    #   [[ "$imgurl" != "null" ]] && echo "img: $imgurl"
    # else
    #   echo "E: $res"
    # fi
    local text="${*}"
    local i
    local api_error=1
    get_res "word=${*}" && {
      for (( i=0 ; i<64 ; i++   ))
      do
        local data=$(echo "$res" | jq -r ".data[$i]")
        [[ "$data" == "null" ]] && break
        local name=$(echo "$data" | jq -r ".name")
        local desc=$(echo "$data" | jq -r ".desc")
        local imgurl=$(echo "$data" | jq -r ".imgurl")
        if [[ "${text,,}" == "${name,,}" ]]; then
          api_error=0
          echo "${name}: $desc"
          [[ "$imgurl" != "null" ]] && echo "img: $imgurl"
        fi
      done
      
      [[ "$api_error" == 1 ]] && echo "没找到"
      for (( i=0 ; i<64 ; i++   ))
      do
        local data=$(echo "$res" | jq -r ".data[$i]")
        [[ "$data" == "null" ]] && break
        [[ "$i" == "0" ]] && echo -ne "\n可能相关的词:"
        echo -n " $(echo "$data" | jq -r ".name")"
      done
      echo
    } || api_error=1
    local hhsh=$(bash "$SH_PATH/nbnhhsh.sh" "$text" || echo "E: $?")
    [[ "$hhsh" != "${text,,}:" && "$hhsh" != "null:" ]] && echo && echo "能不能好好说话: $hhsh" || {
      [[ "$api_error" == 1 ]] && {
        echo
        echo "google: 意思 $text"
        bash "$SH_PATH/google.sh" -n 5 "意思" "$text" || echo "E: $?"
      }
    }
  fi
}

#https://api.muxiaoguo.cn/api/xiaohua
xiaohua(){
  if [[ "$1" == "help" ]]; then
    echo "随机笑话"
  else
    get_res || return 1
    echo "$res" | jq -r ".data.title"
    #https://stackoverflow.com/a/43058947
    # echo "$res" | jq -r ".data.content" | sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/\</g; s/&gt;/\>/g; s/&quot;/\"/g; s/#&#39;/\'"'"'/g; s/&ldquo;/\"/g; s/&rdquo;/\"/g;'
    local LineOut=$(echo "$res" | jq -r ".data.content")
    LineOut="${LineOut//&ldquo;/'"'}" # TODO: ASCII/ISO for opening quote
    LineOut="${LineOut//&rdquo;/'"'}" # TODO: ASCII/ISO for closing quote
    echo "$LineOut"
  fi
}

#https://api.muxiaoguo.cn/api/yiyan
yiyan(){
  if [[ "$1" == "help" ]]; then
    echo "一言"
  else
    get_res || return 1
    echo "$res" | jq -r ".data.constant"
    echo -n "--" && echo "$res" | jq -r ".data.source"
  fi
}


#https://api.muxiaoguo.cn/api/163reping
163reping(){
#  if [[ -z "$1" || "$1" == "help" ]]; then
  if [[ "$1" == "help" ]]; then
    echo "网易云热评"
  else
    get_res || return 1
    echo -n "$(echo "$res" | jq -r ".data.nickname")"
    echo -n ": "
    echo "$res" | jq -r ".data.content"
    echo -n "song: " && echo -n $(echo "$res" | jq -r ".data.songAutho") && echo -n "-" && echo -n $(echo "$res" | jq -r ".data.songName") && echo -n ' ' && echo -n $(echo "$res" | jq -r ".data.songId") && echo -n ' ' && echo "$res" | jq -r ".data.songPic"
  fi
}
#https://api.muxiaoguo.cn/api/163music?id=3716423
163music(){
  if [[ -z "$1" || "$1" == "help" ]]; then
    echo "网易云音乐解析"
    echo ".wy \$id"
  else
    get_res "id=$1" || return 1
    echo -n "曲名: " && echo "$res" | jq -r ".data.songName"
    echo -n "作者: " && echo "$res" | jq -r ".data.songArtists"
    echo -n "封面: " && echo "$res" | jq -r ".data.songPic"
    echo -n "id: " && echo "$res" | jq -r ".data.songId"
    echo -n "专辑: " && echo "$res" | jq -r ".data.albumName"
    echo -n "封面: " && echo "$res" | jq -r ".data.albumPicurl"
    echo -n "直链: " && echo "$res" | jq -r ".data.mp3url"
  fi
}

#https://api.muxiaoguo.cn/api/tiangourj
tiangourj(){
  if [[ "$1" == "help" ]]; then
    echo "舔狗日记"
  else
    get_res || return 1
    echo "$res" | jq -r ".data.comment"
  fi
}




api_name=$1
shift
$api_name "$@"
