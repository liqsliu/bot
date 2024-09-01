#!/bin/bash



(

pkill -x mt
sleep 8
cd ~/bot
while true
do
vgp
tgp && bash init.sh && python3 -m tggpt && {
  echo ok
  break
}

pkill -x mt
date
echo "restart ..."
sleep 8
done
)
