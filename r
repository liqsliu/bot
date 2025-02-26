#!/bin/bash
(
pkill -x mt
echo "wait ..."
sleep 5
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
if [[ "$r" -eq 1 ]]; then
  echo stop by me
else
echo "restart ..."
echo "wait ..."
sleep 5
fi
done
)
