#!/bin/bash
export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"
# https://stackoverflow.com/questions/55842311/get-page-titles-from-a-list-of-urls
while read -r URL; do
    echo -n "$URL --> "
    wget -q -O - "$URL" | \
       tr "\n" " " | \
       sed 's|.*<title>\([^<]*\).*</head>.*|\1|;s|^\s*||;s|\s*$||'
    echo
done


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
