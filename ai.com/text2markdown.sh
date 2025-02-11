#!/bin/bash


get_md_telethon(){
  text="$*"
  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

  text="$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )"
  text="$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )"
  text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"

  # text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  cat << EOF
$text
EOF
}

get_md_link(){
  text="$*"
  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
  cat << EOF
$text
EOF
}


get_md_code(){
  text="$*"
  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
  text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"
  cat << EOF
$text
EOF
}

get_md(){
  text="$*"
  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
  text="$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )"
  text="$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )"
  text="$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )"
  text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"

  # text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  cat << EOF
$text
EOF
}


conv_mdv2(){
  text="$*"


  text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

  text="$(echo "$text" | cut -d '_' --output-delimiter='\_' -f 1- )"
  text="$(echo "$text" | cut -d '*' --output-delimiter='\*' -f 1- )"
  text="$(echo "$text" | cut -d '[' --output-delimiter='\[' -f 1- )"
  text="$(echo "$text" | cut -d ']' --output-delimiter='\]' -f 1- )"
  text="$(echo "$text" | cut -d '(' --output-delimiter='\(' -f 1- )"
  text="$(echo "$text" | cut -d ')' --output-delimiter='\)' -f 1- )"
  text="$(echo "$text" | cut -d '~' --output-delimiter='\~' -f 1- )"
  text="$(echo "$text" | cut -d '`' --output-delimiter='\`' -f 1- )"
  text="$(echo "$text" | cut -d '>' --output-delimiter='\>' -f 1- )"
  text="$(echo "$text" | cut -d '#' --output-delimiter='\#' -f 1- )"
  text="$(echo "$text" | cut -d '+' --output-delimiter='\+' -f 1- )"
  text="$(echo "$text" | cut -d '-' --output-delimiter='\-' -f 1- )"
  text="$(echo "$text" | cut -d '=' --output-delimiter='\=' -f 1- )"
  text="$(echo "$text" | cut -d '|' --output-delimiter='\|' -f 1- )"
  text="$(echo "$text" | cut -d '{' --output-delimiter='\{' -f 1- )"
  text="$(echo "$text" | cut -d '}' --output-delimiter='\}' -f 1- )"
  text="$(echo "$text" | cut -d '.' --output-delimiter='\.' -f 1- )"
  text="$(echo "$text" | cut -d '!' --output-delimiter='\!' -f 1- )"


  # text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- )"
  cat << EOF
$text
EOF
}






#conv_mdv2 "$@"

if [[ "$2" == "link" ]];then
  get_md_link "$1"
elif [[ "$2" == "code" ]];then
  get_md_code "$1"
elif [[ "$2" == "v1" ]];then
  get_md "$1"
elif [[ "$2" == "telethon" ]];then
  get_md_telethon "$1"
elif [[ "$2" == "v2" ]];then
  conv_mdv2 "$1"
else
  conv_mdv2 "$@"
fi





