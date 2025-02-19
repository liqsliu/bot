#!/bin/bash
(

pkill -x mt
echo "wait ..."
sleep 2
cd ~/bot
while true
do
vgp && tgp && bash init.sh || break
python3 -m bot && {
  echo 'ok. stop ...'
  break
} || r=$?
echo "res: $r"

pkill -x mt
date
echo "restart ..."
echo "wait ..."
sleep 3
done
)
