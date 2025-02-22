#!/bin/bash



target=zh

tr(){
  # -H 'Content-Type: application/json' \
curl -s -X POST 'https://translate.monocles.de/translate' \
  -d "q=$*" \
  -d 'source=auto' \
  -d "target=$target" \
  -d 'fromat=json' \
  -d 'api_key=' | jq -r '.translatedText'
}

if [[ -z "$1" ]] || [[ "$1" == "help" ]]; then
  echo "翻译
用法: .mtr \$text
用法: .mtr -t en \$text
--
https://translate.monocles.de/"
exit
elif [[ "$1" == "-t" ]]; then
  target=$2
  shift
  shift
fi

tr "$@"
