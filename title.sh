#!/bin/bash
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null

export DOMAIN=${DOMAIN:-$(cat "$SH_PATH/DOMAIN")}
LP=${LP:-$HOME/tera/tmp}

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
# UA="curl/7.88.1"
LA='Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'



# https://stackoverflow.com/questions/20317945/limit-size-wget-can-download/20318140#20318140

# if [[ "$4" == "down" ]]; then
if [[ -n "$4" ]]; then
  # 暂时忽略自定义大小
ulimit -f 2048000
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-1000000000}
# MAX_TIMEOUT=300
MAX_TIMEOUT=$4

else
ulimit -f 204800
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-10000000}
MAX_TIMEOUT=16


fi

# https://stackoverflow.com/questions/55842311/get-page-titles-from-a-list-of-urls
# while read -r URL; do
    # echo -n "$URL --> "
URL=$1
# fn=${URL##*/}
# fn=${fn##*:}
# fn=${fn##*\?}
# fn=${fn##*=}
# fn=${fn%%#*}
# # fn=${fn#-}
# # fn=${fn#-}
# # fn=${fn#-}
# fn=$(echo "$fn" | sed "s/^-*//g")
# if [[ -z "$fn" ]]; then
#   # fn=$(date "+%Y%m%d_%H%M%S")
#   # fn=$(date "+%H%M%S")
#   fn=tmp
# elif [[ "${fn}" == "index.html" ]]; then
#   fn=tmp
# elif [[ "${fn}" == "index" ]]; then
#   fn=tmp
# fi
# fno=$fn
fno=tmp
fn="$HOME/t/$fno"
cd "$HOME/t/" || {
# rm * &>/dev/null || true
  echo "目录有问题"
  exit 1
}
# echo "$fn"

[[ -e "$fn" ]] && rm -f "$fn"


if [[ "$3" == direct ]]; then
  unset http_proxy
  unset https_proxy
  # wget -T $MAX_TIMEOUT -q -O "$fn" "$URL" || {
  # wget --server-response -T $MAX_TIMEOUT -O "$fn" "$URL" || exit $?
  # wget -T $MAX_TIMEOUT -O "$fn" "$URL" || exit $?
  # }
else
  export http_proxy="http://127.0.0.1:6080"
  export https_proxy="http://127.0.0.1:6080"
fi

if [[ "$2" == curl ]]; then
  # curl -s -L -m $MAX_TIMEOUT --max-filesize $MAX_SHARE_FILE_SIZE -o "$fn" -H "$LA" "$URL" -A "$UA" || {
  # curl -v -L -m $MAX_TIMEOUT --max-filesize $MAX_SHARE_FILE_SIZE -o "$fn" -H "$LA" "$URL" -A "$UA"
  curl -v -L -m $MAX_TIMEOUT --max-filesize $MAX_SHARE_FILE_SIZE -o "$fno" -H "$LA" "$URL" -A "$UA" 
  sc=$?
  # }

elif [[ "$2" == raw ]]; then
  # wget -T $MAX_TIMEOUT -q -O "$fn" "$URL" || {
  # wget --server-response -T $MAX_TIMEOUT -O "$fn" "$URL" || exit $?
  # wget -T $MAX_TIMEOUT -O "$fn" "$URL"
  wget -T $MAX_TIMEOUT -O "$fno" "$URL"
  sc=$?
  # }
else
  # wget --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -q -O "$fn" "$URL" || {
  # wget --server-response --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -O "$fn" "$URL" || exit $?
  # wget --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -O "$fn" "$URL"
  # wget --content-on-error --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -O "$fn" "$URL"
  wget --content-on-error --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -O "$fno" "$URL"
  # wget -O "$fn" "$URL"
  sc=$?
  # }
fi

[[ -e "$fn" ]]  || {
  echo "not found file"
  exit $sc
}

ft=$(file --mime-type -b -- "$fn")  || {
  echo "can not open file"
  exit $?
}

  # echo "$html" > "$fn"
  # fes=$(file --extension -b -- "$fn" | grep -o -P "[^\s/]+")
  # unset fe
  # if [[ -z "$fes" ]]; then
  #   :
  #   # fe=bin
  # else
  #   for i in $fes; do
  #     if [[ "${fno%.${i}}" == "$fno" ]]; then
  #       if [[ -z "$fe" ]]; then
  #         fe=".$i"
  #       fi
  #     else
  #       fno=${fno%.${i}}
  #       fe=".$i"
  #       break
  #     fi
  #   done
  # fi
  # grep -i "$mime_type" /etc/mime.types | awk '{for(i=2;i<=NF;i++) print $i}'
mime_type=$ft
# 定义 MIME 类型到扩展名的映射
case "$mime_type" in
  "image/jpeg")
    ext="jpg"
    ;;
  "image/png")
    ext="png"
    ;;
  "image/gif")
    ext="gif"
    ;;
  "image/webp")
    ext="webp"
    ;;
  "text/plain")
    ext="txt"
    ;;
  "text/html")
    ext="html"
    ;;
  "application/pdf")
    ext="pdf"
    ;;
  "application/zip")
    ext="zip"
    ;;
  "application/msword")
    ext="doc"
    ;;
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    ext="docx"
    ;;
  "audio/mpeg")
    ext="mp3"
    ;;
  "video/mp4")
    ext="mp4"
    ;;
  *)
    # echo "未知 MIME 类型: $mime_type"
    # exit 1
    ext=""
    ;;
esac

unset fe
# if [[ -n "$ext" ]]; then
#   fe=".$ext"
#   if [[ "${fno%.${ext}}" == "$fno" ]]; then
#     mv "$fn" "$HOME/t/$fno$fe"
#     fn="$HOME/t/$fno$fe"
#   else
#     fno=${fno%.${ext}}
#   fi
#   # tmp=$(echo "$fno"| tr -d '_-' | tr -d '#?' | tr -d '=.')
#   # if [[ -z "$tmp" || ${#tmp} -ne 6 || "$tmp" != "$fno" ]]; then
#   #   fno=$tmp
#   #   # if [[ ${#fno} -gt 6 ]]; then
#   #   #   # fno=${fno::6}
#   #   #   fno=$(echo "$fno"| tr -d '_-' | tr -d '#?' | tr -d '=.')
#   #   # fi
#   #   if [[ ${#fno} -gt 6 ]]; then
#   #     fno=${fno: -6}
#   #   elif [[ ${#fno} -lt 6 ]]; then
#   #     fno+=$(date "+%H%M%S")
#   #   fi
#   #
#   if true; then
#     fno=$(shasum "$fn" | awk '{print $1}')
#     # fno=$(ipfs add -n -Q "$fn")
#
#     mv "$fn" "$HOME/t/$fno$fe"
#     fn="$HOME/t/$fno$fe"
#   fi
# fi
fno=$(ipfs add -n -Q "$fn")
if [[ -z "$fno" ]]; then
  # fno=$(date "+%H%M%S")
  fno=$(shasum "$fn" | awk '{print $1}')
fi
if [[ -n "$ext" ]]; then
  fe=".$ext"
fi
if [[ "$fn" != "$HOME/t/$fno$fe" ]]; then
  mv "$fn" "$HOME/t/$fno$fe"
  fn="$HOME/t/$fno$fe"
fi

echo "$fn"

if [[ "$5" == "just_path" ]]; then
  exit
fi

# ft=$(echo "$html" | file --mime-type -b -- -)
if [[ -z "$4" && "$ft" == "text/html" ]]; then
  # echo "$html" | tr "\n" " " | sed 's|.*<title>\([^<]*\).*</head>.*|\1|;s|^\s*||;s|\s*$||' || exit $?
  # cat "$fn" | tr "\n" " " | sed 's|.*<title>\([^<]*\).*</head>.*|\1|;s|^\s*||;s|\s*$||' || exit $?
  # echo
  # s=$(grep --binary-file=text -P -o '<title>.*?</title>'  "$fn" | head -n1 )
  s=$(grep --binary-file=text -P -o '<title>.*?</title>'  "$fn" | cut -d'>' -f2- | cut -d'<' -f1)
  # if [[ -n "$s" ]]; then
  if [[ -n "$(echo $s)" ]]; then
    # echo -n "${s:7:-8} "
    echo -n "${s} "
  else
    # s=$(grep --binary-file=text -P -o '<title ?[^>]+>.*?</title>' "$fn" | head -n1 | grep -o '>.*<' )
    s=$(grep --binary-file=text -P -o '<title ?[^>]+>.*?</title>' "$fn" | cut -d'>' -f2- | cut -d'<' -f1)
    if [[ -n "$(echo $s)" ]]; then
      # echo -n "${s:1:-1} "
      echo -n "${s} "
    else
      # echo null
      echo -n "没找到标题 "
    fi
  fi
  du -h -- "$fn" | cut -f1
  # rm "$fn"
  # exit
  exit $sc
  exit 0
  exit $?
elif [[ $sc -ne 0 ]]; then
  echo -n "$ft "
  du -h -- "$fn" | cut -f1
  exit $sc
else


  # fs=$(du -b -- "$fn" | cut -f1)
  fs=$(du -h -- "$fn" | cut -f1)
  ft=$(file -i -b -- "$fn") 
  ft3=$(file -b -- "$fn") 


  # fe=$(file --extension -- "${fn}" | grep -o -P "[^\s/]+$")
  # fe=$(echo "$html" | file --extension -b -- -)
  # size=$(echo "$html" | wc -c)
  # echo "$fn"
  # echo -n "[file]($URL): "
  echo "$ft $fs"
  echo "$ft3"
  # echo
  # echo "- https://$DOMAIN/${fno}${fe}"
  # echo
  # echo "- $(bash "$SH_PATH/file_to_ipfs.sh" "${fn}")"

  # nohup mv "$fn" "$LP/$fno$fe" &>/dev/null &

fi
# done


# sed 's|.*<title[^>]*>\([^<]*\).*</head>.*|\1|;s|^\s*||;s|\s*$||'
# while read -r URL; do
#     echo -n "$URL --> "
#     # title=$(wget --header='Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
#     #   --user-agent=="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36" \
#     #       -q -O - "$URL" )
#     title=$(curl -L -m 16 -s -o - -w '%{http_code}' -H "Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6" "$URL" -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' )
#     title=$(echo "$title" | grep -o -E "<title[^>]*>.*</title>")
#     echo "$title"
#     title=${title#*>}
#     title=${title%%<*}
#     echo "$title"
# done
