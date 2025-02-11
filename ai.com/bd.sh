#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6000 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "google bard 支持上下文"
  echo "用法: "
  echo ".bd \$str"
  echo ".bd reset: 出错时使用，也可用于新建对话，清空上下文。"
  echo "--"
  echo "link: https://github.com/EvanZhouDev/bard-ai"
  echo "link: https://bard.google.com/"
else
# ai "$@"
ai "$*"
fi
