#!/bin/bash
# MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-64000000}
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
UA="curl/7.88.1"
LA='Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6'

# https://stackoverflow.com/questions/20317945/limit-size-wget-can-download/20318140#20318140
ulimit -f 204800

MAX_TIMEOUT=16
export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"
# https://stackoverflow.com/questions/55842311/get-page-titles-from-a-list-of-urls
# while read -r URL; do
    # echo -n "$URL --> "
  URL=$1
  if [[ "$2" == raw ]]; then
    html=$(wget -T $MAX_TIMEOUT -q -O - "$URL") || {
      wget --server-response -T $MAX_TIMEOUT -O - "$URL" || echo "E: $?"
      exit
    }

  elif [[ "$2" == direct ]]; then
    unset http_proxy
    unset https_proxy
    html=$(wget -T $MAX_TIMEOUT -q -O - "$URL") || {
      wget --server-response -T $MAX_TIMEOUT -O - "$URL" || echo "E: $?"
      exit
    }

  elif [[ "$2" == curl ]]; then
    html=$(curl -s -L -m $MAX_TIMEOUT -o - -H "$LA" "$URL" -A "$UA") || {
      curl -v -L -m $MAX_TIMEOUT -o - -H "$LA" "$URL" -A "$UA" || echo "E: $?"
      exit
    }

  else
    html=$(wget --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -q -O - "$URL") || {
      wget --server-response --user-agent="$UA" --header="$LA" --header="Accept: */*" -T $MAX_TIMEOUT -O - "$URL" || echo "E: $?"
      exit
    }
  fi
  echo "$html" | tr "\n" " " | \
  sed 's|.*<title>\([^<]*\).*</head>.*|\1|;s|^\s*||;s|\s*$||' || echo "E: $?"
  echo
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
