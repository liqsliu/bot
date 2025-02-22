#!/bin/bash
#get msg for tox and run cmd
export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
#res="[]"
res=$(curl -m 2 -s http://127.0.0.1:4241/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
bash "$SH_PATH/cmd.sh" "$res"
fi
