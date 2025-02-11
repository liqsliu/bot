#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

# if [[ $(( $(date "+%s") % 600 )) -lt 25 ]]; then
#   sleep $(( 30 - $(date "+%s") % 600 ))
# else
#   sleep $(( 630 - $(date "+%s") % 600 ))
# fi


per=1800

if [[ $(( $(date "+%s") % per )) -gt 55 ]]; then
  sleep $(( per - $(date "+%s") % per ))
fi
#bash ~/tg.sh "$@"
#bash "$SH_PATH/tg.sh" "$@"
#python3 "$SH_PATH/twtg.py" "$@"
bash "$SH_PATH/sm.sh" "$@"
