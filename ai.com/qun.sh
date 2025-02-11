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
  if [[ -z "$1" ]]; then
    echo -e "$(cat)"
  else
    echo -e "$1"
  fi
}


get_jid(){
  # cat | grep -G -o ": .*"
  # cat | sed -r 's/.*: ([^ ]+)($| .*)/\1/1'
  # cat | sed -r 's/(^|\s)(\S+@\S+)($|\s)/\2/1'
  cat | sed -r -e 's|^.*?: ||1' -e 's| .*$||1' | grep -o -P '[^\s]+@[^\s]+'
}

get_jid2(){
  # cat | grep -G -o ": .*"
  # cat | sed -r 's/.*: ([^ ]+)($| .*)/xmpp:\1?join/1'
  # cat | sed -r 's/(^|\s)(\S+@\S+)($|\s)/xmpp:\2?join/1'
  cat | sed -r -e 's|^.*?: ||1' -e 's| .*$||1' | grep -o -P '[^\s]+@[^\s]+' | sed -r 's/^(.*)$/xmpp:\1?join/1'
}


del_jid(){
  local jid=$1
  text=${text// xmpp:$jid?join / }
  text=${text// $jid / }
  text=${text//xmpp:$jid?join /}
  text=${text//$jid /}
  text=${text// xmpp:$jid?join/}
  text=${text// $jid/}
  text=${text//xmpp:$jid?join/}
  text=${text//$jid/}
  text=$(echo "$text"| sed '/^$/d')
}

add() {
  local username=$1
  local text=$2
  text=$(echo "$text"|sed 's/^> //')

  local jid=$(echo "$text"| grep -o -P '(?<=^|\s)[^\s]+@[^\s]+(?=$|\s)'|head -n1)

  if [[ -z "$jid" ]]; then
    echo "没找到群地址"
    return 0
  fi
  if echo "$jid" | grep -q -G '^xmpp:.*?join$'; then
  #   jid=$(echo "$jid" |sed -r 's/^(xmpp:)(.*)(\?join)$/\2/1')
    jid=${jid#xmpp:}
    jid=${jid%?join}
  fi
  del_jid "$jid"

  existed=0
  jids=$(cat "$NOTE_FILE"| sed -r -e 's|^.*?: ||1' -e 's| .*$||1')
  if echo "$jids"| grep -q -F "$jid"; then
    existed=1
  fi
  jid2=$(bash "$SH_PATH/urldecode.sh" "$jid")
  if [[ "$jid2" != "$jid" ]]; then
    del_jid "$jid2"
    if [[ "$existed" -eq 0 ]]; then
      if echo "$jids"| grep -q -F "$jid2"; then
        existed=1
      fi
    fi
    jid=$jid2
  fi
  # if echo "$text"| head -n1 | awk '{print $1}'|grep -q -F "@"; then
  #   :
  # else
  # for line_num in $(echo "$text" | grep -n -F "$jid" | cut -d ':' -f1)
  # do
  #   line=$(echo "$text"|sed -n ${line_num}p)
  #   if [[ "$line" == "$jid" ]]; then
  #     text=$(echo "$text" |sed ${line_num}d)
  #   # elif echo "$line"| grep -q -F "$jid"; then
  #   else
  #     text=$(echo "$text" |sed -r -e $line_num's/(^)\S+@\S+(\s+)//g' -e $line_num's/(\s+)\S+@\S+($)//g' -e $line_num's/(\s+)\S+@\S+(\s+)/ /g')
  #   fi
  # done
  # text="$jid $text"

  # if grep -q -F "$jid" "$NOTE_FILE"; then
  if [[ "$existed" -gt 0 ]]; then
 

    line_num=$(grep -n -F "$jid" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    echo "已存在: $line" | my_decode
  else
    echo "$username$(my_encode "$jid $text")" >>"$NOTE_FILE" && {
      echo "已添加"
      echo "jid: $jid"
      echo "描述: $text"
    } || echo "E: $?"
  fi
}

del() {
  # if [[ -z "$2" ]]; then
  local text=$1
  # else
  #   local tag=$1
  #   local text=$2
  # fi
  # text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1-)
  # [[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
  # line_num=$(grep -n -G "^$text\$" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # line_num=$(grep -n -F "$text" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # if echo "$text"|grep -q -P '^\d+$'; then
  #   line_num=$text
  # else
    # line_num=$(grep -n -G "^$tag" "$NOTE_FILE" | grep -F "$text" | cut -d ':' -f1 | head -n1)
    line_num=$(grep -n -F "$(my_encode "$text")" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # fi
  # echo num$line_num
  # read -p ok?
  if [[ -n "$line_num" ]]; then
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $(my_decode "$line")" || echo "E: $?"
    # sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $text" || echo "E: $?"
  else
    echo "没找到: $text"
  fi
}

list_tags() {
  #  cat "$NOTE_FILE" | cut -d ' ' -f1 |sort -n |awk '{if($0!=line)print; line=$0}'
  # local tags=$(cat "$NOTE_FILE" | cut -d ' ' -f1 | sort -n | uniq)
  # echo $tags
  # echo "all tag:"
  # cat "$NOTE_FILE"| sed -r 's/.*: [^ ]+(( +#[^\s])+)/\1/1'| sed -r 's/ /\n/g' | sort -n | uniq
  # cat "$NOTE_FILE"| sed -r 's/.*: [^ ]+( .*$)/\1/1'|grep -o -P '#\S+' | sort -n | uniq
  cat "$NOTE_FILE"| sed -r 's/.*: [^ ]+( .*$)/\1/1'|grep -o -P '(?<=^|\s)#[^\s]+' | sort -n | uniq
}


print_help(){
  echo "群组列表整理
用法:
.qun [add] [\$jid] [\$text(描述，可以包含#开头的tag，群jid可以放到描述里)]
.qun list [join|jid|jidonly|full] [\$tag]
.qun se \$text
.qun tag
.qun del \$text
.qun help

备份: https://github.com/liqsliu/bot/blob/master/qun.txt
源码: https://github.com/liqsliu/bot/blob/master/qun.sh"

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
log_msg note "$@" >> $LOG_FILE
#
NOTE_FILE="$SH_PATH/group_qun.txt"

username=$1
username=$(my_encode "$1")
text="$2"
[[ -z "$text" ]] && print_help && exit 0
text_1=$(echo "$text"|head -n1)
cmd_1=$(echo "$text_1" | awk '{print $1}' )
cmd_2=$(echo "$text_1" | awk '{print $2}' )

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
  ;;
esac

[[ -z "$text" ]] && [[ "$cmd" != "list" ]] && echo '内容不能为空' && exit 0
# text=$(my_encode "$text")

case "${cmd}" in
list)
  # echo "$tag"
  # my_decode "$(grep -G "^$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  # my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  # my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | sed -r 's|:#[^ ]+ |%|1')"



  full=$(cat "$NOTE_FILE")
  # my_decode "$(echo "$full")"
  for tag in $(echo "$text"|grep -o -P "(?<=^|\s)#[^\s]+")
  do
    full=$(echo "$full"|grep -F "$tag")
  done

  if [[ "$cmd_2" == "jid" ]]; then
    echo "for join"
    echo "$full" | get_jid2 | grep -n ^ | sed 's|:|% |1'
  elif [[ "$cmd_2" == "j" ]]; then
    echo "for join"
    echo "$full" | get_jid2 | grep -n ^ | sed 's|:|% |1'
  elif [[ "$cmd_2" == "join" ]]; then
    echo "for join"
    echo "$full" | get_jid2 | grep -n ^ | sed 's|:|% |1'
  elif [[ "$cmd_2" == "q" ]]; then
    echo jid only
    echo "$full" | get_jid | grep -n ^ | sed 's|:|% |1'
  elif [[ "$cmd_2" == "jidonly" ]]; then
    echo jid only
    echo "$full" | get_jid | grep -n ^ | sed 's|:|% |1'
  elif [[ "$cmd_2" == "full" ]]; then
    echo full
    my_decode "$(echo "$full" | grep -n ^ | sed 's|:|% |1')"
  else
    echo default format
    my_decode "$(echo "$full" | sed -r 's|^.*?: ||1' | grep -n ^ | sed -r 's|^|\n|1' | sed 's|:|% |1')"
  fi
  ;;
se)
  echo "search: $text"
  full=$(cat "$NOTE_FILE")
  # full=$(echo "$full"|grep -F "$tag")
  text=$(my_encode "$text")
  my_decode "$(echo "$full" | grep -n ^ | grep -F "$text" | sed 's|:|% |1')"
  ;;
add)
  add "$username" "$text"
  ;;
del)
  del "$username$text"
  ;;
delete)
  del "$text"
  ;;
*)
  add "$username$text"
  ;;
esac
