#!/bin/bash

echo 1
echo "$1"
[[ "$1" == "name" ]] && echo "==name"
echo 2
echo "$2"
[[ "$2" == "text" ]] && echo "==text"
echo "########"
echo "$*"

echo "########"
echo $@

