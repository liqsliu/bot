#!/bin/bash



(

pkill -x mt
sleep 8
cd ~/bot
while true
do
vgp
r=0
tgp && bash init.sh && python3 -m tggpt && {
  echo ok
  break
} || r=$?
echo "res: $r"

pkill -x mt
date
echo "restart ..."
sleep 8
done
)
