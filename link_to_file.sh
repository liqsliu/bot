#!/bin/bash




export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
# [[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/mt.log" || export LOG_FILE=/dev/null



# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
# LP=${LP:-/var/www/dav/tmp}
LP=${LP:-$HOME/tera/tmp}
#DOMAIN=${DOMAIN:-liuu.tk}
export DOMAIN=${DOMAIN:-$(cat "$SH_PATH/DOMAIN")}
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-64000000}

MAX_TIMEOUT=16



# $2 type
# $3 12345
# [[ -n "$2" ]] && MAX_SHARE_FILE_SIZE="$2"

export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"

link_to_file() {
  local URL="$1"

  local my_url="$URL"
  local fn=${URL##*/}
  local fn fe ft fs my_url title
  fn=${fn##*:}
  fn=${fn##*\?}
  fn=${fn##*=}
  fn=${fn%%#*}
  fn=${fn#-}
  fn=${fn#-}
  fn=${fn#-}
  if [[ -z "$fn" ]]; then
    fn=$(date "+%Y%m%d_%H%M%S").html
    fe=html
    local fn_en=$fn
  else
    local fn_en=$fn
    fn=$(bash "$SH_PATH/"urldecode.sh "$fn")
    local fe=${fn##*\.}
  #  [[ "$fe" == "$fn" ]] && fe=""
    [[ "$fe" == "$fn" ]] && fe="" || fe=$(bash "$SH_PATH/"urldecode.sh "$fe")
  fi


  local flag=0
  local error=0
  cd $LP

  # local curl_res=$(curl -L -m 8 --max-filesize $MAX_SHARE_FILE_SIZE -s -o "$fn" -w '%{http_code}'  "$URL") || error=$?
    local curl_res=$(curl -L -m $MAX_TIMEOUT --max-filesize $MAX_SHARE_FILE_SIZE -s -o "$fn" -w '%{http_code}' -H "Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6" "$URL" -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' ) || error=$?
    # [[ "$curl_res" != "200" ]] && curl_res=$(curl -L -m 8 --max-filesize $MAX_SHARE_FILE_SIZE -s -o "$fn" -w '%{http_code}'  "$URL" -A 'Mozilla/5.0 (Linux; Android 11; KB2000) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.56 Mobile Safari/537.36' )
    [[ "$curl_res" != "200" ]] && {
      unset http_proxy
      unset https_proxy
      local curl_res=$(curl -L -m $MAX_TIMEOUT --max-filesize $MAX_SHARE_FILE_SIZE -s -o "$fn" -w '%{http_code}' -H "Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6" "$URL") || error=$?
    }

  if [[ "$curl_res" == "200" ]]; then
    if [[ -e "$fn" ]]; then
      spider_res="fake_Length: $(du -b -- "$fn" | cut -f1) [$(file --mime-type -b -- "${fn}")]"; flag=0; error=5; 
    else
      spider_res="fake_Length: 0 [text/html]"; flag=0; error=5; 
    fi
  else
    local spider_res="$spider_res
curl_exit: $error: $curl_res"
  fi

  # if [[ "$flag" -eq 512  ]]; then
  if [[ "$flag" -ne 0  ]]; then
    export http_proxy="http://127.0.0.1:6080"
    export https_proxy="http://127.0.0.1:6080"
  #  spider_res=$(wget -T 8 --spider "$URL" 2>&1 | grep Length) || ( error=$?; flag=512 )
    # spider_res=$(wget -T 8 --spider "$URL" 2>&1) || { error=$?; flag=512; } || local spider_res="$?: $spider_res"
    spider_res=$(wget -T $MAX_TIMEOUT --spider "$URL" 2>&1) || { error=$?; flag=512; }


  fi
  #spider_res="Length: 56161 (55K) [image/jpeg]"
  #  if [[ "$spider_res" == "" || $( echo "$URL" | wc -l ) -ne 1 ]] ; then
#  if [[ "$error" -ne 0 ]]; then
  if [[ "$error" -eq 512 ]]; then
    if [[ "$spider_res" == "" ]]; then
      flag=11
    fi
  else
    # echo testspider$spider_res
    spider_res=$( echo "$spider_res" | grep -P "Length|长度" | tail -n1 )
    # fs=$(echo "$spider_res" | awk '{ print $2}' | grep -o -P '\d+' | tail -n 1)
    fs=$(echo "$spider_res" | awk '{ print $2}' | grep -o -P '\d+' | head -n 1)
    local fsh=$(echo "$spider_res"| grep -o -P '\([^\)]+\)')
#    ft=$(echo "$spider_res" | awk '{ print $4}')
    ft=$(echo "$spider_res"| grep -o -P '\[[^\]]+\]')
    ft="${ft:1:-1}"
    
    [[ -z "$fs" ]] && fs=0
    if [[ $fs -ge $MAX_SHARE_FILE_SIZE ]]; then
      flag=1
    elif [[ "$fs" == "0" ]]; then
      flag=2
#    elif [[ "$ft" = *image/* || "$ft" = *video/* ]]; then
#    elif [[ "$ft" = *image/* || "$ft" = *video/* || "$ft" = *text/* ]]; then
#    elif [[ "$ft" != "[text/html]" ]]; then
    elif [[ 1 != 2 ]]; then
      if [[ "${URL:0:$((9 + ${#DOMAIN}))}" == "https://$DOMAIN/" && -e "$(bash "$SH_PATH/"urldecode.sh "${URL:$((9 + ${#DOMAIN}))}")" && "$(bash "$SH_PATH/"urldecode.sh "${URL:$((9 + ${#DOMAIN}))}")" = */* ]]; then
        # [[ -e "$(bash "$SH_PATH/"urldecode.sh "${URL:$((9 + ${#DOMAIN}))}")" ]] && cp "$(bash "$SH_PATH/"urldecode.sh "${URL:$((9 + ${#DOMAIN}))}")" "$fn"
        local sub_dir=$(bash "$SH_PATH/"urldecode.sh "${URL:$((9 + ${#DOMAIN}))}")
        sub_dir=${sub_dir%/*}
        [[ -n "$sub_dir" ]] && sub_dir="${sub_dir}/" && cd "${sub_dir}" && local sub_dir_en=$(bash "$SH_PATH/"urlencode.sh "${sub_dir}")
      fi
      

      if [[ -e "$fn" ]]; then
        if [[ "${URL:0:$((9 + ${#DOMAIN}))}" == "https://$DOMAIN/" || -n "$fe"  ]]; then
          my_url="https://$DOMAIN/${sub_dir_en}$fn_en"
        else
          [[ "$error" -eq 0 ]] && rm -f -- "$fn" # don't delete file downloaded by curl -o
        fi
      fi

      if [[ -e "$fn" ]]; then
        :
      else
        export http_proxy="http://127.0.0.1:6080"
        export https_proxy="http://127.0.0.1:6080"
        error_info=$( wget -T $MAX_TIMEOUT -q "$URL" -O "$fn" 2>&1 ) && my_url="https://$DOMAIN/${sub_dir_en}$fn_en" || { error=$?; flag=64; }
        if [[ "$(du -b -- "$fn" | cut -f1)" == "0" ]]; then
          echo "wget download error, empty file"
          [[ "$flag" -eq 0 ]] && flag=5
        fi
      fi
    else
      :
#      flag=4
    fi
  fi
  if [[ "$flag" == "0" ]]; then
    if [[ -z "$fe" ]]; then
      if [[ "$ft" == "text/html" ]]; then
        #fe=html
        #fe=$(file --extension "${fn}" | grep -o -P "\S+$")
        fe=$(file --extension -- "${fn}" | grep -o -P "[^\s/]+$")
        ft=$(file -bi -- "$fn"|cut -d';' -f1)
        [[ "$fe" == "???" ]] && fe=html && ft="text/html"
      else
        fe=$(file --extension -- "${fn}" | grep -o -P "[^\s/]+$")
      fi
      [[ -e "$fn" ]] && {
        mv "${fn}" "${fn}.${fe}"
        fn="${fn}.${fe}"
      }
      my_url="https://$DOMAIN/${sub_dir_en}${fn_en}.${fe}"
    fi
    if [[ "$2" == "type" ]]; then
      #if [[ "$ft" = *text/html* ]]; then
      if [[ "$ft" == "text/html" ]]; then
        if [[ $(echo "$URL" | grep -o '/' | wc -l) -le 2 ]]; then
          mv "${fn}" "${fn}.html"
          fn="${fn}.html"
          my_url="${my_url}.html"
        fi
        if [[ $( file -i -- "$fn"| grep -c "application/gzip" ) -eq 1 ]]; then
          title=$(cat -- "$fn" | gzip -d -c -)
        elif [[ $( file -i -- "$fn"| grep -c "text/html" ) -eq 1 ]]; then
          title=$(cat -- "$fn")
        else
          title="<title>E: unknown file type</title>"
        fi
        title=$(echo "$title" | grep -o -E "<title[^>]*>.*</title>")
        title=${title#*>}
        title=${title%%<*}
        echo "title: $title"
        [[ "$error" -ne 0 ]] && echo "remote: $fs $ft"
        echo "file info: $(du -b -- "$fn" | cut -f1)$fsh;$(file -i -- "${fn}"|cut -d":" -f2)"
        echo "tmp link: $my_url"
      else
        echo "file info: $(du -b -- "$fn" | cut -f1)$fsh;$(file -i -- "${fn}"|cut -d":" -f2)"
        [[ "$error" -ne 0 ]] && echo "remote: $fs $ft"
        echo "ipfs: $(bash "$SH_PATH/file_to_ipfs.sh" "$LP/${sub_dir}${fn}")"
        echo "tmp link: $my_url"
        
      fi
    else
      # if [[ "$ft" == "text/plain" ]] && [[ $fs -le 512000 ]]; then
      #   :
      # fi
      echo "$LP/${sub_dir}${fn}"
    fi
  elif [[ "$flag" == "64" ]]; then
    echo "wget error"
    echo "info: $error_info"
    return $error
  elif [[ "$flag" == "512" ]]; then
    echo "wget spider error"
    echo "spider_res: $spider_res"
    return $error

  elif [[ "$flag" == "1" ]]; then
    # echo "too big file: $fs > $MAX_SHARE_FILE_SIZE"
    echo "too big: $spider_res"
    [[ "$error" -ne 0 ]] && echo "remote: $fs $ft"
    return 1
  elif [[ "$flag" == "2" ]]; then
    echo "empty file: $spider_res"
    [[ "$error" -ne 0 ]] && echo "remote: $fs $ft"
    return 2
  elif [[ "$flag" == "4" ]]; then
    echo "not support $ft : $spider_res"
    [[ "$error" -ne 0 ]] && echo "remote: $fs $ft"
    return 4
  elif [[ "$flag" == "5" ]]; then
    return 5
  else
    :
    # bash ~/tg.sh "$2 $URL"
    # echo "$my_url"
    echo "unknown error(flag: $flag), @liqsliu"
    return $error
  fi
}

link_to_file "$@"
