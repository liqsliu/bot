#!/bin/bash



log_msg(){

  echo "#### `date "+%Y%m%d_%H%M%S"` ####"
  local i=0
  for i in "$@"
  do
    echo -n "||$i"
  done
  echo
  echo "#### END ####"
}

log_msg "$@" &>> ~/tera/mt.log

