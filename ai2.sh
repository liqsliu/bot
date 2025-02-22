#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6001 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "把问题翻译成英文，然后交给bard，同时用英文要求bard用中文回答"
  echo "用法: .ai2 \$str"
else
# ai "$@"
# ai "$*"
text=$(bash "$SH_PATH/trans.sh" -brief :en "$*") || exit $?
ai "$text
Please answer in Chinese."
fi
