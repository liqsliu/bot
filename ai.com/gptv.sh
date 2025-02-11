#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}

wtf(){
  local text=$(echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
  # local text=$(echo "$1" | sed -e 's/\\/\\\\/g' -e 's/\\\\n/\\n/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
echo "$text"
}

ai(){
# echo -n test
# echo "生命的意义是一个非常深奥的问题，很难用简单的语言来回答。对于不同的人来说，生命的意义可能也不同。对于某些人来说，生命的意义可能是为了实现自己的梦想和目标，或者是为了帮助别人。对于其他 人来说，生命的意义可能是为了寻找真理和答案，或者是为了寻求快乐和幸福。总之，生命的意义是一个个人主观的问题，每个人都必须自己去思考和发现。"

# curl -m 1800 -s -XPOST -d "$*" 127.0.0.1:8888 || exit $?
#echo "$*" | nc -w 1800 127.0.0.1 8888 || exit $?
local role=${2:-user}
local text=${1:-你好}
text=$(wtf "$text")
curl -s --location 'http://127.0.0.1:5005/v1/chat/completions' --header 'Content-Type: application/json' --data '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "'"$role"'", "content": "'"$text"'"}],
     "stream": false
   }'

}



if [[ -z "$1" ]]; then
  echo "openai gpt3.5"
  echo ".gptv \$str"
  echo ".gptv -u \$username \$str"
  # echo "/GPT \$str"
  echo '--'
  echo "https://github.com/LanQian528/chat2api"
  echo "https://chat.openai.com/"
  # echo "只能单线程工作，并且速度较慢。但是结果可能比ai和bot命令好一点。"
  # echo "model: ChatGPT"
  # echo "link: https://openai.com/blog/chatgpt/"
# elif [[ "$2" == "on" ]]; then
#   :
else
  if [[ "$1" == "-u" ]]; then
    shift
    role=$1
    shift
    ai "$*" "$role"
  else
    ai "$*"
  fi
fi
