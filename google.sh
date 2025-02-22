#!/bin/bash

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}


if [[ -z "$1" ]]; then
  echo ".google \$words"
  echo ".google -n \$num \$words"
  echo
  echo "https://github.com/jarun/googler"
else
  if [[ "$1" != "-n" ]]; then
#    res=$( googler -n 1 -c en -l en --json -6 search "$@" )
    # res=$( googler -n 64 -c en -l en --json -6 "$@" )
    res=$( googler -n 64 -c en -l en --json "$@" )
    url=$(echo "$res" | jq -r ".[0].url")
    if [[ "$url" == "null" ]]; then
      # res=$( googler -n 1 -c en -l en --json -6 "$@" )
      res=$( googler -n 1 -c en -l en --json "$@" )
      url=$(echo "$res" | jq -r ".[0].url")
      if [[ "$url" == "null" ]]; then
        echo "E: $res"
      fi
    fi
    title=$(echo "$res" | jq -r ".[0].title")
    abstract=$(echo "$res" | jq -r ".[0].abstract")
    echo "$url [${title}] $abstract"
  else
    num=$2
    shift
    shift
   # res=$( googler -n $num -c en -l en --np -6 "$@" )
    res=$( googler -n $num -c en -l en --np "$@" )

    echo "$res"
  fi
fi
