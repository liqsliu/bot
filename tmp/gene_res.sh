#!/bin/bash
#text=$(echo "$1" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
#[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")


text=$1
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
text=$(bash "$SH_PATH/change_long_text.sh" "$text" 4096)
gateway=${2-gateway1}
username=${3-bot}



text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"

[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")


[[ -z "$text" ]] && exit 1
cat <<EOF
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF





exit 0


text="$(printf "%q" "'${text}")"
if [[ "${text:0:2}" == "\\'" ]]; then
  text=${text:2}
  # text=$(echo -e "$text")
  # {"message":"Syntax error: offset=12, error=invalid character ' ' in string escape code"}
  text="$(echo "$text" | sed "s/\\\\ / /g")"
  # text="$(echo "$text" | sed "s/\\\\?/?/g")"
else
  text="${text:4}"
  text="${text%\'}"
  text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  text="$(echo "$text" | sed "s/\\\\'/'/g")"
fi

[[ -z "$text" ]] && exit 1
cat <<EOF
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF
