#!/bin/bash



SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

NOTE_FILE="$SH_PATH/group_note.txt"


my_encode() {

  local text="$1"
  # text='1
  # 2\n3'
  text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1-)
  # text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1-)
  [[ $(echo "$text" | wc -l) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
  # echo -e "$text"
  cat <<EOF
$text
EOF

}

my_decode() {
  echo -e "$1"
}


get_a(){
  # faq_text=$(bash "$SH_PATH/note.sh" "" "#faq" "list")
  local text_en=$(my_encode "$1")
  # faq_text=$(grep -G "^$text|\$" "$NOTE_FILE" | cut -d "|" -f2-)
  faq_text=$(grep -G "^#faq " "$NOTE_FILE" | cut -d ":" -f2- | grep -G "^ $text_en|" | cut -d "|" -f2-)
  if [[ -z "$faq_text" ]]; then
    return 1
  else
    my_decode "$faq_text"
    return 0
  fi
}





#get_a "$*"

text=$1
username=$2

if [[ "${text:0:4}" == ".faq" ]]; then
#  if [[ -z "$1" || "$1" == "help" ]]; then
  if [[ -z "${text:5}" || "${text:5}" == "help" ]]; then
    echo "自定义问答"
#    echo "格式为: .faq 触发关键词|回复内容"
#    echo "添加示例: .faq ping|pong"
    echo "添加示例: .note #faq ping|pong"
    echo "使用(触发): ping"
  else
    :
    # if [[ $(echo "$text" | grep -c -P "^.faq \S+.*\|\S+.*") -eq 1 ]]; then
    # #  if bash "$SH_PATH/faq.sh" "$(echo "${text:5}" | cut -d"|" -f1)" &> /dev/null ; then
    #  if get_a "${text:5}" &> /dev/null ; then
    #    echo "不能和已有记录重复"
    #  else
    #   #  bash "$SH_PATH/note.sh" "$username" "#faq add i $* i ${text:5}" && echo && echo "问: $(echo "${text:5}" | cut -d"|" -f1)" && echo "答: $(echo "${text:5}" | cut -d"|" -f2)" || echo "E: $?"
    #   bash "$SH_PATH/note.sh" "$username" "#faq add ${text:5}" || echo "E: $?"
    #  fi
    # else
    #   echo "格式不正确"
    # fi
  fi
else
  get_a "$text"
fi

