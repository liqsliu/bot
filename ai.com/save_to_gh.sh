#!/bin/bash


export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
# [[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/mt.log" || export LOG_FILE=/dev/null



# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
# LP=${LP:-/var/www/dav/tmp}
LP=${LP:-$HOME/tera/tmp}
#DOMAIN=${DOMAIN:-liuu.tk}
DOMAIN=$(cat $SH_PATH/DOMAIN)
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-64000000}

export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"

# GP=${GP:-$HOME/bot/note}
# GP=${GP:-$HOME/wtfipfs/txt}

USERNAME=wtfipfs
DIR=d



if [[ "$2" == md ]]; then
  fe=md
else
  fe=txt
fi
GP=${GP:-$HOME/$DIR/$fe}
[[ -e "$GP" ]] || mkdir "$GP" || exit $?

if [[ $(echo "$1" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(txt|md)$") -eq 1 ]]; then
  URL=$1
  file_path=$(bash "$SH_PATH/link_to_file.sh" "$URL" "only") || {
    echo "E: error url, result: $file_path"
    exit $?
  }
  if [[ -f "$file_path" ]]; then
    if file -i "$file_path"| grep -q "text/plain"; then
      fs=$(du -b "$file_path"|cut -f1)
      # if [[ $fs -le 512000 ]]; then
      if [[ $fs -le 1024000 ]]; then
        fn=${URL##*/}
        if [[ "$fe" != "${URL##*.}" ]]; then
          fn+=.$fe
        fi
        if [[ -f "$GP/$fn" ]]; then
          fn=$(date "+%Y%m%d_%H%M%S")"_$fn"
        fi
        cp "$file_path" "$GP/$fn"
      else
        echo "E: too big"
      fi
    else
      echo "E: txt only"
    fi
  else
    echo "E: no $file_path"
  fi
else
  fn=$(date "+%Y%m%d_%H%M%S").$fe
  echo "$1" > "$GP/$fn"
fi

# mp m && mygit pull && bash init.sh && mygitcommit

if [[ -n "fn" ]]; then
# bash -i -c "
# cd $GP
# cd ..
# mp m && mygit pull && mygitcommit
# " &>/dev/null
cd ~
cd "$DIR"
{ git pull && git add . && git commit -a -m "$(date "+%Y%m%d_%H%M%S"): commit by $USER/${host_name}/${operating_system_name}/${kernel_name}/${machine_hardware_name}" --no-edit && git push; } >/dev/null 2>&1

echo https://github.com/$USERNAME/$DIR/blob/main/$fe/"$fn"
fi
