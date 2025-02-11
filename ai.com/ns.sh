#!/bin/bash

#get net spped

interval=1


dev_data=""
get_data(){
#$( ip route get 9.9.9.9 | cut -d " " -f5 | head -n 1 ) == "$ethn"
#[[ -z "$1" ]] && ethn=$( ip route get 9.9.9.9 | cut -d " " -f5 | head -n 1 ) || ethn="$1"
#  local ethn=$( ip route get 9.9.9.9 | cut -d " " -f5 | head -n 1 ) || ethn="eth0"
#  [[ -z "$1" ]] && local dev_name=${ethn} || local dev_name="$1"
#  dev_data=$(cat /proc/net/dev | grep "^[ ]*${dev_name}:")
#  dev_data=$(cat /proc/net/dev)
  dev_data=$(cat /proc/net/dev | sed 's/://g' | sed 's/  */ /g' | sed 's/^ *//g' | cut -d " " -f "1,2,10")
#  dev_data=$(cat /proc/net/dev | grep "^[ ]*${ethn}:")
}
human_data2(){

  if [[ $1 -eq 0 ]];then
    echo -n "    "
  elif [[ $1 -le 1024 ]];then
    echo -n "   ."
  elif [[ $1 -le 10238976 ]];then
    human_data4 $(( $1 / 1024 ))
  else
    human_data4 $(( $1 / 1024 / 1024))
    echo -n "M"
  fi
}
human_data4(){
#  if [[ $1 -ge 1048576 ]];then
  if [[ $1 -ge 1000 ]];then
    echo -n $1
  elif [[ $1 -ge 100 ]];then
    echo -n " "
    echo -n $1
  elif [[ $1 -ge 10 ]];then
    echo -n "  "
    echo -n $1
  else
  #RX=$(echo $1 | awk '{print $1/1024 "KB/s"}')
    echo -n "   "
    echo -n $1
  fi


}

human_data(){
  human_data2 $(( $1 / $interval ))
  return 0

  if [[ $1 -lt 1024 ]];then
    echo "${1}B/s"
  elif [[ $1 -ge 104857600 ]];then
  #  RX=$(echo $1 | awk '{print $1/1048576 "MB/s"}')
    echo "$(( $1 / 1048576 ))MB/s"
  elif [[ $1 -ge 10485760 ]];then
  #  RX=$(echo $1 | awk '{print $1/1048576 "MB/s"}')
    echo $1 | awk '{printf ( "%.1fMB/s\n",$1/1048576) }'
  elif [[ $1 -ge 1048576 ]];then
  #  RX=$(echo $1 | awk '{print $1/1048576 "MB/s"}')
    echo $1 | awk '{printf ( "%.2fMB/s\n",$1/1048576) }'
  elif [[ $1 -ge 102400 ]];then
    echo "$(( $1 / 1024 ))KB/s"
  elif [[ $1 -ge 10240 ]];then
    echo $1 | awk '{printf ( "%.1fKB/s\n", $1/1024) }'
  else
  #RX=$(echo $1 | awk '{print $1/1024 "KB/s"}')
    echo $1 | awk '{printf ( "%.2fKB/s\n", $1/1024) }'
  fi
}

print_rec(){
  #for(( local i=0; i<$1; i++ ))
  local i
  for(( i=0; i<$1; i++ ))
  do
    echo -n "#"
  done
}
print_multi_char(){
  #for(( local i=0; i<$1; i++ ))
  local i
  for(( i=0; i<$1; i++ ))
  do
    echo -n "$2"
  done
}

send_log() {
 [[ -n "$3" ]] && termux-notification -i $1 -t "$2" --alert-once --icon $3 || termux-notification -i $1 -t "$2" --alert-once
}


log(){
#send_log 1 "$1" "$2"
#echo -ne "\n\033[40;37m$1\033[0m\r"
echo "$1"
}






print_data=""
ping_dns(){
  TM=$(date "+%Y%m%d_%H%M%S")
  #dns_server=119.29.29.29
#  dns_server=$1
  dns_server="${1:-223.5.5.5}"
  ping_res=$(ping -c 1 -W 1 $dns_server | cut -d "=" -s -f 4| cut -d " " -f 1)
  if [[ -n "$ping_res" ]];then
  print_data="$print_data $2$ping_res"
  else
    echo -ne $1 >> tmp
    echo -ne " " >> tmp
    date >> tmp
  fi
}

get_print_data(){

  dev_name=$1
  if [[ -n "$dev_name" ]]; then
    RX_pre=$(echo "$old_dev_data" | grep "^${dev_name} " | awk '{print $2}')
    TX_pre=$(echo "$old_dev_data" | grep "^${dev_name} " | awk '{print $3}')
    RX_next=$(echo "$dev_data" | grep "^${dev_name} " | awk '{print $2}')
    TX_next=$(echo "$dev_data" | grep "^${dev_name} " | awk '{print $3}')
    RX=$((${RX_next:-0}-${RX_pre:-0}))
    TX=$((${TX_next:-0}-${TX_pre:-0}))

    [[ -n "$2" ]] && print_data="$(human_data $TX) $(human_data $RX)" || print_data="$print_data $dev_name $(human_data $TX) $(human_data $RX)"
#  else print_data="$print_data tun - -"

    [[ -n "$2" ]] && RTX=$RX
  else
#    echo -n "$2"
    [[ -n "$2" ]] && print_data="$2"
  fi

}


 
RX_pre=0
TX_pre=0
wgrx=0
wgtx=0

  get_data
  old_dev_data="$dev_data"


  eth=$( ip route get 9.9.9.9 | cut -d " " -f5 | head -n 1 ) 
  echo "online: $eth"
  echo "unit: KB/s"
  echo "up down"

max_time=5
[[ -n "$1" ]] && max_time=$1

now_time=0

while true
do
 
  now_time=$((now_time+1))

  if [[ "$now_time" -gt "$max_time" ]];
  then
    break
  fi

  #get_data wg
#  ip li sh dev wg && get_data wg || get_data tun0
#  RX_next=$(echo "$dev_data" | sed 's/:/ /g' | awk '{print $2}')
#  wgrx=$(echo "$dev_data" | sed 's/:/ /g' | awk '{print $2}')
#  wgtx=$(echo "$dev_data" | sed 's/:/ /g' | awk '{print $10}')



#  sleep $interval
#  sleep $(( ${interval} * 1000000000 - $(date "+%N") ))
  sleep $( echo $interval $(date "+%N") | awk '{printf("%.2f",$1-$2/1000000000)}' )
#  echo -e "\t RX `date +%k:%M:%S` TX"
#  echo -e "\t TX `date +%k:%M:%S` RX"

  #get_data $ethn

  get_data

#  dev_name=$( ip route get 9.9.9.9 | cut -d " " -f5 | head -n 1 ) 
  dev_name=$eth
  get_print_data "$dev_name" "- -"


  dev_name=$(ip ad show up type tun | head -n 1|awk '{print $2}' | sed 's/://g')
  get_print_data "$dev_name"


  dev_type=wireguard
  dev_name=$(ip ad show up type $dev_type | head -n 1|awk '{print $2}' | sed 's/://g')
  get_print_data "$dev_name"

  #dev_name=$(ip ad show up type wireguard | head -n 1|awk '{print $2}' | sed 's/://g')
  dev_name_static=rndis0
#  dev_name=$(ip li | grep $dev_name_static &>/dev/null && ip ad show up dev $dev_name_static | head -n 1|awk '{print $2}' | sed 's/://g')
  dev_name=$(ip ad show up dev $dev_name_static 2>/dev/null | head -n 1|awk '{print $2}' | sed 's/://g' )
  get_print_data "$dev_name"

  dev_name_static=wlan0
  dev_name=$(ip ad show up dev $dev_name_static 2>/dev/null | head -n 1|awk '{print $2}' | sed 's/://g')
  get_print_data "$dev_name"

  dev_name_static=wlan1
  dev_name=$(ip ad show up dev $dev_name_static 2>/dev/null | head -n 1|awk '{print $2}' | sed 's/://g')
  get_print_data "$dev_name"

#  ping_dns 119.29.29.29 T
#  ping_dns 223.5.5.5 A
#  `nohup ./ping_log.sh 119.29.29.29 &>/dev/null &; nohup ./ping_log.sh 223.5.5.5 &>/dev/null &` 2>/dev/null

#  `nohup ./ping_log.sh 119.29.29.29 &>/dev/null &
#  nohup ./ping_log.sh 223.5.5.5 &>/dev/null &` 2>/dev/null




#  RTX=$(( TX + RX ))
#  RX=$( human_data $RX ) 
#  TX=$( human_data $TX ) 
#  echo -e "$ethn \t $RX $TX "
#  echo -e "$ethn \t $RX $TX "
#  echo -e "$ethn  $TX $RX "
#  clear
#  termux-notification -i 1 -t "$print_data"
  [[ $RTX -eq 0 ]] && flag=0 || flag=$(( RTX / 1024 ))
  [[ $flag -ne 0 ]] && flag=${#flag}
  case $flag in
    1)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_one
      icon=look_one
      ;;
    2)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_two
      icon=look_two
      ;;
    3)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_3
      icon=look_3
      ;;
    4)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_4
      icon=look_4
      ;;
    5)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_5
      icon=look_5
      ;;
    6)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon looks_6
      icon=look_6
      ;;
    [7-9])
      #termux-notification -i 1 -t "$print_data" --alert-once --icon bolt
      icon=bolt
      ;;
    0)
      #termux-notification -i 1 -t "$print_data" --alert-once --icon exposure_zero
      icon=exposure_zero
      ;;
    *)
#      termux-notification -i 1 -t "$print_data" --alert-once --icon image_search
      #termux-notification -i 1 -t "$print_data" --alert-once
      icon=image_search
      ;;
  esac
  log "$print_data" $icon
  old_dev_data="$dev_data"

#  echo -ne "$ethn $TX $RX "
#echo -ne "$ethn $(human_data $TX) $(human_data $RX) "
#echo -ne "$(human_data $TX) $(human_data $RX) "


  #print_rec ${#RTX}
#  [[ $TX -gt 0 ]] && print_multi_char ${#TX} "^"
#  [[ $RX -gt 0 ]] && print_multi_char ${#RX} "!"
#  print_multi_char $( echo $TX | awk '{printf("%.0f",log($1)/log(100))}' )  "|"
#  print_multi_char $( echo $RX | awk '{printf("%.0f",log($1)/log(100))}' )  "="
  RX_pre=${RX_next}
  TX_pre=${TX_next}


#  ip li sh dev wg && get_data wg || get_data tun0
#  echo -ne "wg "
#  echo -n $(human_data $(( $(echo "$dev_data" | sed 's/:/ /g' | awk '{print $10}') - ${wgtx} )) )
#  echo -ne " "
#  echo -n $( human_data $(( $(echo "$dev_data" | sed 's/:/ /g' | awk '{print $2}') - ${wgrx} )) )
#  echo ""
 
done
