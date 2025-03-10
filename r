#!/bin/bash
(
cd ~/bot || exit 1
pkill -x mt
pkill -x toxbot
echo "wait ..."
# sleep 5
vgp && tgp && bash init.sh || break

while true
do
python3 -m bot && {
  echo 'ok. stop ...'
  break
} || r=$?
echo "res: $r"
date
vgp && tgp && bash init.sh || break
Tgpp && make || exit 1

pkill -x mt
pkill -x toxbot
if [[ "$r" -eq 1 ]]; then
  # ctrl+C
  echo stop by me
  sleep 2
else
  echo "restart ..."
  echo "wait ..."
  sleep 5
fi
done
)
