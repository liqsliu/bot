#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
LP=${LP:-/var/www/dav/tmp}
#DOMAIN=${DOMAIN:-liuu.tk}
DOMAIN=$(cat $SH_PATH/DOMAIN)
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-15000000}




#BEARER_TOKEN="$(cat ~/keys | grep BEARER_TOKEN | cut -d' ' -f 2)"
# BEARER_TOKEN="$(cat "$SH_PATH//keys" | grep BEARER_TOKEN | cut -d' ' -f 2)"

# PRIVATE_KEYS_PATH="${HOME}/vps/private_keys.txt"
# BEARER_TOKEN=$(grep BEARER_TOKEN "$PRIVATE_KEYS_PATH")
# BEARER_TOKEN=${BEARER_TOKEN#* }

set_my_value BEARER_TOKEN



get_tw_name(){

  local id=$1
  id=${id%%\"}
  id=${id##\"}


#  curl -s --request GET "https://api.twitter.com/2/users?ids=$id&user.fields=name,username" --header "Authorization: Bearer $BEARER_TOKEN"  | jq '.data[0].name' # username = id
  curl -s --request GET "https://api.twitter.com/2/users?ids=$id&user.fields=name,username" --header "Authorization: Bearer $BEARER_TOKEN"  | jq -r '.data[0].name' # username = id

}

myjq(){
  local tmp=$(cat | jq -r ".$1")
  if [[ "$tmp" != "null" ]]; then
    echo "$tmp"
  fi
}

get_tw_text(){
  local tw_res=$1
  local name=$(echo "$tw_res" | jq -r ".user.name")
  local name_id=$(echo "$tw_res" | jq -r ".user.screen_name")
  if [[ "$name_id" == "null" ]]; then
    return 1
  fi
  local text=$(echo "$tw_res" | jq -r ".text")


  # echo "$name@$name_id: $text"
  # echo entities
  local entities_num=$(echo "$tw_res" | jq -r ".entities.urls|length")
  # local res=''
  for((i=0; i<$entities_num ; i++ )); do
    local url1=$(echo "$tw_res" | jq -r ".entities.urls[$i].url")
    local url2=$(echo "$tw_res" | jq -r ".entities.urls[$i].expanded_url")
#     if [[ -z "$res" ]]; then
#       echo
#       res='urls:'
#     fi
#     res+="
# - $url1 $url2"
    text=$( echo "$text" | sed "s|$url1| $url2 |" )
  done
  # echo "$res"
  echo "[$name]($URL) @$name_id
$text"

  local media_num=$(echo "$tw_res" | jq -r ".mediaDetails|length")
  local res=''
  for((i=0; i<$media_num ; i++ )); do
    if [[ -z "$res" ]]; then
      echo
      res='media:'
    fi
    res+="
- "

    local media_type=$(echo "$tw_res" | jq -r ".mediaDetails[$i].type")
    if [[ "$media_type" == video ]]; then
      res+="$media_type: "
      local videos=$(echo "$tw_res" | jq -r ".mediaDetails[$i].video_info.variants")
      local length_v=$(echo "$videos" | jq -r ".|length")
      local m3u8
      for((j=0; j<$length_v; j++ )); do
        local url_v=$(echo "$videos" | jq -r ".[$j].url")
        local type_v=$(echo "$videos" | jq -r ".[$j].content_type")
        if [[ "$type_v" == "video/mp4" ]]; then
          res+="[$type_v"
          res+=" "
          res+=$(echo "$videos" | jq -r ".[$j].bitrate")
        else
          m3u8+="[$type_v]($url_v) "
          continue
        fi
        res+="]($url_v)"
        if [[ $j -ne $[length_v-1] ]]; then
          res+=" ||"
        fi
        res+=" "
      done
      if [[ -n "$m3u8" ]]; then
        res+="|| $m3u8"
      fi
      res+="| [photo]($(echo "$tw_res" | jq -r ".mediaDetails[$i].media_url_https"))"
    else
      res+=$(echo "$tw_res" | jq -r ".mediaDetails[$i].media_url_https")
    fi

  done
  echo "$res"


  # echo card
  local card=$(echo "$tw_res" | jq -r ".card")
  if [[ "$card" != "null" ]]; then
    echo
    # echo card: $(echo "$tw_res" | jq -r ".card.url")
    echo -n "card: "
    echo "$card" | myjq binding_values.title.string_value
    echo "$card" | myjq url
    echo "$card" | myjq binding_values.description.string_value
  fi
}

get_tw_url(){
  local tw_res=$1
  local name_id=$(echo "$tw_res" | jq -r ".user.screen_name")
  local id_str=$(echo "$tw_res" | jq -r ".id_str")
  echo "https://x.com/$name_id/status/$id_str"
}


get_tw(){
  local id=$1
  # https://x.com/slippertopia/status/1850867135897280708
  # https://cdn.syndication.twimg.com/tweet-result?id=1808326779083579400&token=123
  # https://cdn.syndication.twimg.com/tweet-result?id=1884149421535002849&token=thx
  local tw_res=$(curl -s --request GET "https://cdn.syndication.twimg.com/tweet-result?id=$id&token=thx" )
  # [[ "$2" == "debug" ]] && local tw_res=$(cat twitter3.json)
  # [[ "$2" == "debug" ]] && echo "tw_res: $tw_res"
  # name=$(echo "$tw_res" | jq -r ".user.name")
  # name_id=$(echo "$tw_res" | jq -r ".user.screen_name")
  # text=$(echo "$tw_res" | jq -r ".text")
  # local res=$(get_tw_text "$tw_res")
  get_tw_text "$tw_res" || return 1

  local tw_res_q=$(echo "$tw_res" | jq -r ".quoted_tweet")
  if [[ "$tw_res_q" != "null" ]]; then
    echo
    echo "---"
    URL=$(get_tw_url "$tw_res_q")
    echo -n "引用推文: "
    get_tw_text "$tw_res_q"
  fi
}


get_tw_____(){
  local id=$1
  id=${id%%\"}
  id=${id##\"}
  # local tw_res=$(curl -s --request GET "https://api.twitter.com/2/tweets?ids=$id&tweet.fields=text,author_id,entities&expansions=attachments.media_keys&media.fields=url,preview_image_url" --header "Authorization: Bearer $BEARER_TOKEN")
  # local tw_res=$(curl -s --request GET "https://api.twitter.com/2/tweets?ids=$id&tweet.fields=text,author_id,entities&user.fields=name,username&expansions=attachments.media_keys,author_id&media.fields=url,preview_image_url" --header "Authorization: Bearer $BEARER_TOKEN")


  # 20230716: no worked https://stackoverflow.com/questions/65595139/twitter-api-version-2-throws-client-forbidden-error https://developer.twitter.com/en/portal/products/basic
  local tw_res=$(curl -s --request GET "https://api.twitter.com/2/tweets/$id?tweet.fields=text,author_id,entities&user.fields=name,username&expansions=attachments.media_keys,author_id&media.fields=url,preview_image_url" --header "Authorization: Bearer $BEARER_TOKEN")


  [[ "$2" == "debug" ]] && echo "tw_res: $tw_res"
  #local text=$(echo $tw_res | jq '.data[0].text' )
#  text=${text%%\"}
#  text=${text##\"}
  # text=$( echo -ne "$text" )
  #local text=$(echo "$tw_res" | jq -r '.data[0].text' )
  local text=$(echo "$tw_res" | jq -r '.data.text' )
  #local name=$( get_tw_name $(echo "$tw_res" | jq '.data[0].author_id' ) )
  local name=$( echo "$tw_res" | jq -r '.includes.users[0].name' )
#  name=${name%%\"}
#  name=${name##\"}
  if [[ "$text" == "null" ]]; then
    echo "error"
    echo "res: $tw_res"
    return 1
  fi
  local i
  for((i=0; i<64 ; i++ ))
  do
    #local url_data=$(echo $tw_res | jq ".data[0].entities.urls[$i]" )
    local url_data=$(echo $tw_res | jq ".data.entities.urls[$i]" )
    [[ "$url_data" == "null" ]] && break
    local url=$(echo $url_data | jq -r '.url' )
    local expanded_url=$(echo $url_data | jq -r '.expanded_url' | cut -d '&' --output-delimiter='\&' -f 1-)
    local display_url=$(echo $url_data | jq -r '.display_url' )
    local start=$(echo $url_data | jq '.start' )
    local end=$(echo $url_data | jq '.end' )
    if [[ $(echo $display_url | grep -c -E "pic\.twitter\.com\/" ) -eq 1 ]];then
      # text=$( echo $text | sed "s|$url|img|" )
      text=$( echo "$text" | sed "s|$url||" )
    else
      # text="${text:0:$start}$(echo $url_data | jq '.expanded_url' )${text:$end:}"
      text=$( echo "$text" | sed "s|$url| $expanded_url |" )

    fi
    # echo "text: $text"
  done

  for((i=0; i<8 ; i++ ))
  do
    local url_data=$(echo $tw_res | jq ".includes.media[$i]" )
    [[ "$url_data" == "null" ]] && break
    [[ $i -eq 0 ]] && text="$text

"
    local type=$(echo $url_data | jq -r '.type' )
    if [[ "$type" == "photo" ]]; then
      local url=$(echo $url_data | jq -r '.url' )
#    elif [[ "$type" == "video" ]]; then
    elif [[ "$type" == "video" || "$type" == "animated_gif"  ]]; then
      cd $LP
      local url=$(echo $url_data | jq -r '.preview_image_url' )
#      local filename=$(youtube-dl --get-filename $URL)
      local filename=$(youtube-dl --id --get-filename "$URL")
        [[ -e "$filename" ]] && [[ "$(du -b "$filename" | cut -f1)" == "0" ]] && rm "$filename"
        [[ -e "$filename" ]] || {
#          you-get -O "${filename%.*}" "$URL"
          [[ -n "$filename" ]] && youtube-dl -q --id "$URL"
          [[ -e "$filename" ]] || {
            [[ -z "$filename" ]] && filename="$(date "+%Y%m%d_%H%M%S").mp4"
            you-get -O "${filename%.*}" "$URL" &>/dev/null
          }
        }
      [[ -e "$filename" ]] && [[ "$(du -b "$LP/$filename" | cut -f1)" -gt 0 ]] && url="https://$DOMAIN/$( bash "$SH_PATH/"urlencode.sh "$filename" )"
    else
   	  local url=$(echo $url_data | jq -r '.preview_image_url' )
    fi
    local file_path=$( bash "$SH_PATH/link_to_file.sh" "$url") && {
      url=$( bash "$SH_PATH/file_to_ipfs.sh" "$file_path" $2) || {
          local fn=${file_path##*/}
          local fn_en=$(bash "$SH_PATH/"urlencode.sh "$fn")
          local my_url="https://$DOMAIN/$fn_en"
  #         url="$my_url
  # E: no open ipfs gateway"
        url="$my_url"
      }
    }
    [[ "$2" == "debug" ]] && echo "path: $file_path"
    [[ "$2" == "debug" ]] && echo "final url: $url"
    text="$text
$type: $url"
  done
  echo "twitter to text: $URL"
  echo -n "$name: "
  echo "$text"
  return 0
  echo -ne "\n"
  echo -ne "\n"
#  echo -e "\n--"; echo "${name}: $text"
  echo "$name" | sed 's/^/> /g'
  echo "$text" | sed 's/^/> /g'

}


#twitter link to text
twitter_to_text(){
  # local URL="$1"
  URL="$1"
  shift
  if [[ "$URL" == "" ]]; then
    return 1
  fi
  # URL=$( echo "$URL" | grep -v -P "^>( >)* ?" | grep -o -P "^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./=&%-]+" )

# if [[ $(echo "$URL" | grep -v -P "^>( >)* ?" | grep -c -P "^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$") -eq 1 ]]; then
  if echo "$URL" | grep -q -P "^https://(mobile\.)?(twitter|x)\.com/[a-zA-Z0-9_./?=&%-]+$"; then
    local id=$( echo "$URL" | grep -v -P "^>( >)* ?" | grep -o -P "^https://(mobile\.)?(twitter|x)\.com/[a-zA-Z0-9_./?=&%-]+$" | grep -i -o -E "/status/[0-9]{5,}" | grep -i -o -E "[0-9]{5,}" )

    if [[ -n "$id" ]]; then
      # local tmp=$(get_tw "$id" "$@") || echo $?
      local tmp
      # tmp=$(get_tw "$id" "$@") || echo $?
      tmp=$(get_tw "$id" "$@") || return 1
      # echo $?
      # echo "$URL"
      echo "$tmp"
    else
      echo "E: error twitter id"
    fi
  else
    echo "E: error twitter url"
    return 2
  fi

}


if [[ "$1" == "help" || -z "$1" ]]; then
  echo "解析推特链接
用法: .tw 推文链接"
# 用法：.tw 推文链接 [all|tmp|*only dtube]"
else
  twitter_to_text "$@"
fi






