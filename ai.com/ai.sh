#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6001 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "google bard 不支持上下文，每次提问都是新的独立的上下文。若想让bot记住上下文，请用bd命令。"
  echo "用法: .ai \$str"
  # echo ".ai reset: 出错时使用"
  echo "--"
  echo "link: https://github.com/EvanZhouDev/bard-ai"
  echo "link: https://bard.google.com/"
else
# ai "$@"
ai "$*"
fi
