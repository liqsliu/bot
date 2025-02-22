#!/bin/bash


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd -P )}


_(){
  # curl -m 64 -v "https://v.api.aa1.cn/api/api-lj-gf/index.php?url=$(bash "$SH_PATH/urlencode.sh" "$*")" || exit $?
  curl -m 64 -s "https://v.api.aa1.cn/api/api-lj-gf/index.php?url=$(bash "$SH_PATH/urlencode.sh" "$*")" || exit $?
  # echo
}

cmd=${0##*/}
cmd=${cmd%%.*}
if [[ -z "$1" ]]; then
  echo ".$cmd"
  echo ".$cmd \$str"
  echo "/$cmd \$str"
  echo '---'
  echo 'https://www.free-api.com/doc/602'
# elif [[ "$2" == "on" ]]; then
#   :
else
# ai "$@"
_ "$*"
fi
