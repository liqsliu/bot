#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6000 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo "google bard 支持上下文"
  echo ".bd \$str"
  echo "--"
  echo "link: https://github.com/EvanZhouDev/bard-ai"
  echo "link: https://bard.google.com/"
# elif [[ "$2" == "on" ]]; then
#   :
else
# ai "$@"
ai "$*"
fi