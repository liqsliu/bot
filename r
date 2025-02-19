#!/bin/bash



(

pkill -x mt
sleep 8
cd ~/bot
while true
do
vgp && tgp && bash init.sh || break
# python3 -m tggpt && {
python3 -m bot && {
  echo 'ok. stop ...'
  break
} || r=$?
echo "res: $r"

pkill -x mt
date
echo "restart ..."
sleep 8
done
)
