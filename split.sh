#!/bin/bash
# split mag < 1024
# just for irc
# copy from sm2.sh

wtf(){
  local text=$1
# text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
  text=$(echo "$text" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
echo "$text"
}

split(){
  local text=$1
  local username=$2

  local MAX_BYTES=${3:-500}
  local ulength=$(echo -n "$username"|wc -c)
  local MAX_BYTES=$[MAX_BYTES-ulength]
  # text=$(wtf1 "$text")
  text_en=$(wtf "$text")
  local length=$(echo -n "$text_en"|wc -c)
  if [[ $length -le $MAX_BYTES ]]; then
    echo "$text_en"
    return
  fi

  # shift
  local i=0
  local now=0
  local n=$[length/MAX_BYTES]
  if [[ $[length%MAX_BYTES] -ne 0 ]]; then
    let n++
  fi
  while true
  do
    # now=$[i*MAX_BYTES]
    # if [[ $((i*MAX_BYTES)) -ge ${#text} ]]; then
    if [[ $now -ge ${#text} ]]; then
      return 0
      break
    fi
    tmp=${text:$now:$MAX_BYTES}
    tmp0=$tmp
    local need_1=0
    while true
    do
      if [[ $[now+${#tmp}] -lt ${#text} ]]; then
        if [[ "${tmp: -1}" != $'\n' ]]; then
          if [[ "${tmp: -1}" != $'\t' ]]; then
            # if [[ "${tmp: -1}" != " " ]]; then
              if [[ -n "$(echo "$tmp"|sed -e '$d' -e '/^ *$/d')" ]]; then
                tmp=$(echo "$tmp"|sed '$d')
                need_1=1
              fi
            # fi
          fi
        fi
      fi
      tmp1=$(wtf "$tmp")
      # if [[ ${#tmp1} -gt $MAX_BYTES ]]; then
      if [[ $(echo -n "$tmp1"|wc -c) -gt $MAX_BYTES ]]; then
        tmp=${tmp::-1}
        if [[ $need_1 -eq 1 ]]; then
              need_1=0
        fi
      else
        break
      fi
    done
    if [[ $need_1 -eq 1 ]]; then
      let now++
    fi
    now=$[now+${#tmp}]

    let i++
    # echo "send...$i/$n" &>> $LOG

    # _send "$tmp1" || {
    echo "$tmp1" || {
      return $?
    }

    # sleep 0.5
    if [[ $i -ge 8 ]]; then
      # _send "E: msg is too long, stop sending, now $i/$n" &>> $LOG
      echo "E: msg is too long, stop sending, now $i/$n"
      return 1
    fi
  done
}

split "$@"

