#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:8890 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo ".bot \$str"
  echo "/BOT \$str"
  echo
  echo "出现故障请对我说\"reset\""
  echo "毫无感情的机器人，如果希望我的回答不要这么死板，请使用ai命令"
  echo "model: text-davinci-003"
  echo "link: https://beta.openai.com/docs/models/overview"
# elif [[ "$2" == "on" ]]; then
#   :
else
# ai "$@"
ai "$*"
fi
