#!/bin/bash

text=$1
# text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
gateway=${2-gateway1}
username=${3-C bot: }

wtf(){
  local text=$(echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
  # local text=$(echo "$1" | sed -e 's/\\/\\\\/g' -e 's/\\\\n/\\n/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
echo "$text"
}

# echo "#" >> ~/t.log
# echo "$text" >> ~/t.log
text=$(wtf "$text")
# echo "##" >> ~/t.log
# echo "$text" >> ~/t.log

username=$(wtf "$username")
ulength=$(echo -n "$username"|wc -c)

# text=$(bash "$SH_PATH/change_long_text.sh" "$text" 4096)
text=$(bash "$SH_PATH/change_long_text.sh" "$text" $[1371-ulength-9])
# text=$(bash "$SH_PATH/change_long_text.sh" "$text" 1370)
cat <<EOF
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF

