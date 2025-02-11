#!/bin/bash
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
res=$(curl -m 2 -s http://127.0.0.1:4240/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
bash "$SH_PATH/gm2.sh" "$res"
fi

