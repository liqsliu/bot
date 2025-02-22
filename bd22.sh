#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6000 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "把问题翻译成英文，然后交给bard，再把回答翻译为中文。"
  echo "用法: .bd22 \$str"
else
text=$(bash "$SH_PATH/trans.sh" -brief :en "$*")
bash "$SH_PATH/trans.sh" -brief :zh "$(
ai "$text"
)"
fi
