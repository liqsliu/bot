#!/bin/bash

# set -x

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

my_encode_old() {
  # [[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")

  if [[ $(echo "$@" | wc -l) -le 1 ]]; then
    #    text="$(printf "%q" "${@}")"
    text=$(printf "%q" "${*}")
  else
    text=$(printf "%q" "${*}")
    #text="${text:2}"
    text="${text#\$\'}"
    text="${text%\'}"
    text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1-)
  fi
  cat <<EOF
$text
EOF

}

my_encode() {

  local text="$1"
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

add() {

  local text=$1
  #if [[ $(grep -c -G "^$text\$" "$NOTE_FILE") -ge 1 ]]; then
  # if grep -q -G "^$text\$" "$NOTE_FILE"; then
  if grep -q -F "$text" "$NOTE_FILE"; then
    line_num=$(grep -n -F "$text" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    echo "已存在: $line"
  else
    # echo "$text";exit 0
    # echo "$1" >> "$NOTE_FILE" && echo "I: added: $(grep -G "^$1\$" "$NOTE_FILE")" || echo "E: $?"
    echo "$text" >>"$NOTE_FILE" && echo "已添加: $text" || echo "E: $?"
  fi
}

del() {
  if [[ -z "$2" ]]; then
    local text=$1
  else
    local tag=$1
    local text=$2
  fi
  # text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1-)
  # [[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
  # line_num=$(grep -n -G "^$text\$" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # line_num=$(grep -n -F "$text" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  if echo "$text"|grep -q -P '^\d+$'; then
    line_num=$text
  else
    line_num=$(grep -n -G "^$tag" "$NOTE_FILE" | grep -F "$text" | cut -d ':' -f1 | head -n1)
  fi
  # echo num$line_num
  # read -p ok?
  if [[ -n "$line_num" ]]; then
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $line" || echo "E: $?"
    # sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $text" || echo "E: $?"
  else
    echo "没找到: $text"
  fi
}

list_tags() {
  #  cat "$NOTE_FILE" | cut -d ' ' -f1 |sort -n |awk '{if($0!=line)print; line=$0}'
  local tags=$(cat "$NOTE_FILE" | cut -d ' ' -f1 | sort -n | uniq)
  echo $tags

}


print_help(){
  echo "公共记事本
用法: .note [add|del|list|se|tag|help] \$tag [\$text]
用法: .note delete \$tag [\$name: ][\$text]
用法: .note delete [\$tag] [\$number(行号)]

tag的格式：#非空白字符

tag可以写在命令（add del list等）前面

delete: text可以不写全。如果不设置name，text可以是任意位置的字符串片段。如果设置了name，text必须从首字母开始。留空也可以。总之，会删除第一个匹配到的记录。text可设为一串数字，会当作行号处理。name参数要包含平台名字，比如X T...

del: text可以不写全，但必须从首字母开始，留空也可以。总之，会删除第一个匹配到的记录。

示例：
列出已经在使用的tag: .note tag
查看默认tag下的记录: .note list
添加记录到默认tag: .note add #default some text
添加记录到默认tag: .note #default add some text
添加记录到默认tag: .note #default some text
添加记录到默认tag: .note some text

备份: https://github.com/liqsliu/bot/blob/master/group_note.txt
源码: https://github.com/liqsliu/bot/blob/master/note.sh"

}

log_msg(){
  echo
  echo
  date
  echo "#### $1 ####"
  shift
  # echo "msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent"
  local i=0
  for i in "$@"
  do
    echo -n "|$i|"
  done
  echo
  echo "#### end ####"
}



shorter(){
text=$(echo "$text" | sed -r '1s/^\s*\S+\s*//' )
}


# date >> ~/tera/mt_msg.log
# echo "$*" >> ~/tera/mt_msg.log
# log_msg note "$@" >> $LOG_FILE
log_msg note "$@" >> $LOG
#
NOTE_FILE="$SH_PATH/group_note.txt"

username=$1
username=$(my_encode "$1")
text=$2
[[ -z "$text" ]] && print_help && exit 0
text_1=$(echo "$text"|head -n1)
cmd_1=$(echo "$text_1" | awk '{print $1}' )
cmd_2=$(echo "$text_1" | awk '{print $2}' )

echo "cmd_1: $cmd_1, cmd_2: $cmd_2" >> $LOG_FILE
# if echo "$cmd_1" | grep -q -P "^#\S+$"; then
# if echo "$cmd_1" | grep -q -P '^#\S+$'; then
if echo "$cmd_1" | grep -q -P '^#[^\s]+$'; then
echo "cmd_1 is a tag: $tag" >> $LOG_FILE
  tag="$cmd_1"
  # text=$(echo " $text" | cut -d ' ' -f3-)
  # text=$(echo "$text" | sed -r  's/^\s*\S+\s*//' )
  shorter
  case "${cmd_2}" in
  list)
    cmd=list
    # text=$(echo "$text" | sed -r  's/^\s*\S+\s*//' )
    shorter
    ;;
  se)
    cmd=se
    shorter
    ;;
  add)
    cmd=add
    # text=$(echo "$text" | sed -r  's/^\s*\S+\s*//' )
    shorter
    ;;
  del)
    cmd=del
    shorter
    ;;
  delete)
    cmd=delete
    shorter
    ;;
  *)
    [[ -z "$text" ]] && cmd=list || cmd=add
    ;;
  esac

else
  case "${cmd_1}" in
  help)
    print_help
    exit 0
    ;;
  tag)
    du -h "$NOTE_FILE"
    list_tags
    exit 0
    ;;
  list)
    cmd=list
    shorter
    ;;
  se)
    cmd=se
    shorter
    ;;
  add)
    cmd=add
    shorter
    ;;
  del)
    cmd=del
    shorter
    ;;
  delete)
    cmd=delete
    shorter
    ;;
  *)
    cmd=add
    cmd_2=""
    ;;
  esac
  # if echo "$cmd_2" | grep -q -P "^#\S+$"; then
  if echo "$cmd_2" | grep -q -P '^#[^\s]+$'; then
    echo "cmd_2 is a tag: $tag" >> $LOG_FILE
    tag="$cmd_2"
    shorter
  else
    tag="#default"
  fi
fi

[[ -z "$text" ]] && [[ "$cmd" != "list" ]] && echo '内容不能为空' && exit 0
echo "finally text: $text" >> $LOG_FILE
text=$(my_encode "$text")


# echo $cmd
# echo $tag
# echo "$tag $username$text"
# exit

case "${cmd}" in
list)
  echo "$tag"
  # my_decode "$(grep -G "^$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  # my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | sed -r -e 's|:#[^ ]+ |%|1' -e 's|^|\n|')"
  ;;
add)
  add "$tag $username$text"
  ;;
se)
  echo "search: $text"
  full=$(cat "$NOTE_FILE")
  # full=$(echo "$full"|grep -F "$tag")
  # text=$(my_encode "$text")
  my_decode "$(echo "$full"|grep -F "$text")"
  ;;
del)
  del "$tag $username$text"
  ;;
delete)
  del "$tag" "$text"
  ;;
*)
  add "$tag $username$text"
  ;;
esac
