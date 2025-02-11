#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6002 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo ".ai \$str"
  echo ".bd \$str #有上下文"
  echo "--"
  echo "link: https://github.com/EvanZhouDev/bard-ai"
  echo "link: https://bard.google.com/"
# elif [[ "$2" == "on" ]]; then
#   :
else
# ai "$@"
ai "$*"
fi
