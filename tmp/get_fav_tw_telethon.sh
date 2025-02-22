#!/bin/bash

#https://unix.stackexchange.com/a/543068
#bash ~/.bashrc


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
LP=${LP:-/var/www/dav/tmp}
DOMAIN=${DOMAIN:-liuu.tk}
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-15000000}

# BEARER_TOKEN="$(cat "$SH_PATH//keys" | grep BEARER_TOKEN | cut -d' ' -f 2)"

PRIVATE_KEYS_PATH="${HOME}/.ssh/private_keys.txt"

BEARER_TOKEN=$(grep BEARER_TOKEN "$PRIVATE_KEYS_PATH")
BEARER_TOKEN=${BEARER_TOKEN#* }

#https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by-username-username#tab0
MY_USER_ID=$(grep MY_USER_ID "$PRIVATE_KEYS_PATH")
MY_USER_ID=${MY_USER_ID#* }


MAX_TW_NUM=5


get_tw() {
  #local tw_res=$(curl -s --request GET "https://api.twitter.com/2/tweets/$id?tweet.fields=text,author_id,entities&user.fields=name,username&expansions=attachments.media_keys,author_id&media.fields=url,preview_image_url" --header "Authorization: Bearer $BEARER_TOKEN")
  local tw_res=$(curl -s --request GET "https://api.twitter.com/2/users/$MY_USER_ID/liked_tweets?max_results=$MAX_TW_NUM&tweet.fields=text,author_id,entities&user.fields=name,username&expansions=attachments.media_keys,author_id&media.fields=url,preview_image_url" --header "Authorization: Bearer $BEARER_TOKEN")

  local media_data=$(echo "$tw_res" | jq ".includes.media")
  local user_data=$(echo "$tw_res" | jq ".includes.users")
  local cur_tw_id=$(cat $SH_PATH/cur_tw_id)
  local j
  for ((j = 0; j < $MAX_TW_NUM; j++)); do
    local tw_data=$(echo "$tw_res" | jq ".data[$j]")
    [[ "$tw_data" == "null" ]] && break
    local id=$(echo "$tw_data" | jq -r ".id")
    if [[ "$id" == "$cur_tw_id" ]]; then
      break
    fi
    if [[ "$j" == "0" ]]; then
      echo "$id" >$SH_PATH/cur_tw_id
    else
      echo
    fi
    local text=$(echo "$tw_data" | jq -r ".text")
    #local name=$( echo "$tw_res" | jq -r ".includes.users[$j].name" )
    local name=$(echo "$user_data" | jq -r ".[$j].name")
    #https://twitter.com/holymation/status/1440841871308115971?s=09
    local username=$(echo "$user_data" | jq -r ".[$j].username")
    local URL="https://twitter.com/$username/status/$id"
    [[ "$2" == "debug" ]] && echo "name$j: $name"
    [[ "$2" == "debug" ]] && echo "includes: $(echo "$tw_res" | jq -r ".includes")"
    local i
    for ((i = 0; i < 64; i++)); do
      local url_data=$(echo "$tw_data" | jq ".entities.urls[$i]")
      [[ "$url_data" == "null" ]] && break
      local url=$(echo $url_data | jq -r '.url')
      local expanded_url=$(echo $url_data | jq -r '.expanded_url' | cut -d '&' --output-delimiter='\&' -f 1-)
      local display_url=$(echo $url_data | jq -r '.display_url')
      if [[ $(echo $display_url | grep -c -P "pic\.twitter\.com\/") -eq 1 ]]; then
        text=$(echo "$text" | sed "s|$url||")
      else
        text=$(echo "$text" | sed "s|$url| $expanded_url |")

      fi
    done

    local k
    for ((k = 0; k < 6; k++)); do

      local media_key=$(echo "$tw_data" | jq -r ".attachments.media_keys[$k]")
      [[ "$media_key" == "null" ]] && break
      [[ "$2" == "debug" ]] && echo "media_keys$j: $media_key"
#      [[ $k -eq 0 ]] && text="$(bash "$SH_PATH/text2markdown.sh" "$text")"

      local url_data=$(echo "$media_data"  | jq -c --arg media_key "$media_key" '.[]|select(.media_key == $media_key)|.')
      [[ -z "$url_data" ]] && continue

      local type=$(echo "$url_data" | jq -r '.type')
      if [[ "$type" == "photo" ]]; then
        local url=$(echo "$url_data" | jq -r '.url')
      elif [[ "$type" == "video" || "$type" == "animated_gif" ]]; then
        cd $LP
        local url=$(echo "$url_data" | jq -r '.preview_image_url')
        local filename=$(youtube-dl --id --get-filename "$URL")
        [[ -e "$filename" ]] && [[ "$(du -b "$filename" | cut -f1)" == "0" ]] && rm "$filename"
        youtube-dl -q --id "$URL"
        [[ -e "$filename" ]] && [[ "$(du -b "$LP/$filename" | cut -f1)" -gt 0 ]] && url="https://$DOMAIN/$(bash "$SH_PATH/"urlencode.sh "$filename")"
      else
        local url=$(echo "$url_data" | jq -r '.preview_image_url')
      fi
#      local file_path=$(bash "$SH_PATH/link_to_file.sh" "$url") && url=$(bash "$SH_PATH/file_to_ipfs.sh" "$file_path") || url="E: $file_path"
      url=$(bash "$SH_PATH/link_to_file.sh" "$url") || url="E: $file_path"

#      text="$text [$type]($(bash "$SH_PATH/text2markdown.sh" "$url"))"
#      text="$text [$type]($url)"
#     text="$text
#$(bash "$SH_PATH/text2markdown.sh" "$url")"
      [[ $k -eq 0 ]] && files="$url" || files="$files $url"
    done
#  nohup bash "$SH_PATH/btg.sh" setcid tw "$URL
#$name
#$text" &> /dev/null &
#nohup bash "$SH_PATH/btg.sh" setcid tw  --md "$(bash "$SH_PATH/text2markdown.sh" "$URL")
#*$(bash "$SH_PATH/text2markdown.sh" "$name")*: $text" &> /dev/null &

[[ -n "$text" ]] && text="$URL
**$name**: $text" || text="$URL"

[[ -z "$files" ]] && {
python3 "$SH_PATH/twtg.py" "$text" &>> ~/tera/t.log
} || {
python3 "$SH_PATH/twtg.py" "$text" "$files" &>> ~/tera/t.log
}
  done

}
get_tw "$@"
