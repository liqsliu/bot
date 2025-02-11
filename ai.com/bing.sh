#!/bin/bash
#
curl "http://127.0.0.1:5500/?text=$1"

exit
fileTMP="$1"
curl -s -F file=@"${fileTMP}" http://127.0.0.1:5500/
