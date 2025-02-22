#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6001 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "把问题翻译成英文，然后交给bard，再把回答翻译为中文。"
  echo "用法: .ai22 \$str"
else
# ai "$@"
# ai "$*"
text=$(bash "$SH_PATH/trans.sh" -brief :en "$*") || exit $?
text=$(ai "$text") || exit $?
bash "$SH_PATH/trans.sh" -brief :zh "$text"
fi
