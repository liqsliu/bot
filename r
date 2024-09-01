#!/bin/bash



(

cd ~/bot

while true
do
vgp
tgp && bash init.sh && python3 -m tggpt && break

pkill -x mt
echo "restart ..."
sleep 8

done
)
